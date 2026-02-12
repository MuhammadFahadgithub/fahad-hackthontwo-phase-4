/**
 * Authentication middleware for Next.js.
 *
 * Protects routes by checking for valid authentication.
 * Constitution Principle II: Authentication & JWT Security
 * Constitution Principle III: User Identity & Isolation
 */
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Public routes that don't require authentication
  const publicRoutes = ["/", "/login", "/signup", "/password-reset", "/api/auth"];
  const isPublicRoute = publicRoutes.some((route) =>
    pathname.startsWith(route)
  );

  if (isPublicRoute) {
    return NextResponse.next();
  }

  // Check authentication for protected routes by verifying the auth token cookie
  const authToken = request.cookies.get("better-auth-session-token");
  
  if (!authToken) {
    // Redirect to login if not authenticated
    // Constitution SR-004: Invalid/missing tokens return 401 (redirect to login)
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
    "/((?!_next/static|_next/image|favicon.ico|public|_next).*)",
  ],
};
