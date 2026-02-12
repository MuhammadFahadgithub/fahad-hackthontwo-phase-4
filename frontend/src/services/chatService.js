/**
 * Chat service for connecting the chat interface to the backend API
 */

import apiService from '../services/api';

class ChatService {
  constructor() {
    // Any initialization code would go here
  }

  async sendMessage(message, context = null) {
    try {
      const messageData = {
        message,
        context: context || {}
      };

      const response = await apiService.sendChatMessage(messageData);
      return response;
    } catch (error) {
      console.error('Error sending chat message:', error);
      throw error;
    }
  }

  // Method to process natural language commands
  async processNaturalLanguageCommand(command, userId, conversationId = null) {
    // This would typically involve more sophisticated processing
    // For now, we'll just send it to the backend
    const context = {
      user_id: userId,
      conversation_id: conversationId
    };

    return this.sendMessage(command, context);
  }
}

const chatService = new ChatService();
export default chatService;