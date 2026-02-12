# Feature Specification: User Authentication

**Feature Branch**: `001-authentication`
**Created**: 2026-02-06
**Status**: Draft
**Input**: Foundational authentication system for Full-Stack Todo Application (Phase 2)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Signup (Priority: P1) 🎯 MVP

A new user needs to create an account to access the Todo application. They provide their email, name, and password, and the system creates a secure account with JWT-based authentication.

**Why this priority**: Without signup, no users can access the application. This is the absolute foundation of the multi-user system.

**Independent Test**: Can be fully tested by creating a new account through the signup form and verifying that:
- User record is created in database
- Password is hashed (never stored in plain text)
- JWT token is generated and returned
- User can immediately access protected routes with the token

**Acceptance Scenarios**:

1. **Given** a new user visits the signup page, **When** they enter valid email, name, and password (min 8 chars), **Then** account is created, JWT token is returned, and user is redirected to dashboard
2. **Given** a user tries to signup, **When** they enter an email that already exists, **Then** system returns error "Email already registered" without revealing user existence to unauthorized parties
3. **Given** a user tries to signup, **When** they enter a password shorter than 8 characters, **Then** system returns validation error "Password must be at least 8 characters"
4. **Given** a user tries to signup, **When** they enter an invalid email format, **Then** system returns validation error "Invalid email format"
5. **Given** a user successfully signs up, **When** JWT token is generated, **Then** token contains user_id in 'sub' claim and expires in 7 days

---

### User Story 2 - User Login (Priority: P2)

A returning user needs to log in to access their existing todos. They provide their email and password, and the system verifies credentials and issues a JWT token.

**Why this priority**: After signup, login is essential for returning users. Without it, users can only use the app once.

**Independent Test**: Can be fully tested by:
- Creating a user account (via signup or direct database insert)
- Logging in with correct credentials
- Verifying JWT token is returned
- Verifying user can access protected routes

**Acceptance Scenarios**:

1. **Given** an existing user visits the login page, **When** they enter correct email and password, **Then** JWT token is returned and user is redirected to dashboard
2. **Given** a user tries to login, **When** they enter incorrect password, **Then** system returns error "Invalid email or password" (generic message to prevent email enumeration)
3. **Given** a user tries to login, **When** they enter an email that doesn't exist, **Then** system returns error "Invalid email or password" (same generic message)
4. **Given** a user successfully logs in, **When** JWT token is generated, **Then** token contains user_id in 'sub' claim and email in payload
5. **Given** a user logs in, **When** they navigate to protected routes, **Then** JWT token is automatically included in Authorization header

---

### User Story 3 - User Logout (Priority: P3)

A logged-in user needs to log out to end their session, especially on shared devices. The system clears the JWT token from client storage.

**Why this priority**: Important for security on shared devices, but users can still use the app without explicit logout (token will expire).

**Independent Test**: Can be fully tested by:
- Logging in as a user
- Clicking logout button
- Verifying token is cleared from client storage
- Verifying user is redirected to login page
- Verifying user cannot access protected routes after logout

**Acceptance Scenarios**:

1. **Given** a logged-in user, **When** they click the logout button, **Then** JWT token is cleared from client storage and user is redirected to login page
2. **Given** a user has logged out, **When** they try to access a protected route, **Then** they are redirected to login page with 401 error
3. **Given** a user logs out, **When** they click browser back button, **Then** they cannot access protected pages (token is gone)

---

### User Story 4 - Password Reset (Priority: P4)

A user who forgot their password needs to reset it via email. The system sends a secure reset link and allows password update.

**Why this priority**: Nice to have for user convenience, but not critical for MVP. Users can create new accounts if needed initially.

**Independent Test**: Can be fully tested by:
- Requesting password reset for existing email
- Receiving reset token/link
- Using token to set new password
- Logging in with new password

**Acceptance Scenarios**:

1. **Given** a user forgot their password, **When** they enter their email on password reset page, **Then** system sends reset link to email (if email exists)
2. **Given** a user receives reset link, **When** they click it and enter new password, **Then** password is updated and user can login with new password
3. **Given** a user requests password reset, **When** email doesn't exist in system, **Then** system shows success message anyway (to prevent email enumeration)
4. **Given** a password reset token, **When** it's older than 1 hour, **Then** token is expired and user must request new reset link

---

### Edge Cases

