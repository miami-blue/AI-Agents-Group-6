import { useState } from 'react';
import { sendGoalAgentPrompt, type AgentResponse } from '../../api/endpoints';
import { ChatProvider, useChatContext } from './ChatContext';
import ChatFloatingButton from './ChatFloatingButton';
import arrow_up from '../../assets/arrow_up.svg';
import { useDataContext } from '../../api/DataContext';
import Markdown from 'react-markdown';

const ChatComponent = () => {
  // Refetch the data after agent responses. TODO: Figure out a way to only do it when the agent has used a tool that modifies data.
  const { goalsResponse } = useDataContext();

  const { messageHistory, addMessage } = useChatContext();

  const [prompt, setPrompt] = useState(''); // State to hold the input value
  const [chatOpen, setChatOpen] = useState(false); // State to control chat visibility
  const [responseLoading, setResponseLoading] = useState(false);

  const handleAgentResponse = (agentResponse: AgentResponse) => {
    setResponseLoading(false);
    addMessage({ role: 'agent', content: agentResponse.content });
    goalsResponse.refetch(); // Refetch the goals data after receiving the agent's response
  };

  const handleSendPrompt = async () => {
    if (prompt.trim() === '') {
      alert('Please enter a prompt.');
      return;
    }

    setPrompt('');
    addMessage({ role: 'user', content: prompt }); // Add the user's message to the history

    setResponseLoading(true);

    try {
      const agentResponse = await sendGoalAgentPrompt(prompt);
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
    if (messageHistory.length === 0) {
      getWelcomeMessage();
    }
    setChatOpen(true);
  };

  return (
    <div>
      <div className="chat-floating-button-container">
        <ChatFloatingButton onClick={handleOpenChat} />
      </div>

      {chatOpen && (
        <div className="chat-container">
          <button
            className="small-button"
            onClick={() => setChatOpen((prev) => false)}
          >
            Close
          </button>
          <div className="chat-flow-container">
            <div className="chat-flow">
              <div className="chat-flow-scroll">
                {messageHistory.map((message, index) => (
                  <div key={index} className="chat-item-container">
                    <div className={`chat-item ${message.role}`}>
                      {message.role === 'agent' && <b>Budgy </b>}
                      <Markdown children={message.content} />
                    </div>
                  </div>
                ))}

                {responseLoading && (
                  <div>I&apos;m thinking, hold on tight...</div>
                )}
              </div>
              <div className="chat-input-container">
                <input
                  type="text"
                  value={prompt}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') {
                      handleSendPrompt(); // Call the send function when Enter is pressed
                    }
                  }}
                  onChange={(e) => setPrompt(e.target.value)} // Update the prompt state on input change
                  placeholder="Type your prompt here..."
                />

                <button onClick={handleSendPrompt}>
                  {<img src={arrow_up} width={16} alt="Send" />}
                </button>
              </div>
            </div>
          </div>
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
