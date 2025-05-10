import React, { createContext, useContext, useState } from 'react';

// Define the shape of a message
interface Message {
  role: 'user' | 'agent';
  content: string;
}

// Define the context value type
interface ChatContextType {
  messageHistory: Message[];
  addMessage: (message: Message) => void;
  clearHistory: () => void;
}

// Create the context
const ChatContext = createContext<ChatContextType | undefined>(undefined);

// Provider component
export const ChatProvider = ({ children }: { children: React.ReactNode }) => {
  const [messageHistory, setMessageHistory] = useState<Message[]>([]);

  // Function to add a message to the history
  const addMessage = (message: Message) => {
    setMessageHistory((prev) => [...prev, message]);
  };

  // Function to clear the message history
  const clearHistory = () => {
    setMessageHistory([]);
  };

  return (
    <ChatContext.Provider value={{ messageHistory, addMessage, clearHistory }}>
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
