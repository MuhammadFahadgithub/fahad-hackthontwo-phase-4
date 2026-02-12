// frontend/src/components/chat/ChatInterface.jsx

import React, { useState, useRef, useEffect } from 'react';
import ApiService from '../../services/api';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const messagesEndRef = useRef(null);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message to the chat
    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Send message to backend
      const response = await ApiService.sendMessage(inputValue, conversationId);
      
      // Update conversation ID if it was returned
      if (response.conversation_id && !conversationId) {
        setConversationId(response.conversation_id);
      }

      // Add AI response to the chat
      const aiMessage = {
        id: Date.now() + 1,
        text: response.response,
        sender: 'ai',
        timestamp: response.timestamp,
        taskOperations: response.task_operations
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Add error message to the chat
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error processing your request. Please try again.',
        sender: 'system',
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const formatTaskOperations = (operations) => {
    if (!operations || operations.length === 0) return null;
    
    return (
      <div className="task-operations">
        {operations.map((op, index) => (
          <div key={index} className={`operation-${op.status}`}>
            {op.status === 'success' ? '✅' : '❌'} {op.message || `${op.operation} ${op.status}`}
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <h3>Hello! I'm your AI Todo Assistant.</h3>
            <p>You can ask me to:</p>
            <ul>
              <li>Add tasks (e.g., "Add a task to buy groceries")</li>
              <li>List tasks (e.g., "Show me my tasks")</li>
              <li>Complete tasks (e.g., "Complete task 1")</li>
              <li>Delete tasks (e.g., "Delete the meeting task")</li>
              <li>Update tasks (e.g., "Change task 1 to buy milk instead of bread")</li>
            </ul>
          </div>
        ) : (
          messages.map((message) => (
            <div 
              key={message.id} 
              className={`message ${message.sender}-message`}
            >
              <div className="message-content">
                <span className="message-text">{message.text}</span>
                {message.taskOperations && formatTaskOperations(message.taskOperations)}
              </div>
              <span className="timestamp">
                {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </span>
            </div>
          ))
        )}
        {isLoading && (
          <div className="message ai-message">
            <div className="message-content">
              <span className="typing-indicator">AI is thinking...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="chat-input-form">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Type your message here..."
          disabled={isLoading}
          className="chat-input"
        />
        <button type="submit" disabled={!inputValue.trim() || isLoading} className="send-button">
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;