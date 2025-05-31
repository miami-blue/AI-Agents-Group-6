import json
from datetime import datetime
from tools import tool_definitions, handle_tool_usage
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
CURRENT_DATE = datetime(2024, 5, 10)  # Example: May 4, 2024

message_history = []

welcome_message = {
    "role": "system",
    "content": "Hi! I am Budgy, your personal financial coach helping you set a realistic financial budget for the upcoming month. What would you like to focus on next month?"
}

async def handle_budget_agent_prompt(input: str):
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
            "start_date": "2026-11-30",
            "end_date": "2026-12-31"
        }

        example_budget_params = {
            "Month": "2024-06",
            "Items": [
                {"Category": "Groceries", "Amount": 400.0},
                {"Category": "Rent", "Amount": 900.0},
                {"Category": "Leisure", "Amount": 100.0}
            ]
}

        prompt = f"""
        You are Budgy, an AI Agent that helps users to set a realistic financial budget for the upcoming month based on their past transactions and spending history.
        You should make decisions based on the user's transaction history, user's question, conversation history, and the tools available to you.
        You should start forming a budget straight away and guide the user through the process. You should always back your decisions with data from the user's transaction history.
        Do not ask the user for information that you can get from the tools available to you.
        You should always leave the user with a question or query yourself again to keep the conversation going.

        Current date: {CURRENT_DATE.strftime('%Y-%m-%d')}
        User's question: {input}
        Previous messages: {json.dumps(message_history)}
        Available tools: {json.dumps(tool_definitions)}
        Example response of tool usage: USE_TOOL:::get_transactions_in_range:::{json.dumps(example_tool_params)}
        Example response of tool usage: USE_TOOL:::save_budget:::{json.dumps(example_budget_params)}
        
        You should make a decision if you need to use a tool to answer the user's question. If you need a tool, don not answer the user until you no longer need tools in your response. Do not attempt to use a tool unless you have all required parameters. Partial tool calls are not allowed.

        Any response must strictly follow one of the following three formats. Do not include extra text outside the format.

        Formats:
        1. If you need more information from the user, return the response in the following format: REQUEST_INFORMATION:::question
        2. If you want to use a tool, return the response in the following format: USE_TOOL:::tool_name:::parameters (parameters must be valid JSON)
        3. If you want to answer the user directly, return the response in the following format: ANSWER:::answer
        """

        agent_response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )

        message_history.append({
            "role": "system",
            "content": agent_response.text
        })

        # Handle REQUEST_INFORMATION or ANSWER directly
        if "REQUEST_INFORMATION:::" in agent_response.text or "ANSWER:::" in agent_response.text:
            response_parts = agent_response.text.split(":::", 1)
            if len(response_parts) > 1:
                return {"content": response_parts[1].strip()}
            else:
                return {"content": "Invalid response format from the agent."}

        # Handle USE_TOOL
        while "USE_TOOL:::" in agent_response.text:
            tool_response = await handle_tool_usage(agent_response.text)
            message_history.append({
                "role": "system",
                "content": tool_response
            })

            tool_used_prompt = f"""
            You are Budgy, an AI Agent that helps users to set a realistic financial budget for the upcoming month.
            You have used a tool to gather information about the user's financial situation. Now, you should provide a final answer to the user based on the tool's response and your previous reasoning.

            Current date: {CURRENT_DATE.strftime('%Y-%m-%d')}
            This was the user's question: {input}
            Here is your reasoning: {agent_response.text}
            Here is the tool response: {tool_response}
            Here are the previous messages: {json.dumps(message_history)}

            Available tools: {json.dumps(tool_definitions)}
            If you need to use another tool to be able to answer the user's question, you should format the response as follows: USE_TOOL:::tool_name:::parameters

            In other case, you are responding directly to the user, so provide a clear and concise answer.

            Example responses:
            User's question: What is my budget for next month?
            Your response: Based on your transaction history, your recommended budget for next month is $2,000. Would you like to adjust any categories?

            User's question: Please update my groceries budget to $400.
            Your response: I have updated your groceries budget to $400 for next month.
            """

            tool_used_explanation = client.models.generate_content(
                model="gemini-2.0-flash", contents=tool_used_prompt
            )

            message_history.append({
                "role": "system",
                "content": tool_used_explanation.text
            })

            if "USE_TOOL:::" in tool_used_explanation.text:
                agent_response = tool_used_explanation
                continue
            else:
                return {
                    "content": tool_used_explanation.text
                }

        # If the response was not in the expected format, just return the agent's response
        return {
            "content": agent_response.text
        }

    except Exception as e:
        return {
            "content": f"An error occurred: {str(e)}"
        }




