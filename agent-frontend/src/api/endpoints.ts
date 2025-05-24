import axios from 'axios';
import { AGENT_API_URL } from './apiVariables';

export interface AgentResponse {
  content: string;
}

export const sendGoalAgentPrompt = async (
  prompt: string
): Promise<AgentResponse> => {
  try {
    console.log('Sending prompt to AI agent:', prompt);
    const response = await axios.post(`${AGENT_API_URL}/goal-agent/prompt`, {
      prompt,
    });
    return response.data as AgentResponse;
  } catch (error) {
    console.error('Error fetching AI response:', error);
    return { content: "Couldn't get a response from the agent." };
  }
};
