import { useState } from 'react';
import { sendBudgetAgentPrompt, sendGoalAgentPrompt, type AgentResponse } from '../../api/endpoints';
import { ChatProvider, useChatContext } from './ChatContext';
import ChatFloatingButton from './ChatFloatingButton';
import arrow_up from '../../assets/arrow_up.svg';
import { useDataContext } from '../../api/DataContext';
import Markdown from 'react-markdown';
import './chat.css';
import budgy_icon from '../../assets/budgy_icon.svg';
import GoalAgentChat from './GoalAgentChat';
import BudgetAgentChat from './BudgetAgentChat';

const ChatComponent = () => {
  // Refetch the data after agent responses. TODO: Figure out a way to only do it when the agent has used a tool that modifies data.
  const [selectedTab, setSelectedTab] = useState<'goal' | 'budget'>('goal');
  const [chatOpen, setChatOpen] = useState(false); // State to control chat visibility

  const { goalsResponse, budgetsResponse } = useDataContext();
  const { goalAgentMessageHistory, addGoalAgentMessage, budgetAgentMessageHistory, addBudgetAgentMessage } = useChatContext();

  // GOAL AGENT STATE
  const [goalPrompt, setGoalPrompt] = useState(''); // State to hold the input value
  const [responseLoading, setResponseLoading] = useState(false);

  const handleAgentResponse = (agentResponse: AgentResponse) => {
    setResponseLoading(false);
    addGoalAgentMessage({ role: 'agent', content: agentResponse.content });
    goalsResponse.refetch(); // Refetch the goals data after receiving the agent's response
  };

  const handleSendPrompt = async () => {
    if (goalPrompt.trim() === '') {
      alert('Please enter a prompt.');
      return;
    }

    setGoalPrompt('');
    addGoalAgentMessage({ role: 'user', content: goalPrompt }); // Add the user's message to the history

    setResponseLoading(true);

    try {
      const agentResponse = await sendGoalAgentPrompt(goalPrompt);
      handleAgentResponse(agentResponse); // Update the response state with the agent's response
    } catch (error) {
      setResponseLoading(false);
      console.error('Error sending prompt:', error);
    }
  };

  const getWelcomeMessage = async () => {
    try {
      const agentResponse = await sendGoalAgentPrompt('/start');
      handleAgentResponse(agentResponse); // Update the response state with the agent's response
    } catch (error) {
      setResponseLoading(false);
      console.error('Error sending prompt:', error);
    }
  };

  const handleOpenChat = () => {
    if (goalAgentMessageHistory.length === 0) {
      getWelcomeMessage();
    }
    setChatOpen(true);
  };

  // BUDGET AGENT STATE
  const [budgetPrompt, setBudgetPrompt] = useState(''); // State to hold the input value
  const [budgetResponseLoading, setBudgetResponseLoading] = useState(false);

  const handleBudgetAgentResponse = (agentResponse: AgentResponse) => {
    setBudgetResponseLoading(false);
    addBudgetAgentMessage({ role: 'agent', content: agentResponse.content });
    budgetsResponse.refetch(); // Refetch the goals data after receiving the agent's response
  };

  const handleSendBudgetAgentPrompt = async () => {
    if (budgetPrompt.trim() === '') {
      alert('Please enter a prompt.');
      return;
    }

    setBudgetPrompt('');
    addBudgetAgentMessage({ role: 'user', content: budgetPrompt }); // Add the user's message to the history

    setBudgetResponseLoading(true);

    try {
      const agentResponse = await sendBudgetAgentPrompt(budgetPrompt);
      handleBudgetAgentResponse(agentResponse); // Update the response state with the agent's response
    } catch (error) {
      setBudgetResponseLoading(false);
      console.error('Error sending prompt:', error);
    }
  };

  const getBudgetAgentWelcomeMessage = async () => {
    try {
      const agentResponse = await sendBudgetAgentPrompt('/start');
      handleBudgetAgentResponse(agentResponse); // Update the response state with the agent's response
    } catch (error) {
      setBudgetResponseLoading(false);
      console.error('Error sending prompt:', error);
    }
  };

const handleSelectTab = (tab: "goal" | "budget") => {
  if (tab === 'budget' && budgetAgentMessageHistory.length === 0) {
    getBudgetAgentWelcomeMessage();
  }
  setSelectedTab(tab);
}

  return (
    <div>
      <div className="chat-floating-button-container">
        <ChatFloatingButton onClick={handleOpenChat} />
      </div>

      {chatOpen && (
        <div className="chat-container">
          <div className="buttons-container">
            <button
              className="small-button"
              onClick={() => setChatOpen((prev) => false)}
            >
              Close
            </button>

            <div className="tabs">
              <button className="small-button" onClick={() => handleSelectTab('goal')}>Set goals</button>

              <button className="small-button" onClick={() => handleSelectTab('budget')}>Set budget</button>
            </div>
          </div>

          {selectedTab === 'goal' && (
            <GoalAgentChat {...{responseLoading, handleSendPrompt, goalPrompt, setGoalPrompt}} />
          )}
          {selectedTab === 'budget' && (
            <BudgetAgentChat {...{budgetResponseLoading, handleSendBudgetAgentPrompt, budgetPrompt, setBudgetPrompt}} />
          )}
        </div>
      )}
    </div>
  );
};

const Chat = () => {
  return (
    <ChatProvider>
      <ChatComponent />
    </ChatProvider>
  );
};

export default Chat;
