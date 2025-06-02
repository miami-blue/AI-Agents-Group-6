import { useChatContext } from './ChatContext';
import arrow_up from '../../assets/arrow_up.svg';
import Markdown from 'react-markdown';
import './chat.css';
import budgy_icon from '../../assets/budgy_icon.svg';

interface Props {
  budgetResponseLoading: boolean;
  handleSendBudgetAgentPrompt: () => Promise<void>;
  budgetPrompt: string;
  setBudgetPrompt: React.Dispatch<React.SetStateAction<string>>;
}

const BudgetAgentChat = ({
  budgetResponseLoading,
  handleSendBudgetAgentPrompt,
  budgetPrompt,
  setBudgetPrompt,
}: Props) => {
  const { budgetAgentMessageHistory } = useChatContext();
  return (
    <div className="chat-flow-container">
      <div className="chat-flow">
        <div className="chat-flow-scroll">
          {budgetAgentMessageHistory.map((message, index) => (
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

          {budgetResponseLoading && <div>I&apos;m thinking, hold on tight...</div>}
        </div>
        <div className="chat-input-container">
          <input
            type="text"
            value={budgetPrompt}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                handleSendBudgetAgentPrompt(); // Call the send function when Enter is pressed
              }
            }}
            onChange={(e) => setBudgetPrompt(e.target.value)} // Update the budgetPrompt state on input change
            placeholder="Type your prompt here..."
          />

          <button onClick={handleSendBudgetAgentPrompt}>
            {<img src={arrow_up} width={16} alt="Send" />}
          </button>
        </div>
      </div>
    </div>
  );
};

export default BudgetAgentChat;
