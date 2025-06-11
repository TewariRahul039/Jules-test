content:
// This file will contain the logic for interacting with the chatbot API.
// For now, it can remain empty or contain a placeholder function.

export const sendMessageToBot = async (message) => {
  // Placeholder implementation - replace with actual API call
  console.log("Sending message to backend:", message);
  // Simulate a delay and a generic response for now
  await new Promise(resolve => setTimeout(resolve, 500));
  if (message.toLowerCase().includes("hello")) {
    return { text: "Hello! How can I assist you today?", sender: "bot" };
  } else if (message.toLowerCase().includes("bye")) {
    return { text: "Goodbye! Have a great day.", sender: "bot" };
  } else if (message.toLowerCase().includes("help")) {
    return { text: "You can ask me to search for products (e.g., 'search for laptops'), or say hello/goodbye. How can I assist?", sender: "bot" };
  } else if (message.toLowerCase().startsWith("search for ") || message.toLowerCase().startsWith("find ")) {
    const query = message.substring(message.indexOf(" ") + 1);
    return { type: 'product_list', products: [], text: `Searching for "${query}"... (This is a mock response, backend integration needed)`, sender: 'bot' };
  }
  return { text: "Sorry, I didn't understand that. You can ask me to 'search for [product]' or ask for 'help'.", sender: 'bot' };
};
