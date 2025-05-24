import json
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
        "description": "Saves a new financial goal for a user, and returns the saved goal. You should only use this tool when you have all the information needed to save a goal and think that the user can realistically save the desired amount.",
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
        else:
            return f"Unknown tool: {tool_name}"

        # Return the result of the tool execution
        return f"Tool '{tool_name}' executed successfully. Result: {json.dumps(result)}"
        
    except Exception as e:
        return f"An error occurred while using the tool: {str(e)}"


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


    
