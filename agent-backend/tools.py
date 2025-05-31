from pydantic import BaseModel
from dotenv import load_dotenv
import os
import requests
import json
from fastapi import HTTPException
from typing import Dict, List
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Config
JSON_SERVER_URL = os.getenv("JSON_SERVER_URL")
if not JSON_SERVER_URL:
    raise ValueError("JSON_SERVER_URL is not set in the .env file")

tool_definitions = [
    {
        "tool_name": "get_transactions_in_range",
        "description": "Fetches transactions for a user for a given time period.",
        "parameters": {
            "start_date": "string (YYYY-MM-DD)", 
            "end_date": "string (YYYY-MM-DD)",
        },
        "expected_output": {
            "transactions": [
                {
                    "Date": "string (YYYY-MM-DD)",
                    "Category": "string",
                    "Subcategory": "string",
                    "Amount": "float",
                    "Seller": "string"
                }
            ],
            "total_count": "integer"
        }
    },
    {
        "tool_name": "get_goals",
        "description": "Retrieves a list of already saved financial goals of the user.",
        "parameters": None,
        "expected_output": {
            "goals": [
                {
                    "goal_name": "string", 
                    "target_amount": "float",
                    "monthly_amount": "float",
                    "due_date": "string (YYYY-MM-DD)",
                }
            ]
        }
    },
    {
        "tool_name": "save_goal",
        "description": "Saves a new financial goal for a user, and returns the saved goal. You should only use this tool when you have all the information needed to save a goal and think that the user can realistically save the desired amount. If the user wants to edit an existing goal, you should first delete the existing goal using the delete_goal tool, and then save the new goal with this tool.",
        "parameters": {
            "goal_name": "string", 
            "target_amount": "float",
            "monthly_amount": "float",
            "due_date": "string (YYYY-MM-DD)",
        },
        "expected_output": {
            "goal_name": "string", 
            "target_amount": "float",
            "monthly_amount": "float",
            "due_date": "string (YYYY-MM-DD)",
        }
    },
    {
        "tool_name": "save_budget",
        "description": "Saves the entire financial budget for a month for a user. Accepts a month and a list of budget items (category and amount). Each item will be saved as a separate row in the database. Make sure you give the parameters in the correct JSON format. Make sure the tool call is a single JSON object (not a stringified or escaped object).",
        "parameters": {
            "Month": "string (YYYY-MM)",
            "Items": [
                {
                    "Category": "string",
                    "Amount": "float"
                }
            ]
        },
        "expected_output": [
            {
                "Month": "string (YYYY-MM)",
                "Category": "string",
                "Amount": "float",
                "id": "string"
            }
        ]
    },
    {
        "tool_name": "delete_goal",
        "description": "Deletes a financial goal by its ID. You should only use this tool when the user explicitly asks to delete a goal, and always ask the user to confirm the goal_name and id before executing this action. If the user does not provide an ID, you should find the goal by its goal_name from the list of goals, and get the ID from there.",
        "parameters": {
            "id": "string (UUID)",
        },
        "expected_output": {
            "id": "string (UUID)"
        }
    }
]

async def handle_tool_usage(response: str):
    try:
        # Parse the tool name and parameters from the response
        response_parts = response.split("USE_TOOL:::", 1)
        if len(response_parts) != 2:
            raise ValueError("Invalid tool usage response format")
        tool_name_and_params = response_parts[1]
        tool_name, parameters = tool_name_and_params.split(":::", 1)
        parameters = json.loads(parameters)  # Convert parameters from JSON string to dictionary

        # Dynamically call the corresponding tool function
        if tool_name == "save_goal":
            validated_params = SaveGoalParams(**parameters)
            result = save_goal(validated_params)  # Call the save_goal function with validated parameters
        elif tool_name == "get_goals":
            result = get_goals()
        elif tool_name == "delete_goal":
            validated_params = DeleteGoalParams(**parameters)  # Validate parameters using Pydantic
            result = delete_goal(validated_params)  # Call the delete_goal function with validated parameters
        elif tool_name == "get_transactions_in_range":
            result = get_transactions_in_range(parameters)
        elif tool_name == "save_budget":
            result = save_budget(parameters)
        else:
            return f"Unknown tool: {tool_name}"

        # Return the result of the tool execution
        return f"Tool '{tool_name}' executed successfully. Result: {json.dumps(result)}"
        
    except Exception as e:
        return f"An error occurred while using the tool: {str(e)}"
    # Tool functions

    # Load Transactions
def load_transactions():
    try:
        # Call the FastAPI endpoint
        response = requests.get(JSON_SERVER_URL + "/transactions")
        response.raise_for_status()  # Raise an error for HTTP errors
        return response.json()  # Return the JSON response as a Python list
    except requests.exceptions.RequestException as e:
        print(f"Error fetching transactions: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch transactions from the /transactions endpoint.")

def get_transactions(month: str):
    """Return all txns for the yyyy-mm period."""
    try:
        # Load all transactions
        transactions = load_transactions()

        # Filter transactions by the given date range
        filtered_transactions = [
        t for t in transactions
        if t["Date"].startswith(month)
        ]

        return filtered_transactions
    except Exception as e:
        print(f"Error processing transactions: {e}")
        raise HTTPException(status_code=500, detail="Failed to process transactions.")

