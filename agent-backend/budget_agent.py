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

        prompt_template = """
        You are Budgy, an AI Agent that helps users to set a realistic financial budget for the upcoming month based on their past transactions and spending history.
        You should make decisions based on the user's transaction history, user's question, conversation history, and the tools available to you.
        You should start forming a budget straight away and guide the user through the process. You shuold always back your decisions with data from the user's transaction history.
        Do not ask the user for information that you can get from the tools available to you.
        You should always leave the user with a question or query yourself again to keep the conversation going.
        Here is some information for you:

        Current date: {current_date}
        User's question: {user_input}
        Previous messages: {message_history}
        Available tools: {tools}
        You should make a decision if you need to use a tool to answer the user's question. Do not attempt to use a tool unless you have all required parameters. Partial tool calls are not allowed.
        Any response must strictly follow one of the following three formats. Do not include extra text outside the format.

        Formats:
        - If you need more information from the user, return the response in the following format: "REQUEST_INFORMATION:::question"
        - If you want to use a tool, return the response in the following format: "USE_TOOL:::tool_name:::parameters". Make sure that the parameters in the tool call are valid JSON and enclosed as a JSON object.
        - If you want to answer the user directly, return the response in the following format: "ANSWER:::answer"

        Example response of tool usage: USE_TOOL:::save_goal:::{example_tool_params}
        """

        # Loop until the agent does not use a tool
        agent_message = input
        loop_count = 0  # Prevent infinite loops
        max_loops = 5

        while True:
            prompt = prompt_template.format(
                current_date=CURRENT_DATE.strftime('%Y-%m-%d'),
                user_input=agent_message,
                message_history=json.dumps(message_history),
                tools=json.dumps(tool_definitions),
                example_tool_params=json.dumps(example_tool_params)
            )

            agent_response = client.models.generate_content(
                model="gemini-2.0-flash", contents=prompt
            )

            message_history.append({
                "role": "system",
                "content": agent_response.text
            })

            if "USE_TOOL:::" in agent_response.text:
                tool_response = await handle_tool_usage(agent_response.text)
                message_history.append({
                    "role": "system",
                    "content": tool_response
                })
                # Feed tool response back to agent for next step
                agent_message = tool_response
                loop_count += 1
                if loop_count >= max_loops:
                    return {
                        "content": "Loop limit reached. Please try again or rephrase your request."
                    }
                continue
            else:
                # Either REQUEST_INFORMATION or ANSWER, so return to user
                return {
                    "content": agent_response.text
                }

    except Exception as e:
        return {
            "content": f"An error occurred: {str(e)}"
        }




