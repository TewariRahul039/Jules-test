import React, { useState } from 'react';
import './ChatWindow.css'; // To be created
import MessageList from './MessageList'; // To be created
import MessageInput from './MessageInput'; // To be created

const ChatWindow = () => {
  const [messages, setMessages] = useState([
    // Initial welcome message from bot
    { id: 1, text: 'Hello! How can I help you today?', sender: 'bot' }
  ]);

  const handleSendMessage = (text) => {
    const newMessage = { id: messages.length + 1, text, sender: 'user' };
    // For now, just add user message. Bot response will be handled later.
    setMessages([...messages, newMessage]);
    // TODO: Send message to backend and get bot response
  };

  return (
    <div className="chat-window">
      <MessageList messages={messages} />
      <MessageInput onSendMessage={handleSendMessage} />
    </div>
  );
};
export default ChatWindow;
