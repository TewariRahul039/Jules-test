import React, { useState } from 'react';
import './MessageInput.css'; // To be created

const MessageInput = ({ onSendMessage }) => {
  const [text, setText] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (text.trim()) {
      onSendMessage(text.trim());
      setText('');
    }
  };

  return (
    <form className="message-input-form" onSubmit={handleSubmit}>
      <input
        className="message-input-field"
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Type a message..."
      />
      <button className="message-send-button" type="submit">Send</button>
    </form>
  );
};
export default MessageInput;
