import { useChatContext } from './ChatContext';
import arrow_up from '../../assets/arrow_up.svg';
import Markdown from 'react-markdown';
import './chat.css';
import budgy_icon from '../../assets/budgy_icon.svg';

interface Props {
  responseLoading: boolean;
  handleSendPrompt: () => Promise<void>;
  goalPrompt: string;
  setGoalPrompt: React.Dispatch<React.SetStateAction<string>>;
}

const GoalAgentChat = ({
  responseLoading,
  handleSendPrompt,
  goalPrompt,
  setGoalPrompt,
}: Props) => {
  const { goalAgentMessageHistory } = useChatContext();
  return (
    <div className="chat-flow-container">
      <div className="chat-flow">
        <div className="chat-flow-scroll">
          {goalAgentMessageHistory.map((message, index) => (
            <div key={index} className="chat-item-container">
              <div className={`chat-item ${message.role}`}>
                {message.role === 'agent' && (
                  <div className="budgy-chat-item-header">
                    <div className="budgy-avatar-container">
                      <img
                        src={budgy_icon}
                        alt="Budgy Icon"
                        width={24}
                        height={24}
                      ></img>
                    </div>

                    <b>Budgy</b>
                  </div>
                )}
                <Markdown children={message.content} />
              </div>
            </div>
          ))}

          {responseLoading && <div>I&apos;m thinking, hold on tight...</div>}
        </div>
        <div className="chat-input-container">
          <input
            type="text"
            value={goalPrompt}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                handleSendPrompt(); // Call the send function when Enter is pressed
              }
            }}
            onChange={(e) => setGoalPrompt(e.target.value)} // Update the goalPrompt state on input change
            placeholder="Type your prompt here..."
          />

          <button onClick={handleSendPrompt}>
            {<img src={arrow_up} width={16} alt="Send" />}
          </button>
        </div>
      </div>
    </div>
  );
};

export default GoalAgentChat;
