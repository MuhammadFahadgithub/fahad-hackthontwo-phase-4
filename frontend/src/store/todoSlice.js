import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import apiService from '../services/api';

// Async thunks for todos
export const fetchTodos = createAsyncThunk(
  'todos/fetchTodos',
  async ({ status = null, limit = 100, offset = 0 } = {}) => {
    const params = {};
    if (status) params.status = status;
    if (limit) params.limit = limit;
    if (offset) params.offset = offset;

    const response = await apiService.getTodos(params);
    return response;
  }
);

export const addTodo = createAsyncThunk(
  'todos/addTodo',
  async (todoData) => {
    const response = await apiService.createTodo(todoData);
    return response;
  }
);

export const updateTodo = createAsyncThunk(
  'todos/updateTodo',
  async ({ id, todoData }) => {
    const response = await apiService.updateTodo(id, todoData);
    return response;
  }
);

export const deleteTodo = createAsyncThunk(
  'todos/deleteTodo',
  async (id) => {
    await apiService.deleteTodo(id);
    return id;
  }
);

// Async thunks for chat
export const sendChatMessage = createAsyncThunk(
  'chat/sendChatMessage',
  async (messageData) => {
    const response = await apiService.sendChatMessage(messageData);
    return response;
  }
);

// Initial state
const initialState = {
  todos: [],
  status: 'idle',
  error: null,
  chatMessages: [],
  chatStatus: 'idle',
  chatError: null,
};

// Slice
const todoSlice = createSlice({
  name: 'todos',
  initialState,
  reducers: {
    addMessage: (state, action) => {
      state.chatMessages.push(action.payload);
    },
    clearMessages: (state) => {
      state.chatMessages = [];
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch todos
      .addCase(fetchTodos.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(fetchTodos.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.todos = action.payload;
      })
      .addCase(fetchTodos.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message;
      })
      // Add todo
      .addCase(addTodo.fulfilled, (state, action) => {
        state.todos.push(action.payload);
      })
      // Update todo
      .addCase(updateTodo.fulfilled, (state, action) => {
        const index = state.todos.findIndex(todo => todo.id === action.payload.id);
        if (index !== -1) {
          state.todos[index] = action.payload;
        }
      })
      // Delete todo
      .addCase(deleteTodo.fulfilled, (state, action) => {
        state.todos = state.todos.filter(todo => todo.id !== action.payload);
      })
      // Send chat message
      .addCase(sendChatMessage.pending, (state) => {
        state.chatStatus = 'loading';
      })
      .addCase(sendChatMessage.fulfilled, (state, action) => {
        state.chatStatus = 'succeeded';
        state.chatMessages.push({
          id: Date.now(),
          text: action.payload.response,
          sender: 'bot'
        });
      })
      .addCase(sendChatMessage.rejected, (state, action) => {
        state.chatStatus = 'failed';
        state.chatError = action.error.message;
      });
  },
});

export const { addMessage, clearMessages } = todoSlice.actions;
export default todoSlice.reducer;