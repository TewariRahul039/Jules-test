```javascript
import React from 'react';
import './App.css';
import ChatWindow from './components/ChatWindow/ChatWindow';

function App() {
  return (
    <div className="App">
      {/*
        You could add a header or other layout elements here if you wanted.
        For example:
        <header className="App-header">
          <h1>E-commerce Chatbot</h1>
        </header>
      */}
      <ChatWindow />
    </div>
  );
}

export default App;
```
