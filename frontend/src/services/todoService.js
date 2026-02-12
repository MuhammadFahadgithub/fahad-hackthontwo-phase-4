/**
 * Todo service for connecting the web UI to the backend API
 */

import apiService from './api';

class TodoService {
  constructor() {
    // Any initialization code would go here
  }

  async getTodos(filters = {}) {
    try {
      const response = await apiService.getTodos(filters);
      return response;
    } catch (error) {
      console.error('Error fetching todos:', error);
      throw error;
    }
  }

  async createTodo(todoData) {
    try {
      const response = await apiService.createTodo(todoData);
      return response;
    } catch (error) {
      console.error('Error creating todo:', error);
      throw error;
    }
  }

  async updateTodo(id, todoData) {
    try {
      const response = await apiService.updateTodo(id, todoData);
      return response;
    } catch (error) {
      console.error('Error updating todo:', error);
      throw error;
    }
  }

  async deleteTodo(id) {
    try {
      const response = await apiService.deleteTodo(id);
      return response;
    } catch (error) {
      console.error('Error deleting todo:', error);
      throw error;
    }
  }
}

const todoService = new TodoService();
export default todoService;