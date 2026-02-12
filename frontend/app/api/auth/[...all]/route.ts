/**
 * Better Auth API route handler.
 *
 * This file should be removed as Better Auth API should be handled in the backend.
 * Frontend should only consume the API from the backend service.
 * Constitution Principle II: Authentication & JWT Security
 */

// This file is not needed in the frontend - API routes belong in the backend
// The frontend should only consume the auth API from the backend service
export async function GET() {
  return new Response(
    JSON.stringify({ error: "Authentication API should be handled in the backend" }),
    { status: 501, headers: { "Content-Type": "application/json" } }
  );
}

export async function POST() {
  return new Response(
    JSON.stringify({ error: "Authentication API should be handled in the backend" }),
    { status: 501, headers: { "Content-Type": "application/json" } }
  );
}
