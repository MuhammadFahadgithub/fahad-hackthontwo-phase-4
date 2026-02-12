---
name: better-auth-integration
description: |
  Comprehensive guide for implementing Better Auth in Next.js applications,
  including JWT token generation, session management, authentication flows,
  and integration with FastAPI backends.

proficiency_level: "B2"
category: "Authentication"
use_when: |
  - Setting up Better Auth in Next.js
  - Implementing signup/login flows
  - Managing JWT tokens and sessions
  - Integrating with FastAPI backend
  - Implementing protected routes
  - Handling authentication state
  - Troubleshooting auth issues
---

# Better Auth Integration Guide

## Role
You are an authentication specialist focused on implementing Better Auth in Next.js applications with FastAPI backend integration.

## Better Auth Overview

### What is Better Auth?
- **Modern Authentication**: Type-safe authentication library for Next.js
- **JWT-Based**: Uses JSON Web Tokens for stateless authentication
- **Database Agnostic**: Works with PostgreSQL, MySQL, SQLite
- **Built-in Features**: Email/password, OAuth, magic links, 2FA
- **Type-Safe**: Full TypeScript support

### Key Features
- ✅ Email/password authentication
- ✅ JWT token generation and verification
- ✅ Session management
- ✅ OAuth providers (Google, GitHub, etc.)
- ✅ Magic link authentication
- ✅ Two-factor authentication
- ✅ Password reset flows
- ✅ Email verification

## Installation and Setup

### Install Better Auth

```bash
cd frontend
npm install better-auth
```

### Database Setup

**Create Auth Tables:**
```sql
-- Better Auth requires these tables
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    name VARCHAR(255),
    image VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    provider VARCHAR(255) NOT NULL,
    provider_account_id VARCHAR(255) NOT NULL,
    access_token TEXT,
    refresh_token TEXT,
    expires_at BIGINT,
    token_type VARCHAR(255),
    scope VARCHAR(255),
    id_token TEXT,
    session_state VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(provider, provider_account_id)
);

CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    expires TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE verification_tokens (
    identifier VARCHAR(255) NOT NULL,
    token VARCHAR(255) UNIQUE NOT NULL,
    expires TIMESTAMP NOT NULL,
    PRIMARY KEY (identifier, token)
);
```

### Better Auth Configuration

**Create Auth Configuration:**
```typescript
// lib/auth/config.ts
import { betterAuth } from "better-auth";
import { Pool } from "pg";

// Database connection
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

export const auth = betterAuth({
  // Database configuration
  database: {
    provider: "postgresql",
    pool: pool,
  },

  // Email/password authentication
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // Set to true in production
    minPasswordLength: 8,
  },

  // JWT configuration
  jwt: {
    secret: process.env.BETTER_AUTH_SECRET!,
    expiresIn: "7d", // Token expiration
  },

  // Session configuration
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days in seconds
    updateAge: 60 * 60 * 24, // Update session every 24 hours
  },

  // Base URL
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3000",

  // Callbacks
  callbacks: {
    async signIn({ user, account }) {
      // Custom logic on sign in
      console.log(`User ${user.email} signed in`);
      return true;
    },
    async signOut({ session }) {
      // Custom logic on sign out
      console.log(`Session ${session.id} signed out`);
    },
  },
});

export type Auth = typeof auth;
```

### API Route Handler

**Create Auth API Route:**
```typescript
// app/api/auth/[...all]/route.ts
import { auth } from "@/lib/auth/config";
import { toNextJsHandler } from "better-auth/next-js";

export const { GET, POST } = toNextJsHandler(auth);
```

## Authentication Flows

### Sign Up Flow

**Sign Up Component:**
```typescript
// components/auth/SignUpForm.tsx
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { signUp } from "@/lib/auth/client";

export function SignUpForm() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const result = await signUp({
        email,
        password,
        name,
      });

      if (result.error) {
        setError(result.error.message);
        return;
      }

      // Redirect to dashboard on success
      router.push("/dashboard");
    } catch (err) {
      setError("An unexpected error occurred");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="name" className="block text-sm font-medium">
          Name
        </label>
        <input
          id="name"
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
        />
      </div>

      <div>
        <label htmlFor="email" className="block text-sm font-medium">
          Email
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
        />
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium">
          Password
        </label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          minLength={8}
          className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
        />
      </div>

      {error && (
        <div className="text-red-600 text-sm">{error}</div>
      )}

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? "Signing up..." : "Sign Up"}
      </button>
    </form>
  );
}
```

### Sign In Flow

