/**
 * API client service for the Todo Chatbot frontend
 */
class ApiService {
  constructor(baseURL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1') {
    this.baseURL = baseURL;
  }

  // Generic request method
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Todo-related methods
  async getTodos(params = {}) {
    const queryParams = new URLSearchParams(params).toString();
    const endpoint = queryParams ? `/todos?${queryParams}` : '/todos';
    return this.request(endpoint);
  }

  async createTodo(todoData) {
    return this.request('/todos', {
      method: 'POST',
      body: JSON.stringify(todoData),
    });
  }

  async getTodoById(id) {
    return this.request(`/todos/${id}`);
  }

  async updateTodo(id, todoData) {
    return this.request(`/todos/${id}`, {
      method: 'PUT',
      body: JSON.stringify(todoData),
    });
  }

  async deleteTodo(id) {
    return this.request(`/todos/${id}`, {
      method: 'DELETE',
    });
  }

  // Chat-related methods
  async sendChatMessage(messageData) {
    return this.request('/chat/message', {
      method: 'POST',
      body: JSON.stringify(messageData),
    });
  }
}

// Export a singleton instance
const apiService = new ApiService();
export default apiService;