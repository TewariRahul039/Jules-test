content:
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const sendMessageToBot = async (messageText) => {
  try {
    const response = await apiClient.post('/chatbot', { message: messageText });
    return response.data; // This should be the bot's response object
  } catch (error) {
    console.error("Error sending message to bot:", error);
    // Return a structured error message for the chat
    return {
      type: 'error',
      text: 'Sorry, I encountered an error. Please try again later.',
      sender: 'bot'
    };
  }
};