**Sign In Component:**
```typescript
// components/auth/SignInForm.tsx
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { signIn } from "@/lib/auth/client";

export function SignInForm() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const result = await signIn({
        email,
        password,
      });

      if (result.error) {
        setError(result.error.message);
        return;
      }

      // Redirect to dashboard on success
      router.push("/dashboard");
    } catch (err) {
      setError("An unexpected error occurred");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="email" className="block text-sm font-medium">
          Email
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
        />
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium">
          Password
        </label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
        />
      </div>

      {error && (
        <div className="text-red-600 text-sm">{error}</div>
      )}

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? "Signing in..." : "Sign In"}
      </button>
    </form>
  );
}
```

### Auth Client Functions

**Create Auth Client:**
```typescript
// lib/auth/client.ts
import { createAuthClient } from "better-auth/client";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_AUTH_URL || "http://localhost:3000",
});

export const signUp = authClient.signUp;
export const signIn = authClient.signIn;
export const signOut = authClient.signOut;
export const getSession = authClient.getSession;
export const useSession = authClient.useSession;
```

## Session Management

### Auth Context Provider

**Create Auth Context:**
```typescript
// lib/auth/AuthProvider.tsx
"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { getSession } from "./client";

interface User {
  id: number;
  email: string;
  name: string | null;
  emailVerified: boolean;
}

interface Session {
  user: User;
  token: string;
  expiresAt: string;
}

interface AuthContextType {
  session: Session | null;
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  refreshSession: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [session, setSession] = useState<Session | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const refreshSession = async () => {
    try {
      const result = await getSession();
      if (result.data) {
        setSession(result.data);
      } else {
        setSession(null);
      }
    } catch (error) {
      console.error("Failed to refresh session:", error);
      setSession(null);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    refreshSession();
  }, []);

  const value: AuthContextType = {
    session,
    user: session?.user || null,
    token: session?.token || null,
    isAuthenticated: !!session,
    isLoading,
    refreshSession,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
```

**Add Provider to Layout:**
```typescript
// app/layout.tsx
import { AuthProvider } from "@/lib/auth/AuthProvider";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}
```

## Protected Routes

### Middleware Approach

**Create Auth Middleware:**
```typescript
// middleware.ts
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { auth } from "@/lib/auth/config";

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Public routes that don't require authentication
  const publicRoutes = ["/", "/login", "/signup", "/api/auth"];
  const isPublicRoute = publicRoutes.some((route) =>
    pathname.startsWith(route)
  );

  if (isPublicRoute) {
    return NextResponse.next();
  }

  // Check authentication
  const session = await auth.api.getSession({
    headers: request.headers,
  });

  if (!session) {
    // Redirect to login if not authenticated
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("callbackUrl", pathname);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     */
    "/((?!_next/static|_next/image|favicon.ico|public).*)",
  ],
};
```

### Component-Level Protection

**Protected Component Wrapper:**
```typescript
// components/auth/ProtectedRoute.tsx
"use client";

import { useAuth } from "@/lib/auth/AuthProvider";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push("/login");
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!isAuthenticated) {
    return null;
  }

  return <>{children}</>;
}
```

**Usage:**
```typescript
// app/dashboard/page.tsx
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <div>
        <h1>Dashboard</h1>
        {/* Protected content */}
      </div>
    </ProtectedRoute>
  );
}
```

## JWT Token Integration with FastAPI

### Extracting JWT Token

**API Client with Token:**
```typescript
// lib/api/client.ts
import { useAuth } from "@/lib/auth/AuthProvider";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function apiRequest(
  endpoint: string,
  options: RequestInit = {}
) {
  const token = localStorage.getItem("auth_token"); // Or get from context

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    },
  });

  if (response.status === 401) {
    // Token expired or invalid
    window.location.href = "/login";
    throw new Error("Unauthorized");
  }

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "API request failed");
  }

  return response;
}

// Todo API functions
export async function getTodos() {
  const response = await apiRequest("/api/v1/todos");
  return response.json();
}

export async function createTodo(data: { title: string; description?: string }) {
  const response = await apiRequest("/api/v1/todos", {
    method: "POST",
    body: JSON.stringify(data),
  });
  return response.json();
}
```

### Using Auth Hook in Components

**Component with API Calls:**
```typescript
// components/TodoList.tsx
"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/lib/auth/AuthProvider";
import { getTodos } from "@/lib/api/client";

interface Todo {
  id: number;
  title: string;
  completed: boolean;
}

export function TodoList() {
  const { token, isAuthenticated } = useAuth();
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!isAuthenticated) return;

    async function fetchTodos() {
      try {
        const data = await getTodos();
        setTodos(data);
      } catch (err) {
        setError("Failed to load todos");
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    fetchTodos();
  }, [isAuthenticated]);

  if (!isAuthenticated) {
    return <div>Please log in to view todos</div>;
  }

  if (loading) {
    return <div>Loading todos...</div>;
  }

  if (error) {
    return <div className="text-red-600">{error}</div>;
  }

  return (
    <div>
      <h2>My Todos</h2>
      <ul>
        {todos.map((todo) => (
          <li key={todo.id}>{todo.title}</li>
        ))}
      </ul>
    </div>
  );
}
```

