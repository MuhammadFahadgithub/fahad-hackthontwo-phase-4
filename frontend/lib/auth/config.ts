/**
 * Better Auth client configuration for Next.js frontend.
 *
 * Client-side configuration for consuming Better Auth API from backend.
 * Constitution Principle II: Authentication & JWT Security
 */
import { createAuthClient } from "better-auth/client";

// Create client instance for frontend
export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || process.env.BETTER_AUTH_URL || "http://localhost:3000/api/auth",
});

// Export auth functions for easy use
export const signUp = authClient.signUp.email;
export const signIn = authClient.signIn.email;
export const signOut = authClient.signOut;
export const getSession = authClient.getSession;
export const useSession = authClient.useSession;
