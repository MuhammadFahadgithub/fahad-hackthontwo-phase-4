# Implementation Plan: User Authentication

**Branch**: `001-authentication` | **Date**: 2026-02-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-authentication/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement foundational authentication system for Full-Stack Todo Application using Better Auth (frontend) and JWT verification (backend). System enables user signup, login, logout, and password reset with secure token-based authentication. All user data is isolated by user_id extracted from JWT tokens, ensuring zero cross-user data access.

**Primary Requirement**: Multi-user authentication with JWT-based session management
**Technical Approach**: Better Auth library for frontend token generation, FastAPI JWT verification middleware for backend, bcrypt password hashing, Neon PostgreSQL for user storage

## Technical Context

**Frontend**:
- Framework: Next.js 16+ (App Router)
- Language: TypeScript
- Styling: Tailwind CSS
- Authentication: Better Auth (JWT generation)

**Backend**:
- Framework: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: JWT verification with BETTER_AUTH_SECRET

**Testing**:
- Backend: pytest with pytest-asyncio
- Frontend: Jest + React Testing Library
- E2E: Playwright

**Project Type**: Web application (frontend + backend)
**Performance Goals**: <200ms API response time (p95), <50ms JWT verification
**Constraints**: Multi-user isolation, JWT authentication required, password hashing mandatory
**Scale/Scope**: Multi-tenant SaaS application, foundational feature blocking all other features

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Reference**: `.specify/memory/constitution.md` (v1.0.0)

### I. Spec-First Development ✅
- [x] Feature spec exists and is complete (`specs/001-authentication/spec.md`)
- [x] API contracts documented (6 endpoints with request/response schemas)
- [x] Database schema defined (users, sessions, verification_tokens tables)
- [x] All specs reviewed before implementation

### II. Authentication & JWT Security ✅
- [x] All protected endpoints require JWT (specified in SR-001)
- [x] JWT sent in `Authorization: Bearer <token>` header (SR-002)
- [x] Backend verifies token with `BETTER_AUTH_SECRET` (SR-003)
- [x] Invalid/missing tokens return `401 Unauthorized` (SR-004)
- [x] JWT secrets never logged or exposed (SR-005)

### III. User Identity & Isolation ✅
- [x] User identity extracted from JWT only (never from request body) (SR-006)
- [x] URL `user_id` matches JWT user_id (or returns `403 Forbidden`) (SR-007)
- [x] No client-provided user identifiers trusted (SR-008)

### IV. Query-Level Authorization ✅
- [x] All database queries filter by authenticated `user_id` (SR-009)
- [x] Authorization in query (not post-fetch filtering) (SR-010)
- [x] Example: `WHERE user_id = current_user.id` (SR-011)

### V. Zero Cross-User Data Access ✅
- [x] Users can only access their own data (SR-012)
- [x] Ownership verification on all operations (SR-013)
- [x] Prefer `404` over `403` to avoid leaking existence (SR-014)
- [x] Cross-user access tests included (SR-015)

### VI. API Contract Compliance ✅
- [x] RESTful endpoint conventions followed (SR-016)
- [x] Correct HTTP status codes returned (200, 201, 204, 400, 401, 403, 404, 422) (SR-017)
- [x] API documentation complete (6 endpoints documented)
- [x] Error responses consistent

**Constitution Compliance**: ✅ PASS - All 6 principles satisfied

## Project Structure

### Documentation (this feature)

```text
specs/001-authentication/
├── spec.md              # Feature specification (COMPLETE)
├── plan.md              # This file (IN PROGRESS)
├── research.md          # Phase 0 output (PENDING)
├── data-model.md        # Phase 1 output (PENDING)
├── quickstart.md        # Phase 1 output (PENDING)
├── contracts/           # Phase 1 output (PENDING)
│   ├── signup.md
│   ├── login.md
│   ├── logout.md
│   ├── password-reset.md
│   └── get-me.md
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

**Structure Decision**: Web application with separate frontend and backend

```text
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration and settings
│   ├── database.py          # Database connection and session
│   ├── models/              # SQLModel database models
│   │   ├── __init__.py
│   │   └── user.py          # User model (NEW)
│   ├── schemas/             # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   └── auth.py          # Auth schemas (NEW)
│   ├── api/                 # API routes
│   │   ├── __init__.py
│   │   ├── deps.py          # Dependencies (auth, db) (NEW)
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── auth.py      # Auth endpoints (NEW)
│   └── core/                # Core functionality
│       ├── __init__.py
│       ├── auth.py          # JWT verification (NEW)
│       └── security.py      # Password hashing (NEW)
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test fixtures (NEW)
│   ├── test_auth.py         # Authentication tests (NEW)
│   └── test_security.py     # Security tests (NEW)
├── alembic/                 # Database migrations
│   ├── versions/
│   │   └── 001_create_users_table.py (NEW)
│   └── env.py
├── .env                     # Environment variables (not committed)
├── requirements.txt         # Python dependencies (UPDATE)
└── pytest.ini              # Pytest configuration (NEW)