## Password Reset Flow

**Request Password Reset:**
```typescript
// lib/auth/password-reset.ts
export async function requestPasswordReset(email: string) {
  const response = await fetch("/api/auth/password-reset/request", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email }),
  });

  if (!response.ok) {
    throw new Error("Failed to request password reset");
  }

  return response.json();
}

export async function resetPassword(token: string, newPassword: string) {
  const response = await fetch("/api/auth/password-reset/confirm", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ token, newPassword }),
  });

  if (!response.ok) {
    throw new Error("Failed to reset password");
  }

  return response.json();
}
```

**Password Reset Form:**
```typescript
// components/auth/PasswordResetForm.tsx
"use client";

import { useState } from "react";
import { requestPasswordReset } from "@/lib/auth/password-reset";

export function PasswordResetForm() {
  const [email, setEmail] = useState("");
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await requestPasswordReset(email);
      setSuccess(true);
    } catch (err) {
      setError("Failed to send reset email");
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="text-green-600">
        Password reset email sent! Check your inbox.
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="email" className="block text-sm font-medium">
          Email
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
        />
      </div>

      {error && <div className="text-red-600 text-sm">{error}</div>}

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? "Sending..." : "Send Reset Email"}
      </button>
    </form>
  );
}
```

## OAuth Integration

**Add OAuth Providers:**
```typescript
// lib/auth/config.ts
import { betterAuth } from "better-auth";
import { google, github } from "better-auth/providers";

export const auth = betterAuth({
  // ... other config

  // OAuth providers
  providers: [
    google({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
    github({
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    }),
  ],
});
```

**OAuth Sign In Buttons:**
```typescript
// components/auth/OAuthButtons.tsx
"use client";

import { signIn } from "@/lib/auth/client";

export function OAuthButtons() {
  const handleGoogleSignIn = async () => {
    await signIn({ provider: "google" });
  };

  const handleGitHubSignIn = async () => {
    await signIn({ provider: "github" });
  };

  return (
    <div className="space-y-2">
      <button
        onClick={handleGoogleSignIn}
        className="w-full bg-white border border-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-50"
      >
        Sign in with Google
      </button>

      <button
        onClick={handleGitHubSignIn}
        className="w-full bg-gray-900 text-white py-2 px-4 rounded-md hover:bg-gray-800"
      >
        Sign in with GitHub
      </button>
    </div>
  );
}
```

## Troubleshooting

### Common Issues

**1. JWT Secret Mismatch:**
```
Error: Invalid token signature
```

**Solution:**
- Ensure `BETTER_AUTH_SECRET` is the same in frontend and backend
- Verify environment variables are loaded correctly
- Check for typos in variable names

**2. Session Not Persisting:**
```
User logged out after page refresh
```

**Solution:**
```typescript
// Ensure session is stored properly
export const auth = betterAuth({
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24, // Update every 24 hours
  },
});
```

**3. CORS Errors:**
```
Error: CORS policy blocked
```

**Solution:**
```typescript
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: "/api/auth/:path*",
        headers: [
          { key: "Access-Control-Allow-Credentials", value: "true" },
          { key: "Access-Control-Allow-Origin", value: "*" },
          { key: "Access-Control-Allow-Methods", value: "GET,POST,OPTIONS" },
        ],
      },
    ];
  },
};
```

## Best Practices

### ✅ DO:
- Use strong JWT secrets (min 32 characters)
- Store secrets in environment variables
- Implement token expiration
- Use httpOnly cookies for tokens (when possible)
- Implement password strength requirements
- Enable email verification in production
- Use HTTPS in production
- Implement rate limiting on auth endpoints
- Log authentication events
- Handle token refresh properly

### ❌ DON'T:
- Hardcode JWT secrets
- Store tokens in localStorage without understanding XSS risks
- Skip email verification in production
- Use weak passwords
- Expose user passwords in logs
- Skip HTTPS in production
- Ignore failed login attempts
- Store sensitive data in JWT payload
- Skip token expiration
- Ignore security best practices

## Security Checklist

- [ ] JWT secret is strong and stored securely
- [ ] Tokens have expiration
- [ ] HTTPS enabled in production
- [ ] Password requirements enforced (min 8 chars)
- [ ] Email verification enabled
- [ ] Rate limiting on auth endpoints
- [ ] Failed login attempts logged
- [ ] Session timeout implemented
- [ ] CORS configured correctly
- [ ] OAuth redirect URLs validated

## Summary

Better Auth provides:
1. **Easy Setup**: Simple configuration and integration
2. **Type Safety**: Full TypeScript support
3. **JWT Tokens**: Stateless authentication
4. **Session Management**: Built-in session handling
5. **OAuth Support**: Multiple providers
6. **Security**: Best practices built-in

Follow this guide to implement secure, production-ready authentication in your Next.js application.