- **What happens when user tries to signup with existing email?** Return generic error without revealing account existence
- **What happens when JWT token expires?** Frontend receives 401, redirects to login, user must re-authenticate
- **What happens when user tries to access protected route without token?** Middleware intercepts, returns 401, redirects to login
- **What happens when JWT secret is compromised?** All tokens become invalid when secret is rotated, all users must re-login
- **What happens when user provides malformed JWT token?** Backend verification fails, returns 401 Unauthorized
- **What happens when user tries to login with SQL injection attempt?** Parameterized queries prevent injection, login fails safely
- **What happens when multiple users signup with same email simultaneously?** Database unique constraint prevents duplicates, second request fails
- **What happens when user's session expires while using the app?** Next API call returns 401, frontend detects and redirects to login

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to create accounts with email, name, and password
- **FR-002**: System MUST validate email addresses (format: user@domain.com)
- **FR-003**: System MUST enforce password minimum length of 8 characters
- **FR-004**: System MUST hash passwords using bcrypt before storing (never store plain text)
- **FR-005**: System MUST generate JWT tokens upon successful signup/login
- **FR-006**: System MUST include user_id in JWT 'sub' claim and email in payload
- **FR-007**: System MUST set JWT token expiration to 7 days
- **FR-008**: System MUST verify JWT tokens on all protected backend endpoints
- **FR-009**: System MUST allow users to login with email and password
- **FR-010**: System MUST allow users to logout (clear token from client)
- **FR-011**: System MUST prevent duplicate email registrations (unique constraint)
- **FR-012**: System MUST return generic error messages to prevent email enumeration
- **FR-013**: System MUST persist user data in Neon PostgreSQL database
- **FR-014**: System MUST use Better Auth library for frontend authentication
- **FR-015**: System MUST implement password reset flow with time-limited tokens (1 hour expiration)

### Key Entities

- **User**: Represents an authenticated user in the system
  - `id` (integer, primary key, auto-increment)
  - `email` (string, unique, indexed, max 255 chars)
  - `name` (string, max 255 chars)
  - `hashed_password` (string, bcrypt hash, max 255 chars)
  - `email_verified` (boolean, default false)
  - `created_at` (timestamp, auto-generated)
  - `updated_at` (timestamp, auto-updated)
  - Relationships: One user has many tasks

- **Session** (managed by Better Auth):
  - `id` (integer, primary key)
  - `user_id` (integer, foreign key to users)
  - `session_token` (string, unique)
  - `expires` (timestamp)
  - `created_at` (timestamp)
  - `updated_at` (timestamp)

- **VerificationToken** (for password reset):
  - `identifier` (string, email address)
  - `token` (string, unique, random)
  - `expires` (timestamp, 1 hour from creation)

### Security Requirements *(mandatory for all features)*

**Reference**: Constitution Principles II-V (Authentication, Identity, Authorization, Isolation)

#### Authentication (Principle II)
- **SR-001**: All protected endpoints MUST require valid JWT token
- **SR-002**: JWT MUST be sent in `Authorization: Bearer <token>` header
- **SR-003**: Backend MUST verify token using `BETTER_AUTH_SECRET`
- **SR-004**: Invalid/missing tokens MUST return `401 Unauthorized`
- **SR-005**: JWT secrets MUST NEVER be logged or exposed

#### User Identity & Isolation (Principle III)
- **SR-006**: User identity MUST be extracted from JWT only (never from request body)
- **SR-007**: If `user_id` in URL, it MUST match JWT user_id (or return `403 Forbidden`)
- **SR-008**: Client-provided user identifiers MUST be ignored

#### Authorization (Principle IV)
- **SR-009**: All database queries MUST filter by authenticated `user_id`
- **SR-010**: Authorization MUST happen at query level (not post-fetch)
- **SR-011**: Example enforcement: `WHERE user_id = current_user.id`

#### Data Isolation (Principle V)
- **SR-012**: Users MUST only access their own data
- **SR-013**: Ownership verification MUST occur before update/delete operations
- **SR-014**: Prefer `404 Not Found` over `403 Forbidden` to avoid leaking existence
- **SR-015**: Cross-user access MUST be prevented and tested

#### API Contract (Principle VI)
- **SR-016**: Endpoints MUST follow RESTful conventions
- **SR-017**: Correct HTTP status codes MUST be returned:
  - `200 OK` - Successful GET, PUT, PATCH
  - `201 Created` - Successful POST (signup)
  - `204 No Content` - Successful DELETE
  - `400 Bad Request` - Invalid request data
  - `401 Unauthorized` - Missing/invalid JWT
  - `403 Forbidden` - Valid JWT but insufficient permissions
  - `404 Not Found` - Resource doesn't exist or not owned
  - `422 Unprocessable Entity` - Validation error

### Additional Security Requirements (Authentication-Specific)

