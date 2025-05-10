
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import requests
from fastapi import HTTPException

# Load environment variables from .env file
load_dotenv()

# Config Gemini
JSON_SERVER_URL = os.getenv("JSON_SERVER_URL")
if not JSON_SERVER_URL:
    raise ValueError("JSON_SERVER_URL is not set in the .env file")

tool_definitions = [
    # {
    #     "tool_name": "get_transactions",
    #     "description": "Fetches a list of transactions for a given account or user.",
    #     "parameters": [
    #         {
    #             "name": "start_date",
    #             "description": "Start date of transactions to fetch. Should be formatted (YYYY-MM-DD).",
    #             "required": True,
    #             "type": "string"
    #         },
    #         {
    #             "name": "end_date",
    #             "description": "End date of transactions to fetch. Should be formatted (YYYY-MM-DD).",
    #             "required": True,
    #             "type": "string"
    #         }
    #     ],
    #     "expected_output": "A list of transactions within the specified date range.",
    # },
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
        "description": "Saves a new financial goal for a user, and returns the saved goal. You should only use this tool when you have all the information needed to save a goal.",
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
    # {
    #     "tool_name": "assess_feasibility_of_goal",
    #     "description": "Assesses whether a financial goal is feasible based on user data.",
    #     "parameters": {
    #         "goal_name": "string", 
    #         "target_amount": "float",
    #         "due_date": "string (YYYY-MM-DD)",
    #         "monthly_amount": "float",
    #     },
    #     "expected_output": {
    #         "feasible": "boolean",
    #         "reason": "string"
    #     }
    # }
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

def get_goals():
    try:
        # Call the FastAPI endpoint
        response = requests.get(JSON_SERVER_URL + "/goals")
        response.raise_for_status()  # Raise an error for HTTP errors
        return response.json()  # Return the JSON response as a Python list
    except requests.exceptions.RequestException as e:
        print(f"Error fetching goals: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch goals from the /goals endpoint.")


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
            json=params
        )
        response.raise_for_status()  # Raise an error for HTTP errors

        return response.json()  # Return the response from the server
    except requests.exceptions.RequestException as e:
        print(f"Error saving goal: {e}")
        raise HTTPException(status_code=500, detail="Failed to save the goal to the /goals endpoint.")
    except Exception as e:
        print(f"Validation or other error: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid parameters: {str(e)}")


    
