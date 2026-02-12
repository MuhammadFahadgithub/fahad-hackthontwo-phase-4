import { useState, useRef, useEffect } from 'react';
import { Box, TextField, Button, Paper, Typography } from '@mui/material';

const ChatInterface = () => {
  const [inputValue, setInputValue] = useState('');
  const [messages, setMessages] = useState([]);
  const messagesEndRef = useRef(null);

  // Mock function to simulate sending a message to the backend
  const sendMessage = async (messageText) => {
    // Add user message to the chat
    const userMessage = { id: Date.now(), text: messageText, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);

    // Simulate API call to backend
    try {
      // In a real implementation, this would be an API call to the backend
      const response = await fetch('/api/v1/chat/message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: messageText }),
      });

      const data = await response.json();
      
      // Add bot response to the chat
      const botMessage = { 
        id: Date.now() + 1, 
        text: data.response, 
        sender: 'bot' 
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Add error message to the chat
      const errorMessage = { 
        id: Date.now() + 1, 
        text: 'Sorry, I encountered an error processing your request.', 
        sender: 'system' 
      };
      setMessages(prev => [...prev, errorMessage]);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputValue.trim() !== '') {
      sendMessage(inputValue);
      setInputValue('');
    }
  };

  // Scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <Box sx={{ width: '100%', maxWidth: '800px', margin: '0 auto', p: 2 }}>
      <Typography variant="h4" component="h1" gutterBottom align="center">
        Todo Chatbot
      </Typography>
      
      <Paper 
        elevation={3} 
        sx={{ 
          height: 400, 
          overflowY: 'auto', 
          mb: 2, 
          p: 2, 
          backgroundColor: '#f5f5f5' 
        }}
      >
        {messages.length === 0 ? (
          <Typography variant="body1" sx={{ textAlign: 'center', mt: 4, color: '#666' }}>
            Welcome! You can ask me to add, list, complete, or delete todos.
          </Typography>
        ) : (
          messages.map((message) => (
            <Box
              key={message.id}
              sx={{
                display: 'flex',
                justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start',
                mb: 1,
              }}
            >
              <Box
                sx={{
                  maxWidth: '70%',
                  p: 1,
                  borderRadius: 2,
                  backgroundColor:
                    message.sender === 'user'
                      ? '#007bff'
                      : message.sender === 'bot'
                      ? '#e9ecef'
                      : '#ffc107',
                  color: message.sender === 'user' ? 'white' : 'black',
                }}
              >
                {message.text}
              </Box>
            </Box>
          ))
        )}
        <div ref={messagesEndRef} />
      </Paper>
      
      <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '8px' }}>
        <TextField
          fullWidth
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Type your message here..."
          variant="outlined"
        />
        <Button type="submit" variant="contained" color="primary">
          Send
        </Button>
      </form>
    </Box>
  );
};

export default ChatInterface;