import json
from datetime import datetime
from tools import handle_tool_usage, tool_definitions
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

        print(f"💬 User input: {input}")
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

        You should always assess the feasibility of the user's wish before saving it as a goal. You can use the available tools to gather information about the user's financial situation, such as their existing financial goals.
        You can also ask additional questions from the user to understand how much they can realistically save per month. Only request information from the user if you can not get it using the available tools.
        If the goal does not seem realistic, you can use your knowledge to suggest a more realistic or alternative goal.
        Only when you have all the information you need and confirmation that the user can realistically save the desired amount, save the goal. 
        
        You should make decisions based on the user's question, conversation history, and the tools available to you. Here is some information for you:

        Current date: {CURRENT_DATE.strftime('%Y-%m-%d')}
        User's question: {input}
        Previous messages: {json.dumps(message_history)}
        Available tools: {json.dumps(tool_definitions)}
        You should make a decision if you need to use a tool to answer the user's question. Guidelines for tool usage:
        - You should only use one tool at a time. 
        - Do not attempt to use a tool that was not listed in Available tools. 
        - Do not attempt to use a tool unless you have all required parameters. Partial tool calls are not allowed.
        
        Any response must strictly follow one of the following three formats. Do not include extra text after the format.
        You can include additional reasoning, but it should be before the format.
        Formats:
        - If you need more information from the user, return the response in the following format: "REQUEST_INFORMATION:::question"
        - If you want to use a tool, return the response in the following format: "USE_TOOL:::tool_name:::parameters". Make sure that the parameters in the tool call are valid JSON and enclosed as a JSON object.
        - If you want to answer the user directly, return the response in the following format: "ANSWER:::answer"

        Example response of tool usage: USE_TOOL:::save_goal:::{json.dumps(example_tool_params)}

        Example response of using multiple tools: User wants to delete a goal, but does not provide the ID. You should first use the get_goals tool to find the goal by its name, and then use the delete_goal tool with the ID of the goal.USE_TOOL:::get_goals:::{{}}
        """

        agent_response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )

        print(f"🔮 Reasoning: {agent_response.text}")
        message_history.append({
            "role": "system",
            "content": agent_response.text
        })

        if "REQUEST_INFORMATION:::" in agent_response.text or "ANSWER:::" in agent_response.text:
            response_parts = agent_response.text.split(":::", 1)
            if len(response_parts) > 1:
                return {"content": response_parts[1].strip()}
            else:
                return {"content": "Invalid response format from the agent."}

        # Check if the response contains USE_TOOL
        while "USE_TOOL:::" in agent_response.text:
            tool_response = await handle_tool_usage(agent_response.text)
            
            print(f"🔮 Tool response: {tool_response}")
            message_history.append({
                "role": "system",
                "content": tool_response
            })

            agent_reasoning = f"Agent reasoning: {agent_response.text} - Tool response: {tool_response}"

            tool_used_prompt = f"""
            You are Budgy, an AI Agent that helps users to set a realistic financial goal based on their wishes.
            You have used a tool to gather information about the user's financial situation. Now, you should provide a final answer to the user based on the tool's response and your previous reasoning.
            The response should explain the reasoning behind the tool usage and how it relates to the user's question.

            This was the user's question: {input}
            Here is your reasoning: {agent_response.text}
            Here is the tool response: {tool_response}
            Here are the previous messages: {json.dumps(message_history)}
            
            Available tools: {json.dumps(tool_definitions)}
            If you need to use another tool to be able to answer the user's question, you should format the response as follows: USE_TOOL:::tool_name:::parameters

            In other case, you are responding directly to the user, so provide a clear and concise answer.

            Example responses:
            User's question: I want to delete my goal with ID 1234.
            Your response: Based on your request, I successfully deleted the goal with ID 1234.

            User's question: I want to delete my goal to save for a new car.
            Your response: User wanted to delete a goal, but did not provide the ID. I first used the get_goals tool to find the goal by its name. I found this goal:{{"id": "1234", "goal_name": "New Car", "target_amount": 10000, "monthly_amount": 303.03, "due_date":"2027-12-01"}}. Now I know the ID, so I should delete this goal using the tool delete_goal.USE_TOOL:::delete_goal:::{{"id": "1234"}}
            """

            tool_used_explanation = client.models.generate_content(
            model="gemini-2.0-flash", contents=tool_used_prompt
            )

            print(f"🔮 Tool used explanation: {tool_used_explanation.text}")
            message_history.append({
                "role": "system",
                "content": tool_used_explanation.text
            })

            if "USE_TOOL:::" in tool_used_explanation.text:
                # If the tool used explanation contains USE_TOOL, we need to call the tool again
                agent_response = tool_used_explanation
                continue
            # If the tool used explanation does not contain USE_TOOL, we can return the final answer
            else:
                # Return the final answer to the user
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




        