frontend/
├── app/
│   ├── (auth)/             # Auth route group (NEW)
│   │   ├── login/
│   │   │   └── page.tsx    # Login page (NEW)
│   │   ├── signup/
│   │   │   └── page.tsx    # Signup page (NEW)
│   │   └── password-reset/
│   │       ├── page.tsx    # Request reset (NEW)
│   │       └── [token]/
│   │           └── page.tsx # Confirm reset (NEW)
│   ├── (dashboard)/        # Protected route group (NEW)
│   │   ├── layout.tsx      # Dashboard layout (NEW)
│   │   └── page.tsx        # Dashboard home (NEW)
│   ├── api/
│   │   └── auth/
│   │       └── [...all]/
│   │           └── route.ts # Better Auth API handler (NEW)
│   ├── layout.tsx          # Root layout (UPDATE)
│   ├── page.tsx            # Home page (UPDATE)
│   └── middleware.ts       # Auth middleware (NEW)
├── components/
│   ├── auth/               # Authentication components (NEW)
│   │   ├── SignInForm.tsx
│   │   ├── SignUpForm.tsx
│   │   ├── PasswordResetForm.tsx
│   │   └── ProtectedRoute.tsx
│   └── ui/                 # Reusable UI components
│       ├── Button.tsx      # (NEW)
│       ├── Input.tsx       # (NEW)
│       └── Card.tsx        # (NEW)
├── lib/
│   ├── auth/               # Auth configuration (NEW)
│   │   ├── config.ts       # Better Auth config
│   │   ├── client.ts       # Auth client functions
│   │   └── AuthProvider.tsx # Auth context
│   ├── api/                # API client (NEW)
│   │   └── client.ts       # Base API client with JWT
│   └── utils/              # Utility functions
│       └── validation.ts   # Email/password validation (NEW)
├── types/
│   └── index.ts            # Shared TypeScript types (NEW)
├── .env.local              # Environment variables (not committed)
├── package.json            # Node dependencies (UPDATE)
├── tsconfig.json           # TypeScript configuration
├── tailwind.config.ts      # Tailwind CSS configuration
└── next.config.js          # Next.js configuration

.specify/
└── memory/
    └── constitution.md     # Project constitution (REFERENCE)
```

## Phase 0: Research

**Purpose**: Investigate technical unknowns and validate approach

### Research Questions

1. **Better Auth Integration**
   - How to configure Better Auth with Neon PostgreSQL?
   - What database tables does Better Auth require?
   - How to customize JWT token claims (add user_id in 'sub')?
   - How to set token expiration to 7 days?

2. **JWT Verification in FastAPI**
   - Which library to use for JWT verification? (python-jose vs PyJWT)
   - How to create FastAPI dependency for JWT verification?
   - How to extract user_id from JWT 'sub' claim?
   - How to handle expired tokens gracefully?

3. **Password Hashing**
   - Bcrypt cost factor for production? (10, 12, or 14?)
   - How to hash passwords in FastAPI? (passlib library)
   - How to verify hashed passwords during login?

4. **Database Schema**
   - Does Better Auth auto-create tables or need manual migration?
   - How to add custom fields to User model?
   - How to handle database migrations with Alembic?

5. **CORS Configuration**
   - How to configure CORS in FastAPI for Next.js origin?
   - Should credentials be allowed?
   - What headers need to be exposed?

6. **Environment Variables**
   - How to share BETTER_AUTH_SECRET between frontend and backend?
   - How to securely generate strong secrets?
   - How to manage different secrets for dev/staging/prod?

### Research Deliverables

Create `research.md` with:
- Better Auth setup guide with code examples
- JWT verification implementation pattern
- Password hashing best practices
- Database migration strategy
- CORS configuration recommendations
- Environment variable management approach

## Phase 1: Design

**Purpose**: Define data models, API contracts, and architecture

### 1.1 Data Model Design

Create `data-model.md` with:

**User Entity**:
```typescript
interface User {
  id: number;              // Primary key, auto-increment
  email: string;           // Unique, indexed, max 255 chars
  name: string;            // Max 255 chars
  hashed_password: string; // Bcrypt hash, max 255 chars
  email_verified: boolean; // Default false
  created_at: Date;        // Auto-generated
  updated_at: Date;        // Auto-updated
}
```

**SQLModel Implementation**:
```python
from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    name: str = Field(max_length=255)
    hashed_password: str = Field(max_length=255)
    email_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Relationships**:
- User → Tasks (one-to-many, to be implemented in task-crud feature)

**Indexes**:
- `users.email` (unique, for login lookup)
- `users.id` (primary key, automatic)

### 1.2 API Contract Design

Create `contracts/` directory with detailed endpoint specifications:

**contracts/signup.md**:
- Endpoint: POST /api/auth/signup
- Request schema with validation rules
- Response schema with JWT token
- Error responses (400, 409, 422)
- Example requests/responses
- Security considerations

**contracts/login.md**:
- Endpoint: POST /api/auth/login
- Request schema
- Response schema with JWT token
- Error responses (401, 422)
- Generic error messages (prevent enumeration)

**contracts/logout.md**:
- Endpoint: POST /api/auth/logout
- No request body
- Response schema
- Client-side token clearing

**contracts/password-reset.md**:
- Endpoint: POST /api/auth/password-reset/request
- Endpoint: POST /api/auth/password-reset/confirm
- Request/response schemas
- Token expiration (1 hour)
- Security considerations

**contracts/get-me.md**:
- Endpoint: GET /api/auth/me
- No request body
- Response schema with user data
- Requires JWT authentication

### 1.3 Architecture Decisions

**Authentication Flow**:
```
1. User submits credentials (signup/login)
2. Frontend sends to Better Auth API route
3. Better Auth validates and generates JWT
4. JWT stored in frontend (localStorage or cookies)
5. Frontend includes JWT in Authorization header for API calls
6. Backend extracts JWT from header
7. Backend verifies JWT signature with BETTER_AUTH_SECRET
8. Backend extracts user_id from 'sub' claim
9. Backend uses user_id for all database queries
10. Backend returns user-specific data
```

**Security Architecture**:
- JWT tokens signed with HS256 algorithm
- Tokens expire after 7 days
- Passwords hashed with bcrypt (cost factor 12)
- Rate limiting on auth endpoints (10 req/min per IP)
- CORS restricted to frontend origin only
- HTTPS enforced in production

**Error Handling Strategy**:
- Generic error messages for authentication failures
- Specific validation errors for input issues
- Consistent error response format
- No sensitive data in error messages

### 1.4 Frontend Architecture

**Component Hierarchy**:
```
App
├── AuthProvider (context)
│   ├── (auth) route group
│   │   ├── SignUpForm
│   │   ├── SignInForm
│   │   └── PasswordResetForm
│   └── (dashboard) route group (protected)
│       └── Dashboard content
```

**State Management**:
- AuthProvider context for global auth state
- Local state in forms for input handling
- No global state library needed (use React Context)

**API Client Pattern**:
```typescript
// lib/api/client.ts
export async function apiRequest(endpoint: string, options: RequestInit = {}) {
  const token = getAuthToken();

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (response.status === 401) {
    // Redirect to login
    window.location.href = '/login';
  }

  return response;
}
```

### 1.5 Quickstart Guide

Create `quickstart.md` with:
- Local development setup instructions
- Environment variable configuration
- Database setup (Neon connection)
- Running backend (uvicorn)
- Running frontend (npm run dev)
- Testing authentication flow
- Common troubleshooting issues

## Phase 2: Implementation Tasks

**Note**: Detailed task breakdown will be created by `/sp.tasks` command after this plan is approved.

**High-Level Task Groups**:

1. **Setup & Configuration** (5-7 tasks)
   - Create project structure
   - Install dependencies
   - Configure environment variables
   - Setup database connection
   - Configure Better Auth

2. **Backend - Database & Models** (3-5 tasks)
   - Create User model with SQLModel
   - Create Alembic migration for users table
   - Setup database session management
   - Create test fixtures

3. **Backend - Authentication Core** (5-7 tasks)
   - Implement password hashing utilities
   - Implement JWT verification function
   - Create get_current_user dependency
   - Setup CORS middleware
   - Create error handlers

4. **Backend - API Endpoints** (6-8 tasks)
   - Implement POST /api/auth/signup
   - Implement POST /api/auth/login
   - Implement POST /api/auth/logout
   - Implement GET /api/auth/me
   - Implement password reset endpoints
   - Add input validation

5. **Frontend - Better Auth Setup** (4-6 tasks)
   - Configure Better Auth
   - Create Better Auth API route
   - Create AuthProvider context
   - Implement auth client functions

6. **Frontend - UI Components** (8-10 tasks)
   - Create SignUpForm component
   - Create SignInForm component
   - Create PasswordResetForm component
   - Create protected route wrapper
   - Create auth pages (signup, login, etc.)
   - Add loading and error states

7. **Frontend - API Integration** (3-5 tasks)
   - Create API client with JWT attachment
   - Implement auth API functions
   - Handle 401 redirects
   - Handle error responses