- **SR-018**: Passwords MUST be hashed with bcrypt (cost factor 10+)
- **SR-019**: Password reset tokens MUST expire after 1 hour
- **SR-020**: Password reset tokens MUST be single-use (invalidated after use)
- **SR-021**: Failed login attempts MUST be logged for security monitoring
- **SR-022**: Generic error messages MUST be used to prevent email enumeration
- **SR-023**: HTTPS MUST be enforced in production (no plain HTTP)
- **SR-024**: JWT tokens MUST NOT contain sensitive data (passwords, secrets)
- **SR-025**: Rate limiting MUST be implemented on signup/login endpoints (10 requests per minute per IP)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete account creation in under 30 seconds
- **SC-002**: Users can login and receive JWT token in under 2 seconds
- **SC-003**: JWT token verification on backend completes in under 50ms
- **SC-004**: 100% of passwords are hashed (zero plain text passwords in database)
- **SC-005**: 100% of protected endpoints require valid JWT token
- **SC-006**: Zero cross-user data access incidents (verified by tests)
- **SC-007**: Password reset flow completes in under 5 minutes (including email delivery)
- **SC-008**: 95% of users successfully complete signup on first attempt
- **SC-009**: Invalid login attempts return generic error (no email enumeration possible)
- **SC-010**: All authentication tests pass (signup, login, logout, token verification, cross-user isolation)

### Technical Success Criteria

- **TSC-001**: Better Auth successfully integrated with Next.js frontend
- **TSC-002**: JWT tokens generated with correct claims (sub, email, exp)
- **TSC-003**: Backend JWT verification middleware implemented and tested
- **TSC-004**: User model created in Neon PostgreSQL with proper indexes
- **TSC-005**: Password hashing implemented with bcrypt
- **TSC-006**: Frontend auth context provides user state across components
- **TSC-007**: Protected routes redirect to login when unauthenticated
- **TSC-008**: API client automatically attaches JWT token to requests
- **TSC-009**: CORS configured to allow frontend origin only
- **TSC-010**: Environment variables properly configured for BETTER_AUTH_SECRET

### Security Success Criteria

- **SSC-001**: All security requirements (SR-001 to SR-025) implemented and verified
- **SSC-002**: Penetration testing shows no authentication bypass vulnerabilities
- **SSC-003**: JWT tokens cannot be forged (signature verification works)
- **SSC-004**: Expired tokens are rejected (401 Unauthorized)
- **SSC-005**: Password reset tokens expire after 1 hour
- **SSC-006**: No sensitive data logged (passwords, tokens, secrets)
- **SSC-007**: Rate limiting prevents brute force attacks
- **SSC-008**: Email enumeration is not possible through error messages
- **SSC-009**: SQL injection attempts are prevented by parameterized queries
- **SSC-010**: XSS attacks are prevented by proper input sanitization

## API Endpoints

### POST /api/auth/signup
**Purpose**: Create new user account

**Request**:
```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "securepassword123"
}
```

**Response** (201 Created):
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "email_verified": false,
    "created_at": "2026-02-06T10:30:00Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_at": "2026-02-13T10:30:00Z"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid email format or password too short
- `409 Conflict`: Email already registered
- `422 Unprocessable Entity`: Validation errors

### POST /api/auth/login
**Purpose**: Authenticate existing user

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response** (200 OK):
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_at": "2026-02-13T10:30:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Invalid email or password (generic message)
- `422 Unprocessable Entity`: Validation errors

### POST /api/auth/logout
**Purpose**: End user session (client-side token clearing)

**Request**: No body (token in Authorization header)

**Response** (200 OK):
```json
{
  "message": "Logged out successfully"
}
```

### POST /api/auth/password-reset/request
**Purpose**: Request password reset email

**Request**:
```json
{
  "email": "user@example.com"
}
```

**Response** (200 OK):
```json
{
  "message": "If the email exists, a reset link has been sent"
}
```

**Note**: Always returns success to prevent email enumeration

### POST /api/auth/password-reset/confirm
**Purpose**: Reset password with token

**Request**:
```json
{
  "token": "reset-token-here",
  "new_password": "newsecurepassword123"
}
```

