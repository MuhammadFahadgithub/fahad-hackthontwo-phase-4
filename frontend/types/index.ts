/**
 * Shared TypeScript types for the application.
 *
 * Defines interfaces for API responses and data models.
 */

// User Types
export interface User {
  id: number;
  email: string;
  name: string;
  email_verified: boolean;
  created_at: string;
}

// Authentication Types
export interface AuthResponse {
  user: User;
  token: string;
  expires_at: string;
}

export interface SignUpData {
  email: string;
  name: string;
  password: string;
}

export interface LoginData {
  email: string;
  password: string;
}

// Session Types
export interface Session {
  user: User;
  token: string;
  expiresAt: string;
}

// API Error Types
export interface ApiError {
  detail: string;
  errors?: Array<{
    field?: string;
    message: string;
    code?: string;
  }>;
}

// Task Types (for future use)
export interface Task {
  id: number;
  user_id: number;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
  completed?: boolean;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
}

// Pagination Types
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  skip: number;
  limit: number;
  has_more: boolean;
}