8. **Testing** (10-15 tasks)
   - Backend unit tests (password hashing, JWT)
   - Backend integration tests (signup, login, logout)
   - Backend security tests (cross-user isolation, token forgery)
   - Frontend component tests
   - E2E tests (signup flow, login flow)

9. **Security Validation** (5-7 tasks)
   - Verify JWT verification works
   - Verify password hashing works
   - Verify cross-user isolation
   - Verify rate limiting
   - Verify CORS configuration

10. **Documentation & Polish** (3-5 tasks)
    - Update README with auth setup
    - Document environment variables
    - Add API documentation
    - Code cleanup and refactoring

**Estimated Total Tasks**: 50-70 tasks

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**No violations detected** - Constitution check passed all 6 principles.

## Dependencies

### External Dependencies

**Frontend**:
- `better-auth` - Authentication library (NEW)
- `@better-auth/react` - React hooks (NEW)
- `bcryptjs` - Password hashing for client validation (NEW)

**Backend**:
- `python-jose[cryptography]` - JWT verification (NEW)
- `passlib[bcrypt]` - Password hashing (NEW)
- `python-multipart` - Form data handling (NEW)
- `psycopg2-binary` - PostgreSQL driver (EXISTING)

### Internal Dependencies

- Neon PostgreSQL database (must be provisioned)
- Environment variables (BETTER_AUTH_SECRET must be shared)
- CORS configuration (frontend origin must be whitelisted)

### Blocking Dependencies

**This feature blocks**:
- Task CRUD feature (requires user authentication)
- All other features (authentication is foundational)

**This feature is blocked by**:
- None (foundational feature)

## Risk Assessment

### High Risk

**Risk**: JWT secret compromise
- **Impact**: All tokens become invalid, attackers can forge tokens
- **Mitigation**: Use strong random secret (min 32 chars), store in env vars only, never commit
- **Contingency**: Rotate secret immediately, force all users to re-login

**Risk**: Password database breach
- **Impact**: User passwords exposed
- **Mitigation**: Use bcrypt with cost factor 12, never store plain text, rate limit login attempts
- **Contingency**: Force password reset for all users, notify users of breach

### Medium Risk

**Risk**: Email enumeration
- **Impact**: Attackers can discover registered emails
- **Mitigation**: Use generic error messages, same response time for existing/non-existing emails
- **Contingency**: Monitor for suspicious patterns, implement additional rate limiting

**Risk**: Token expiration issues
- **Impact**: Users logged out unexpectedly
- **Mitigation**: Set reasonable expiration (7 days), clear error messages
- **Contingency**: Implement token refresh mechanism (future enhancement)

### Low Risk

**Risk**: CORS misconfiguration
- **Impact**: Unauthorized origins can access API
- **Mitigation**: Explicitly whitelist frontend origin, never use wildcard in production
- **Contingency**: Update CORS config, redeploy backend

## Success Metrics

### Implementation Complete When:

1. ✅ All constitution checks pass
2. ✅ All user stories (P1-P4) implemented and tested
3. ✅ All security requirements (SR-001 to SR-025) verified
4. ✅ All API endpoints working with correct status codes
5. ✅ JWT tokens generated and verified correctly
6. ✅ Passwords hashed with bcrypt (100% coverage)
7. ✅ Cross-user isolation tests pass
8. ✅ Frontend and backend integrated
9. ✅ All tests pass (unit, integration, security, E2E)
10. ✅ Documentation complete (README, API docs, quickstart)

### Performance Targets:

- Signup completes in <30 seconds
- Login completes in <2 seconds
- JWT verification completes in <50ms
- API response time <200ms (p95)

### Security Targets:

- 100% of passwords hashed (zero plain text)
- 100% of protected endpoints require JWT
- Zero cross-user data access incidents
- Rate limiting prevents brute force attacks
- Email enumeration not possible

## Next Steps

1. **Review and Approve Plan**: Stakeholder review of this implementation plan
2. **Phase 0 Research**: Create `research.md` with technical investigation results
3. **Phase 1 Design**: Create `data-model.md`, `contracts/`, and `quickstart.md`
4. **Phase 2 Tasks**: Run `/sp.tasks` to generate detailed task breakdown
5. **Implementation**: Execute tasks in dependency order
6. **Testing**: Verify all acceptance criteria and security requirements
7. **Deployment**: Deploy to staging for integration testing

## Approval

**Plan Status**: Draft - Awaiting Review

**Reviewers**:
- [ ] Technical Lead - Architecture review
- [ ] Security Lead - Security requirements review
- [ ] Product Owner - User stories and acceptance criteria review

**Approval Date**: _____________

**Approved By**: _____________
