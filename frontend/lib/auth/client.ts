/**
 * Authentication client functions.
 *
 * Provides client-side authentication functions using Better Auth.
 * Constitution Principle II: Authentication & JWT Security
 */
import { authClient, signUp, signIn, signOut, getSession, useSession } from './config';

// Re-export everything from config for backward compatibility
// Note: authClient is already exported from config, so we don't need to re-export it here
export { signUp, signIn, signOut, getSession, useSession };
