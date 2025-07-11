from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json, os, re
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
#GEMINI_API_KEY=AIzaSyDWdNRKn9kRxkvF6adWlCLUh6aO5RQxS_o
if not api_key:
    raise ValueError("GEMINI_API_KEY missing in .env")

genai.configure(api_key=api_key)
gemini = genai.GenerativeModel(
    "gemini-2.0-flash",
    generation_config=genai.GenerationConfig(
        temperature=0.25,                   
        top_p=0.9,
        max_output_tokens=2048
    )
)
app = FastAPI()

CURRENT_DATE = datetime(2025, 5, 12)
#OUTLINE_RE = re.compile(r"^\s*1\.\s")

def _read_db() -> Dict[str, Any]:
    with open("db.json") as f:
        return json.load(f)

def _write_db(data: Dict[str, Any]):
    with open("db.json", "w") as f:
        json.dump(data, f, indent=2)

# ---------- Domains --------------------------------------------------

def _month_str(dt: datetime) -> str:
    return dt.strftime("%Y-%m")

def get_transactions(month: str) -> List[Dict]:
    """Return all txns for the yyyy-mm period."""
    data = _read_db()["transactions"]
    return [
        t for t in data
        if t["Date"].startswith(month)       # quick filter
    ]

def total_by_category(txns: List[Dict]) -> Dict[str, float]:
    cat_tot = {}
    for t in txns:
        cat = t["Category"]
        cat_tot[cat] = cat_tot.get(cat, 0.0) + float(t["Amount"])
    return {k: round(v, 2) for k, v in cat_tot.items()}

def load_budget(month: str) -> Dict[str, float]:
    """Budget already saved by your Budget Agent."""
    db = _read_db()
    budgets = db.get("budget", [])

    # detect flat rows: they have a "Month" key
    if budgets and "Month" in budgets[0]:
        return {
            row["Category"]: row["Amount"]
            for row in budgets
            if row["Month"] == month
        }

    # otherwise fall back to the nested structure
    for b in budgets:
        if b.get("month") == month:
            return b.get("categories", {})
    return {}

def budget_vs_actual(actual: Dict[str, float], plan: Dict[str, float]) -> Dict[str, float]:
    deltas = {}
    for cat, act_val in actual.items():
        if cat in plan and plan[cat]:
            deltas[cat] = round(100*(act_val-plan[cat])/plan[cat], 1)
    return deltas

def gather_goal_progress(month: str) -> List[Dict]:
    """Very naive: look at db.goals[*].saved field updated elsewhere."""
    db = _read_db()
    goals = db.get("goals", [])
    progress = []
    for g in goals:
        pct = round(100*g["monthly_amount"]/g["target_amount"], 1)
        progress.append({"goal": g["goal_name"], "progress_pct": pct})
    return progress