**Response** (200 OK):
```json
{
  "message": "Password reset successfully"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid or expired token
- `422 Unprocessable Entity`: Password validation errors

### GET /api/auth/me
**Purpose**: Get current authenticated user

**Request**: No body (token in Authorization header)

**Response** (200 OK):
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe",
  "email_verified": false,
  "created_at": "2026-02-06T10:30:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid token

## Frontend Pages

### /signup
- Signup form with email, name, password fields
- Client-side validation (email format, password length)
- Error display for validation and server errors
- Redirect to /dashboard on success
- Link to /login for existing users

### /login
- Login form with email and password fields
- Client-side validation
- Error display for authentication failures
- Redirect to /dashboard on success
- Links to /signup and /password-reset

### /logout
- No UI (handled by logout button in navigation)
- Clears JWT token from storage
- Redirects to /login

### /password-reset
- Email input form
- Success message (generic)
- Link back to /login

### /password-reset/[token]
- New password form
- Password confirmation field
- Success message with redirect to /login
- Error handling for expired/invalid tokens

## Database Schema

### users table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

### sessions table (Better Auth)
```sql
CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    expires TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_token ON sessions(session_token);
```

### verification_tokens table
```sql
CREATE TABLE verification_tokens (
    identifier VARCHAR(255) NOT NULL,
    token VARCHAR(255) UNIQUE NOT NULL,
    expires TIMESTAMP NOT NULL,
    PRIMARY KEY (identifier, token)
);

CREATE INDEX idx_verification_tokens_token ON verification_tokens(token);
```

## Environment Variables

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=<min-32-char-random-string>
BETTER_AUTH_URL=http://localhost:3000
DATABASE_URL=postgresql://user:password@localhost:5432/auth_db
```

### Backend (.env)
```bash
DATABASE_URL=postgresql://user:password@ep-xxx.neon.tech/neondb?sslmode=require
BETTER_AUTH_SECRET=<same-as-frontend>
ALLOWED_ORIGINS=["http://localhost:3000"]
```

## Testing Requirements

### Unit Tests
- Password hashing and verification
- JWT token generation and verification
- Email validation
- Password strength validation
- User model CRUD operations

### Integration Tests
- Signup flow (end-to-end)
- Login flow (end-to-end)
- Logout flow
- Password reset flow
- JWT token verification on protected endpoints
- Invalid token rejection
- Expired token rejection

### Security Tests (MANDATORY)
- Cross-user isolation (User A cannot access User B's data)
- JWT token forgery prevention
- Password enumeration prevention
- SQL injection prevention
- XSS prevention
- Rate limiting enforcement
- CORS policy enforcement

## Dependencies

### Frontend
- `better-auth` - Authentication library
- `jose` - JWT handling (if needed)
- `bcryptjs` - Password hashing (client-side validation)

### Backend
- `fastapi` - Web framework
- `sqlmodel` - ORM
- `python-jose[cryptography]` - JWT verification
- `passlib[bcrypt]` - Password hashing
- `python-multipart` - Form data handling
- `psycopg2-binary` - PostgreSQL driver

## Out of Scope (Future Enhancements)

- OAuth providers (Google, GitHub) - P5
- Two-factor authentication (2FA) - P6
- Email verification flow - P7
- Remember me functionality - P8
- Account deletion - P9
- Profile picture upload - P10
- Social login - P11

## Risks and Mitigations

### Risk 1: JWT Secret Compromise
**Impact**: All tokens become invalid, attackers can forge tokens
**Mitigation**:
- Use strong random secret (min 32 chars)
- Store in environment variables only
- Never commit to version control
- Rotate secret if compromised (forces all users to re-login)

### Risk 2: Password Database Breach
**Impact**: User passwords exposed
**Mitigation**:
- Use bcrypt with high cost factor (10+)
- Never store plain text passwords
- Implement rate limiting on login
- Monitor for suspicious login patterns

### Risk 3: Email Enumeration
**Impact**: Attackers can discover registered emails
**Mitigation**:
- Use generic error messages
- Same response time for existing/non-existing emails
- Rate limiting on signup/login

### Risk 4: Token Expiration Issues
**Impact**: Users logged out unexpectedly
**Mitigation**:
- Set reasonable expiration (7 days)
- Implement token refresh mechanism (future)
- Clear error messages on expiration

### Risk 5: CORS Misconfiguration
**Impact**: Unauthorized origins can access API
**Mitigation**:
- Explicitly whitelist frontend origin
- Never use wildcard (*) in production
- Test CORS policy before deployment

## Acceptance Criteria Summary

This feature is complete when:

1. ✅ Users can signup with email, name, and password
2. ✅ Users can login with email and password
3. ✅ Users can logout (token cleared)
4. ✅ JWT tokens are generated and verified correctly
5. ✅ All passwords are hashed with bcrypt
6. ✅ Protected endpoints require valid JWT token
7. ✅ Invalid/expired tokens return 401 Unauthorized
8. ✅ Cross-user data isolation is enforced and tested
9. ✅ All security requirements (SR-001 to SR-025) are met
10. ✅ All tests pass (unit, integration, security)
11. ✅ Password reset flow works (P4 - optional for MVP)
12. ✅ Frontend and backend are integrated and working
13. ✅ Environment variables are documented and configured
14. ✅ Database schema is created with proper indexes
15. ✅ API documentation is complete and accurate
