import { useState } from 'react';
import { sendGoalAgentPrompt } from '../../api/endpoints';
import { ChatProvider, useChatContext } from './ChatContext';

const ChatComponent = () => {
  const { messageHistory, addMessage } = useChatContext();

  const [prompt, setPrompt] = useState(''); // State to hold the input value

  const handleSendPrompt = async () => {
    if (prompt.trim() === '') {
      alert('Please enter a prompt.');
      return;
    }

    addMessage({ role: 'user', content: prompt }); // Add the user's message to the history

    try {
      const agentResponse = await sendGoalAgentPrompt(prompt);
      addMessage({ role: 'agent', content: agentResponse.content }); // Update the response state with the agent's response
    } catch (error) {
      console.error('Error sending prompt:', error);
    }
  };

  return (
    <div className="chat-container">
      <h2>Chat with Budgy</h2>
      <div className="input-container">
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)} // Update the prompt state on input change
          placeholder="Type your prompt here..."
        />
        <button onClick={handleSendPrompt}>Send</button>
      </div>

      {messageHistory.map((message, index) => (
        <div key={index}>
          <h3>{message.role}</h3>
          <p>{message.content}</p>
        </div>
      ))}
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