def build_summary_json(month: str) -> Dict[str, Any]:
    txns = get_transactions(month)
    actual = total_by_category(txns)
    plan   = load_budget(month)
    deltas = budget_vs_actual(actual, plan)
    
    prev_month = _month_str(datetime.strptime(month+"-01", "%Y-%m-%d") - timedelta(days=1))
    prev_txns  = get_transactions(prev_month)
    trend_tot  = round(sum(t["Amount"] for t in txns) - sum(t["Amount"] for t in prev_txns), 2)
    prev_actual = total_by_category(prev_txns)
    category_trends = {}
    all_categories = set(actual.keys()) | set(prev_actual.keys()) # Union of all categories from both months

    for cat in all_categories:
        if cat.lower() == "income": # Skip income for spending trends
            continue

        current_val = actual.get(cat, 0.0)
        prev_val = prev_actual.get(cat, 0.0)
        change = current_val - prev_val
        percent_change_str: Optional[str] #Type hinting for clarity

        if prev_val != 0:
            percent_change = round(100 * (change / prev_val), 1)
            percent_change_str = f"{percent_change}%"
        elif current_val != 0 : # prev_val is 0, but current_val is not
            percent_change_str = "new_category_spending" # Indicates spending in a new category or one with no previous spend
        else: # both are 0
            percent_change_str = "no_change_or_no_spending"

        category_trends[cat] = {
            "current_spending": round(current_val,2),
            "previous_spending": round(prev_val,2),
            "change_amount": round(change, 2),
            "percent_change": percent_change_str
        }
    goals = gather_goal_progress(month)

    # Add top transactions for key categories
    top_transactions_details: Dict[str, List[Dict[str, Any]]] = {}
    if actual: # Check if there's any actual spending
        # Identify the most spent category (excluding income)
        # Create a copy of actual to filter out income for this specific calculation
        spending_actual = {k: v for k,v in actual.items() if k.lower() != "income"}
        if spending_actual: # if there are any spending categories left
            most_spent_category = max(spending_actual, key=lambda k: abs(spending_actual[k]))

            # Get top 3 transactions for the most spent category
            # Ensure transactions have 'Description' and 'Amount', handle missing keys
            most_spent_txns_for_category = sorted(
                [t for t in txns if t.get("Category") == most_spent_category and t.get("Amount") is not None],
                key=lambda x: abs(float(x["Amount"])), # Assuming amount can be negative for credits, use abs if only magnitude matters
                reverse=True # Largest amounts first
            )[:3]

            transactions_to_display = []
            for t in most_spent_txns_for_category:
                description_text = t.get("Seller", "N/A") # Use Seller first
                if description_text == "N/A" and "Subcategory" in t: # Fallback to Subcategory if Seller is N/A
                    description_text = t.get("Subcategory")
                
                transactions_to_display.append({
                    "Source": description_text, # Changed key from "Description" to "Source"
                    "Amount": float(t["Amount"])
                })
            top_transactions_details[most_spent_category] = transactions_to_display
        else:
             # Handle case where actual spending is only income or empty after filtering
            most_spent_category = None # Or some default
    else:
        most_spent_category = None # No actual spending at all

    return {
        "month": month,
        "actual_totals": actual, # Contains all categories including income if present in original data
        "budget_plan": plan,
        "pct_vs_budget": deltas,
        "net_change_in_spending_vs_prev_month": trend_tot, # Clarified name
        "goal_progress": goals,
        "category_trends_vs_prev_month": category_trends, # ADDED THIS
        "top_transactions_details_for_most_spent_category": top_transactions_details, # ADDED THIS
        "most_spent_category_excluding_income": most_spent_category if most_spent_category else "N/A"
    }

# ---------- outline enforcement ---------------------------------------------

#def _ensure_outline(text: str, rerun_fn):
    #if OUTLINE_RE.match(text):
        #return text
    # ask the model to re-format once
   # repaired = rerun_fn()
   # if OUTLINE_RE.match(repaired):
    #    return repaired
    # final fallback – wrap everything in a bullet
    #return "1. " + text.replace("\n", "\n   a. ")

# ---------- API schema ------------------------------------------------------

class SummaryRequest(BaseModel):
    month: Optional[str] = None       # yyyy-mm; default = last complete month

class ChatMessage(BaseModel):
    user_message: str
    history: Optional[List[str]] = None

# ---------- endpoint: generate + store monthly summary ----------------------