def get_transactions_in_range(params: dict):
    """Return all transactions for the given date range (inclusive)."""
    try:
        start_date = params.get("start_date")
        end_date = params.get("end_date")
        if not start_date or not end_date:
            raise ValueError("Both start_date and end_date must be provided.")

        # Parse dates
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")

        # Load all transactions
        transactions = load_transactions()

        # Filter transactions by the given date range (inclusive)
        filtered_transactions = [
            t for t in transactions
            if start_dt <= datetime.strptime(t["Date"], "%Y-%m-%d") <= end_dt
        ]

        return {
            "transactions": filtered_transactions,
            "total_count": len(filtered_transactions)
        }
    except Exception as e:
        print(f"Error processing transactions: {e}")
        raise HTTPException(status_code=500, detail="Failed to process transactions.")

def get_goals():
    try:
        # Call the FastAPI endpoint
        response = requests.get(JSON_SERVER_URL + "/goals")
        response.raise_for_status()  # Raise an error for HTTP errors
        return response.json()  # Return the JSON response as a Python list
    except requests.exceptions.RequestException as e:
        print(f"Error fetching goals: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch goals from the /goals endpoint.")

class DeleteGoalParams(BaseModel):
    id: str
def delete_goal(params: DeleteGoalParams):
    try:
        # Send a DELETE request to the /goals endpoint with the goal_id
        response = requests.delete(
            JSON_SERVER_URL + f"/goals/{params.id}",
        )
        response.raise_for_status()  # Raise an error for HTTP errors

        return params.dict()  # Return a success message
    except requests.exceptions.RequestException as e:
        print(f"Error deleting goal: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete the goal from the /goals endpoint.")


class SaveGoalParams(BaseModel):
    goal_name: str
    target_amount: float
    monthly_amount: float
    due_date: str

def save_goal(params: SaveGoalParams):
    try:
        # Send the goal to the /goals endpoint
        response = requests.post(
            JSON_SERVER_URL + "/goals",
            json=params.dict()  # Convert Pydantic model to dictionary
        )
        response.raise_for_status()  # Raise an error for HTTP errors

        return response.json()  # Return the response from the server
    except requests.exceptions.RequestException as e:
        print(f"Error saving goal: {e}")
        raise HTTPException(status_code=500, detail="Failed to save the goal to the /goals endpoint.")
    except Exception as e:
        print(f"Validation or other error: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid parameters: {str(e)}")

class SaveBudgetParams(BaseModel):
    month: str  # Format: YYYY-MM
    items: list

def save_budget(params: dict):
    """
    Saves the entire budget for a given month (multiple categories) into the JSON server database.
    """
    try:
        month = params["Month"]
        items = params["Items"]
        if not isinstance(items, list):
            raise ValueError("Items must be a list of {Category, Amount} objects.")

        # Fetch existing budgets
        response = requests.get(JSON_SERVER_URL + "/budgets")
        response.raise_for_status()
        budgets = response.json()

        results = []
        for item in items:
            category = item["Category"]
            amount = item["Amount"]

            # Check for duplicates
            exists = any(
                b.get("Month") == month and b.get("Category") == category
                for b in budgets
            )
            if exists:
                results.append({
                    "Month": month,
                    "Category": category,
                    "Amount": amount,
                    "error": "Already exists"
                })
                continue

            # Save new budget row
            post_response = requests.post(
                JSON_SERVER_URL + "/budgets",
                json={
                    "Month": month,
                    "Category": category,
                    "Amount": amount
                }
            )
            post_response.raise_for_status()
            results.append(post_response.json())

        return results
    except Exception as e:
        print(f"Error saving budget: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid parameters: {str(e)}")


def load_budgets():
    """Fetch all budgets already saved by your Budget Agent."""
    try:
        # Call the FastAPI endpoint
        response = requests.get(JSON_SERVER_URL + "/budgets")
        response.raise_for_status()  # Raise an error for HTTP errors
        return response.json()  # Return the JSON response as a Python list
    except requests.exceptions.RequestException as e:
        print(f"Error fetching budgets: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch budgets from the /budgets endpoint.")

def get_budget(month: str) -> Dict[str, float]:
    """Budget already saved by your Budget Agent."""
    try:
        # Load all budgets
        budgets = load_budgets()

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
    except Exception as e:
        print(f"Error processing budgets: {e}")
        raise HTTPException(status_code=500, detail="Failed to process budgets.")



def gather_goal_progress(month: str) -> List[Dict]:
    """Very naive: look at db.goals[*].saved field updated elsewhere."""
    goals = get_goals()
    progress = []
    for g in goals:
        pct = round(100*g["monthly_amount"]/g["target_amount"], 1)
        progress.append({"goal": g["goal_name"], "progress_pct": pct})
    return progress


def save_summary(month: str, parsed: Dict):
    summary = {"month": month, **parsed}

    try:
        # Check if a summary for the month already exists
        response = requests.get(f"{JSON_SERVER_URL}/summaries")
        response.raise_for_status()
        existing = response.json()

        if existing:
            # Update the existing summary
            summary_id = existing[0]["id"]
            put_response = requests.put(f"{JSON_SERVER_URL}/summaries/{summary_id}", json=summary)
            put_response.raise_for_status()
        else:
            # Create a new summary
            post_response = requests.post(f"{JSON_SERVER_URL}/summaries", json=summary)
            post_response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print(f"Error saving summary for {month}: {e}")