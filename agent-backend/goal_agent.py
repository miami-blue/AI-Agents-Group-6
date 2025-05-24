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
            "goal_name": "Apartment Downpayment", 
            "target_amount": 7000.0, 
            "monthly_amount": 400.0, 
            "due_date": "2026-11-30"
            }

        prompt = f"""
        You are Budgy, an AI Agent that helps users to set a realistic financial goal based on their wishes. You should be helpful but realistic, taking the role of a financial coach.

        ## OBJECTIVE
        Assess the feasibility of the user's wish before saving it as a goal. You may:
        - Use tools to gather the user's financial situation (e.g. existing goals)
        - Ask the user for more information if it's not accessible via tools.
        - Suggest alternative or more realistic goals if needed.

        ONLY SAVE THE GOAL AFTER YOU HAVE ALL INFORMATION AND HAVE CONFIRMED THAT THE USER CAN REALISTICALLY SAVE THE DESIRED AMOUNT.
        A user can be considered able to realistically save if their expected monthly savings exceed or match the goals required monthly contribution, after accounting for other ongoing goals.
        IF YOU WANT TO SUGGEST A MODIFIED OR ALTERNATIVE GOAL, ALWAYS CONFIRM WITH THE USER BEFORE SAVING IT.
         
        ## CONTEXT
        User input: {input}
        Current date: {CURRENT_DATE.strftime('%Y-%m-%d')}
        Previous messages: {json.dumps(message_history)}
        Available tools: {json.dumps(tool_definitions)}

        ## TOOL USAGE RULES
        - Only use tools listed in Available tools.
        - Tool calls must include ALL required parameters in JSON format.
        - Partial tool calls are not allowed. If you do not have all required parameters, you should use another tool to gather the missing information or request more information from the user. If you cannot obtain required data from tools, ask the user directly instead of guessing.
        - If a task requires multiple tools, you should start with the first required tool call, and explain in your reasoning what steps follow. Only the first tool will be executed immediately.

        ## RESPONSE FORMAT
        - YOU MUST RESPOND IN EXACTLY ONE OF THE FOLLOWING FORMATS. DO NOT MIX FORMATS OR ADD EXTRA TEXT.

        
        - Include the complete response you want to return to user after the formatted part starts. ANYTHING BEFORE THE FORMATTED PART IS NOT RETURNED TO USER.
        - If you need to add reasoning that the AI Agent in next step should use, always add it before the format starts.
        - Do not add reasoning if it's not necessary.
       
        1. If you need more information from the user, return the response in the following format: REQUEST_INFORMATION:::response
        2. If you want to answer the user directly, return the response in the following format: ANSWER:::response
        3. If you want to use a tool, return the response in the following format, making sure that the parameters are enclosed as a JSON object: reasoning USE_TOOL:::tool_name:::parameters

        ## EXAMPLE RESPONSES

        1. Using one tool
        Response: USE_TOOL:::save_goal:::{json.dumps(example_tool_params)}

        2. Using multiple tools
        Response: User wants to delete a goal, but did not provide the ID. To accomplish this, I should follow these steps: 1. Get the existing goals using tool get_goals and find the ID of the goal with matching name 2. Delete the goal by ID with the tool delete_goal. USE_TOOL:::get_goals:::{{}}
       
        3. Requesting more information
        Response: REQUEST_INFORMATION:::Okay, let's analyze your situation. You have $800 available for savings each month, and you're currently allocating it to the following goals:

        *   Downpayment for an apartment: $694.44/month
        *   Skiing trip next January: $250/month
        *   Bicycle for next April: $55.56/month

        This adds up to a total of $1000/month in planned savings. Since you only have $800 available, you're over budget by $200.

        To proceed, we need to either adjust your savings plan or your goals. I can suggest some options:

        1.  **Reduce the monthly contribution to one or more of your existing goals.** For example, you could reduce the monthly amount for the downpayment, skiing trip or bicycle.
        2.  **Extend the timeline for one or more of your existing goals.** This would reduce the required monthly savings amount.
        3.  **Postpone or eliminate one of your goals.** If a goal is not essential, removing it would free up funds for your other goals.

        Which of these options would you prefer to explore? Should I suggest concrete changes to any of the existing goals?
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

            Current date: {CURRENT_DATE.strftime('%Y-%m-%d')}
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




        