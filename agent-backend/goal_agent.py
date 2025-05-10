import json
from datetime import datetime
from tools import tool_definitions
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
CURRENT_DATE = datetime(2024, 5, 4)  # Example: May 4, 2024

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

        prompt = f"""
        You are Budgy, an AI Agent that helps users to set a realistic financial goal based on their wishes.
        You should make decisions based on the user's question, conversation history, and the tools available to you.
        Here is some information for you:

        Current date: {CURRENT_DATE.strftime('%Y-%m-%d')}
        User's question: {input}
        Previous messages: {json.dumps(message_history)}
        Available tools: {json.dumps(tool_definitions)}
        You should make a decision if you need to use a tool to answer the user's question.

        You should format your response as follows:
        - If you need more information from the user, return the response in the following format: "REQUEST_INFORMATION:::question"
        - If you want to use a tool, return the response in the following format: "USE_TOOL:::tool_name:::parameters". parameters should be a JSON object with all the parameters needed for the tool.
        - If you want to answer the user directly, return the response in the following format: "ANSWER:::answer"
        """

        agent_response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        message_history.append({
            "role": "system",
            "content": agent_response.text
        })


        return {
            "content": agent_response.text
        }
    except Exception as e:
        return {
            "content": f"An error occurred: {str(e)}"
        }

   