@app.post("/monthly-summary/")
async def monthly_summary(req: SummaryRequest):
    try:
        # default month = previous full month
        month = req.month or _month_str(CURRENT_DATE.replace(day=1) - timedelta(days=1))
        summary_data = build_summary_json(month)

        most_spent_cat_name = summary_data.get("most_spent_category_excluding_income", "N/A")

        top_transactions_for_prompt = []
        if most_spent_cat_name != "N/A":
            top_transactions_for_prompt = summary_data.get(
                "top_transactions_details_for_most_spent_category", {}
            ).get(most_spent_cat_name, [])

        prompt = f"""
        You are **Budgy - the Monthly-Summary Agent**.
Your job is to give the user a short, encouraging recap of one month’s spending, highlighting successes and areas for improvement,
with actionable advice. Avoid judgmental language. Focus on spending habits and budget adherence.
Do not analyze income as an expense.

──────────────── SYSTEM RULES
• Respond in **exactly three parts** - nothing before Part 1 or after Part 3.
    ─ Part 1 → Plain-text narrative (≤ 30 words). Keep it concise and impactful.
    ─ Part 2 → Numerical key factors. Answer **only** the specific questions below, strictly following the requested format for each. Do not add introductory phrases.
    ─ Part 3 → The *unchanged* JSON you received, wrapped in ```json fences.
• Do **NOT** add, remove, or reorder keys in the JSON you return in Part 3.
• **CRITICAL**: All bracketed placeholders (e.g., `[value_from_JSON]`) in the formatting instructions below MUST be filled with actual data sourced DIRECTLY from the provided JSON in the CONTEXT section. Perform calculations ONLY AS INSTRUCTED. Apply signs (+/-) for changes EXACTLY as specified in the format.

──────────────── WHAT TO COVER IN PART 1
1. Briefly state the overall spending situation compared to the budget. For instance, mention if spending was generally over or under budget, or if it significantly exceeded plans. Be encouraging.

──────────────── WHAT TO COVER IN PART 2
**ATTENTION**: Adhere strictly to the JSON data for all figures and category names.
'Income' categories are excluded from spending calculations.
`category_trends_vs_prev_month.change_amount`: positive for spending DECREASE, negative for spending INCREASE.
`category_trends_vs_prev_month.percent_change`: negative for spending DECREASE, positive for spending INCREASE.

2. Identify:
    a. How much the user saved or went over budget **in total monetary terms (€)**.
        Calculation:
        1. 'Total Actual Spending': Sum `actual_totals` (excluding "Income").
        2. 'Total Budgeted Spending': Sum `budget_plan` (excluding "Income"; if category unbudgeted, use 0).
        3. Result: `abs(Total Actual Spending) - Total Budgeted Spending`.
        Format: "You [saved/went over budget by] [calculated_monetary_value]€."

    b. Progress towards "goals", if any are listed in `goal_progress`.
        Format: For each goal: "\"[goal_name_from_JSON]\" goal progress: [progress_pct_from_JSON]%." If no goals: "No specific goals tracked this month."
        (Example structure: **Category**: X%.")

    c. The category with the **highest total spending** (use `most_spent_category_excluding_income` from JSON).
        Format: "Most spent on: [category_name_from_JSON] [actual_total_amount_from_JSON]€, [pct_vs_budget_value_from_JSON]% [over/under] budget."
        (Note: For `pct_vs_budget` from JSON, a negative value means OVER budget for an expense. E.g., -308% is 308% OVER budget. Include that knowledge also in the percentage value, show the over budget percent as positive and vice versa.)
        (Example structure: "Most spent on: **Category** amount€, +X% over/ -X% under budget.")

    d. The category that showed the **most significant positive financial change for you** (largest DECREASE in spending) AND the category that showed the **most significant negative financial change for you** (largest INCREASE in spending). Source from `category_trends_vs_prev_month`.
        * Largest DECREASE: Find category with largest positive `change_amount`.
        * Largest INCREASE: Find category with most negative `change_amount` (largest absolute value).

        Format for DECREASE (when JSON `change_amount` is positive, JSON `percent_change` is negative):
        "Largest decrease: '[category_name_from_JSON]' -[value_of_JSON_change_amount]€ ([value_of_JSON_percent_change]%)."

        Format for INCREASE (when JSON `change_amount` is negative, JSON `percent_change` is positive):
        "Largest increase: '[category_name_from_JSON]' +[absolute_value_of_JSON_change_amount]€ (+[value_of_JSON_percent_change]%)."

        If no significant changes, don't answer that part

    e. The **single largest transaction by ABSOLUTE amount** from `top_transactions_details_for_most_spent_category` for the category identified in 2c.
        Format: "Largest transaction in [category_from_2c]: [Source_from_JSON_for_largest_txn] ([Amount_from_JSON_for_largest_txn]€)."
        (CRITICAL REMINDER: You MUST identify the transaction with the highest absolute monetary value from the list for that category, not just the first one.)
        (Example structure: "Largest transaction in **Category**: **Source** amount€.")

    f. Conclude with **one practical and specific tip** for next month, related to overspending (2c) or largest increase (2d).
        Format: "Tip for next month: **Your_actionable_tip_here**."

        ──────────────── CONTEXT
        Current date : {CURRENT_DATE:%Y-%m-%d}
        Monthly financial data (Note: 'Income' in actual_totals or budget_plan should be treated as income, not an expense category for spending analysis):
        ```json
        {json.dumps(summary_data, indent=2)}
        ```
        """



# ----- call LLM ------------------------------------------------------
        resp = gemini.generate_content(prompt)
        raw = resp.text

        # split explanation + JSON
        try:
            expl, js = raw.split("```json", 1)
            js = js.split("```")[0]
            parsed = json.loads(js)
        except Exception as e:
            raise ValueError("Parsing LLM output failed") from e

        # store summary back to DB
        db = _read_db()
        db.setdefault("summaries", [])
        db["summaries"] = [s for s in db["summaries"] if s["month"] != month] + [parsed]
        _write_db(db)

        return {"explanation": expl.strip(), "summary": parsed}

    except Exception as e:
        raise HTTPException(500, detail=f"Summary error: {e}")
