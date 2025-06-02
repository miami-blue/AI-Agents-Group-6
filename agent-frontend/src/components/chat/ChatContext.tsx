import React, { createContext, useContext, useState } from 'react';

// Define the shape of a message
interface Message {
  role: 'user' | 'agent';
  content: string;
}

// Define the context value type
interface ChatContextType {
  goalAgentMessageHistory: Message[];
  addGoalAgentMessage: (message: Message) => void;
  budgetAgentMessageHistory: Message[];
  addBudgetAgentMessage: (message: Message) => void;
  clearHistory: () => void;
}

// Create the context
const ChatContext = createContext<ChatContextType | undefined>(undefined);

// Provider component
export const ChatProvider = ({ children }: { children: React.ReactNode }) => {
  const [goalAgentMessageHistory, setGoalAgentMessageHistory] = useState<Message[]>([]);
  const [budgetAgentMessageHistory, setBudgetAgentMessageHistory] = useState<Message[]>([]);

  // Functions to add a message to the history
  const addGoalAgentMessage = (message: Message) => {
    setGoalAgentMessageHistory((prev) => [...prev, message]);
  };
  const addBudgetAgentMessage = (message: Message) => {
    setBudgetAgentMessageHistory((prev) => [...prev, message]);
  };

  // Function to clear the message history
  const clearHistory = () => {
    setGoalAgentMessageHistory([]);
    setBudgetAgentMessageHistory([]);
  };

  return (
    <ChatContext.Provider value={{ goalAgentMessageHistory, addGoalAgentMessage, budgetAgentMessageHistory, addBudgetAgentMessage, clearHistory }}>
      {children}
    </ChatContext.Provider>
  );
};

// Custom hook to use the ChatContext
export const useChatContext = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};
