import json
from datetime import datetime
from tools import tool_definitions, save_goal, get_goals
from google import genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Config Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the .env file")

client = genai.Client(api_key=api_key)

# Simulated current date
CURRENT_DATE = datetime(2025, 5, 10)  # Example: May 4, 2024

message_history = []

welcome_message = {
    "role": "system",
    "content": "Hi! I am Budgy, your personal financial coach helping you set a realistic financial goal. What would you like to achieve?"
}

async def handle_goal_agent_prompt(input: str):
    try:
        # Starting the conversation.
        if input.strip().lower() == "/start":
            message_history.clear()
            message_history.append(welcome_message)
            return {"content": welcome_message["content"]}

        message_history.append({
            "role": "user",
            "content": input
        })

        example_tool_params = {
            "goal_name": "Downpayment for an apartment", 
            "target_amount": 7000.0, 
            "monthly_amount": 400.0, 
            "due_date": "2026-11-30"
            }

        prompt = f"""
        You are Budgy, an AI Agent that helps users to set a realistic financial goal based on their wishes.
        You should make decisions based on the user's question, conversation history, and the tools available to you.
        Here is some information for you:

        Current date: {CURRENT_DATE.strftime('%Y-%m-%d')}
        User's question: {input}
        Previous messages: {json.dumps(message_history)}
        Available tools: {json.dumps(tool_definitions)}
        You should make a decision if you need to use a tool to answer the user's question. Do not attempt to use a tool unless you have all required parameters. Partial tool calls are not allowed.
        Any response must strictly follow one of the following three formats. Do not include extra text outside the format.

        Formats:
        - If you need more information from the user, return the response in the following format: "REQUEST_INFORMATION:::question"
        - If you want to use a tool, return the response in the following format: "USE_TOOL:::tool_name:::parameters". Make sure that the parameters in the tool call are valid JSON and enclosed as a JSON object.
        - If you want to answer the user directly, return the response in the following format: "ANSWER:::answer"

        Example response of tool usage: USE_TOOL:::save_goal:::{json.dumps(example_tool_params)}
        """

        agent_response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        message_history.append({
            "role": "system",
            "content": agent_response.text
        })

        # Check if the response contains USE_TOOL
        if "USE_TOOL:::" in agent_response.text:
            tool_response = await handle_tool_usage(agent_response.text)
            
            message_history.append({
                "role": "system",
                "content": tool_response
            })

            return {
                "content": f"Agent reasoning: {agent_response.text} - Tool response: {tool_response}"
            }

        return {
            "content": agent_response.text
        }
    except Exception as e:
        return {
            "content": f"An error occurred: {str(e)}"
        }



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
            result = save_goal(parameters)  # Call the save_goal function with validated parameters
        elif tool_name == "get_goals":
            result = get_goals()
        else:
            return f"Unknown tool: {tool_name}"

        # Return the result of the tool execution
        return f"Tool '{tool_name}' executed successfully. Result: {json.dumps(result)}"
        
    except Exception as e:
        return f"An error occurred while using the tool: {str(e)}"
        