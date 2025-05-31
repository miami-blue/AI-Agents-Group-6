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

export const generateMonthlySummary = async (
  month: string
): Promise<AgentResponse> => {
  try {
    const regex = /^\d{4}-(0[1-9]|1[0-2])$/; // Check that month matches YYYY-MM format
    const isValid = regex.test(month);
    if (!isValid) {
      throw new Error(
        'Not a valid month string. Month should be in the format YYYY-MM'
      );
    }
    console.log('Generating monthly summary for month:', month);
    const response = await axios.post(`${AGENT_API_URL}/monthly-summary`, {
      month,
    });
    return response.data as AgentResponse;
  } catch (error) {
    console.error('Error fetching AI response:', error);
    return { content: "Couldn't get a response from the agent." };
  }
};
