content:
import React, { useState, useEffect } from 'react';
import './ChatWindow.css';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import { sendMessageToBot } from '../../services/api'; // Adjust path if needed

const ChatWindow = () => {
  const [messages, setMessages] = useState([
    { id: Date.now(), text: 'Hello! How can I help you today?', sender: 'bot', type: 'greeting' }
  ]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (text) => {
    const userMessage = {
      id: Date.now(), // Use timestamp for unique ID for user message
      text,
      sender: 'user',
      type: 'text'
    };
    setMessages(prevMessages => [...prevMessages, userMessage]);
    setIsLoading(true);

    try {
      const botResponse = await sendMessageToBot(text);
      // Ensure botResponse has a unique ID and sender is set correctly
      const botMessage = {
        ...botResponse,
        id: Date.now() + 1, // Ensure unique ID for bot message
        sender: 'bot'
      };
      setMessages(prevMessages => [...prevMessages, botMessage]);
    } catch (error) {
      // Error is already handled in sendMessageToBot, but you could add UI feedback here if needed
      console.error("Error in handleSendMessage:", error);
      // Optionally, display an error message in the chat
      setMessages(prevMessages => [...prevMessages, { id: Date.now() + 1, text: "Sorry, something went wrong.", sender: 'bot', type: 'error' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-window">
      <MessageList messages={messages} />
      <MessageInput onSendMessage={handleSendMessage} isLoading={isLoading} />
    </div>
  );
};

export default ChatWindow;
