import React from 'react';
import './MessageItem.css'; // To be created

const MessageItem = ({ message }) => {
  const { text, sender } = message;
  return (
    <div className={`message-item ${sender}`}>
      <div className="message-content">
        <p>{text}</p>
      </div>
    </div>
  );
};
export default MessageItem;
