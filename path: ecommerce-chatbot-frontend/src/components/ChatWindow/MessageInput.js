content:
import React, { useState } from 'react';
import './MessageInput.css';

const MessageInput = ({ onSendMessage, isLoading }) => {
  const [text, setText] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (text.trim() && !isLoading) {
      onSendMessage(text.trim());
      setText('');
    }
  };

  return (
    <form className="message-input" onSubmit={handleSubmit}>
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder={isLoading ? "Bot is thinking..." : "Type a message..."}
        disabled={isLoading}
      />
      <button type="submit" disabled={isLoading}>
        {isLoading ? '...' : 'Send'}
      </button>
    </form>
  );
};

export default MessageInput;
