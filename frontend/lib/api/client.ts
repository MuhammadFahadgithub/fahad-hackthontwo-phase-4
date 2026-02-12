/**
 * API client for backend communication.
 *
 * Provides base API client with automatic JWT token attachment.
 * Constitution Principle II: Authentication & JWT Security
 * Constitution Principle III: User Identity & Isolation
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Get authentication token from storage.
 *
 * Constitution SR-002: JWT sent in Authorization: Bearer <token> header
 */
function getAuthToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("auth_token");
}

/**
 * Make authenticated API request.
 *
 * Automatically attaches JWT token to all requests.
 * Handles 401 responses by redirecting to login.
 *
 * @param endpoint - API endpoint (e.g., "/api/v1/todos")
 * @param options - Fetch options
 * @returns Response object
 */
export async function apiRequest(
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

  // Constitution SR-004: Invalid/missing tokens return 401
  if (response.status === 401) {
    // Token invalid or expired - redirect to login
    if (typeof window !== "undefined") {
      window.location.href = "/login";
    }
    throw new Error("Unauthorized");
  }

  return response;
}

/**
 * Make GET request.
 */
export async function apiGet<T>(endpoint: string): Promise<T> {
  const response = await apiRequest(endpoint, { method: "GET" });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "API request failed");
  }

  return response.json();
}

/**
 * Make POST request.
 */
export async function apiPost<T>(endpoint: string, data: any): Promise<T> {
  const response = await apiRequest(endpoint, {
    method: "POST",
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "API request failed");
  }

  return response.json();
}

/**
 * Make PUT request.
 */
export async function apiPut<T>(endpoint: string, data: any): Promise<T> {
  const response = await apiRequest(endpoint, {
    method: "PUT",
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "API request failed");
  }

  return response.json();
}

/**
 * Make DELETE request.
 */
export async function apiDelete(endpoint: string): Promise<void> {
  const response = await apiRequest(endpoint, { method: "DELETE" });

  if (!response.ok && response.status !== 204) {
    const error = await response.json();
    throw new Error(error.detail || "API request failed");
  }
}
