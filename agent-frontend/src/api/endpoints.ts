import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

interface AgentResponse {
  content: string;
}

export const sendGoalAgentPrompt = async (
  prompt: string
): Promise<AgentResponse> => {
  try {
    console.log('Sending prompt to AI agent:', prompt);
    const response = await axios.post(`${API_URL}/goal-agent/prompt`, {
      prompt,
    });
    return response.data as AgentResponse;
  } catch (error) {
    console.error('Error fetching AI response:', error);
    return { content: "Couldn't get a response from the agent." };
  }
};
