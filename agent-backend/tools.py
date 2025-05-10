tool_definitions = [
    {
        "tool_name": "get_transactions",
        "description": "Fetches a list of transactions for a given account or user.",
        "parameters": [
            {
                "name": "start_date",
                "description": "Start date of transactions to fetch. Should be formatted (YYYY-MM-DD).",
                "required": True,
                "type": "string"
            },
            {
                "name": "end_date",
                "description": "End date of transactions to fetch. Should be formatted (YYYY-MM-DD).",
                "required": True,
                "type": "string"
            }
        ],
        "expected_output": "A list of transactions within the specified date range.",
    },
    {
        "tool_name": "get_goals",
        "description": "Retrieves a list of already saved financial goals for a user.",
        "parameters": None,
        "expected_output": {
            "goals": "list of goal objects",
            "total_count": "integer"
        }
    },
    {
        "tool_name": "save_goal",
        "description": "Saves a new financial goal for a user. You should only use this tool when you have all the information needed to save a goal.",
        "parameters": {
            "goal_name": "string", 
            "target_amount": "float",
            "due_date": "string (YYYY-MM-DD)",
            "monthly_amount": "float",
        },
        "expected_output": {
            "success": "boolean",
        }
    },
    {
        "tool_name": "assess_feasibility_of_goal",
        "description": "Assesses whether a financial goal is feasible based on user data.",
        "parameters": {
            "goal_name": "string", 
            "target_amount": "float",
            "due_date": "string (YYYY-MM-DD)",
            "monthly_amount": "float",
        },
        "expected_output": {
            "feasible": "boolean",
            "reason": "string"
        }
    }
]



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

def get_transactions(start_date: str, end_date: str):
    try:
        # Load all transactions
        transactions = load_transactions()

        # Filter transactions by the given date range
        filtered_transactions = [
            transaction for transaction in transactions
            if start_date <= transaction["Date"] <= end_date
        ]

        return {
            "transactions": filtered_transactions,
            "total_count": len(filtered_transactions)
        }
    except Exception as e:
        print(f"Error processing transactions: {e}")
        raise HTTPException(status_code=500, detail="Failed to process transactions.")

def load_goals():
    try:
        # Call the FastAPI endpoint
        response = requests.get(JSON_SERVER_URL + "/goals")
        response.raise_for_status()  # Raise an error for HTTP errors
        return response.json()  # Return the JSON response as a Python list
    except requests.exceptions.RequestException as e:
        print(f"Error fetching goals: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch goals from the /goals endpoint.")