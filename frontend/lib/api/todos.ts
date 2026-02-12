/**
 * API client functions for todo operations.
 *
 * Handles all todo CRUD operations with authentication.
 * Constitution Principle II: JWT authentication on all requests
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface Todo {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  user_id: number;
  created_at: string;
  updated_at: string;
}

export interface TodoCreate {
  title: string;
  description?: string;
  completed?: boolean;
}

export interface TodoUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
}

function getAuthToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("auth_token");
}

async function apiRequest(
  endpoint: string,
  options: RequestInit = {}
): Promise<Response> {
  const token = getAuthToken();

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    },
  });

  if (response.status === 401) {
    // Redirect to login if unauthorized
    window.location.href = "/login";
    throw new Error("Unauthorized");
  }

  return response;
}

export async function fetchTodos(): Promise<Todo[]> {
  const response = await apiRequest("/api/v1/todos");

  if (!response.ok) {
    throw new Error("Failed to fetch todos");
  }

  return response.json();
}

export async function createTodo(data: TodoCreate): Promise<Todo> {
  const response = await apiRequest("/api/v1/todos", {
    method: "POST",
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to create todo");
  }

  return response.json();
}

export async function updateTodo(id: number, data: TodoUpdate): Promise<Todo> {
  const response = await apiRequest(`/api/v1/todos/${id}`, {
    method: "PUT",
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to update todo");
  }

  return response.json();
}

export async function deleteTodo(id: number): Promise<void> {
  const response = await apiRequest(`/api/v1/todos/${id}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to delete todo");
  }
}

export async function toggleTodoCompletion(id: number): Promise<Todo> {
  const response = await apiRequest(`/api/v1/todos/${id}/toggle`, {
    method: "PATCH",
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to toggle todo completion");
  }

  return response.json();
}
