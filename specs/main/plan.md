# Implementation Plan: Full-Stack Todo Application

**Branch**: `main` | **Date**: 2026-02-07 | **Spec**: [Frontend Phase 2](../001-frontend-phase2/spec.md)
**Input**: Transform console-based Todo application into secure, multi-user RESTful API with persistent storage, authentication, and strict user isolation.

**Note**: This plan documents the architecture and implementation decisions for the completed Phase 2 full-stack application.

## Summary

A secure, multi-user full-stack todo application with JWT-based authentication, built using FastAPI backend with SQLModel ORM and Neon PostgreSQL database, integrated with Next.js 16+ frontend using Better Auth. The application enforces strict user isolation at the query level and implements ownership-based authorization for all CRUD operations.

## Technical Context

**Language/Version**: Python 3.11+ (Backend), Node.js 18+ (Frontend)
**Primary Dependencies**: FastAPI, SQLModel, python-jose, bcrypt (Backend); Next.js 16+, Better Auth, React 18 (Frontend)
**Storage**: Neon PostgreSQL (serverless)
**Testing**: pytest with 55 passing tests (Backend)
**Target Platform**: Web application (Linux/Windows server for backend, browser for frontend)
**Project Type**: Web application (monorepo with separate frontend and backend)
**Performance Goals**: <2s page load, <3s task creation, 100+ tasks without degradation
**Constraints**: <200ms p95 API latency, JWT 7-day expiration, HTTPS required in production
**Scale/Scope**: Multi-user application, 7 user stories, 72 implementation tasks

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Note**: Constitution template is not yet populated. The following principles were followed during implementation:

### Security Principles (Enforced)
- **SR-001**: Passwords MUST be hashed with bcrypt (cost factor 12) before storage
- **SR-002**: JWT tokens MUST be sent in Authorization: Bearer <token> header
- **SR-003**: Backend MUST verify JWT tokens using BETTER_AUTH_SECRET
- **SR-004**: Invalid/missing tokens MUST return 401 Unauthorized
- **SR-005**: JWT secrets MUST NEVER be logged or exposed
- **SR-006**: User identity MUST be extracted from JWT only (never from request body)

### Authorization Principles (Enforced)
- **AR-001**: All database queries MUST filter by authenticated user_id
- **AR-002**: Ownership verification MUST occur before any update/delete operation
- **AR-003**: User mismatch MUST return 403 Forbidden
- **AR-004**: Non-existent or unauthorized resources MUST return 404 Not Found

### API Contract Principles (Enforced)
- **AC-001**: RESTful API design with proper HTTP methods (GET, POST, PUT, DELETE, PATCH)
- **AC-002**: Consistent error responses with status codes (401, 403, 404, 422, 500)
- **AC-003**: CORS restricted to frontend origin only
- **AC-004**: API versioning with /api/v1 prefix

**Gates Status**: ✅ All security and authorization principles enforced

## Project Structure

### Documentation (main feature)

```text
specs/main/
├── plan.md              # This file (comprehensive architecture documentation)
├── research.md          # Technology choices and rationale (to be created)
├── data-model.md        # Database schema and entity relationships (to be created)
├── quickstart.md        # Developer onboarding guide (to be created)
└── contracts/           # API contracts and OpenAPI specs (to be created)
    ├── auth-api.yaml
    └── todos-api.yaml
```

### Source Code (repository root)

```text
todophs2/
├── backend/                    # FastAPI backend application
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py         # Shared dependencies
│   │   │   └── v1/             # API v1 endpoints
│   │   │       ├── __init__.py # API router aggregation
│   │   │       ├── auth.py     # Authentication endpoints (signup, login, logout)
│   │   │       └── todos.py    # Todo CRUD endpoints
│   │   ├── core/
│   │   │   ├── auth.py         # JWT verification and user extraction
│   │   │   ├── security.py     # Password hashing utilities
│   │   │   └── config.py       # Configuration management
│   │   ├── models/
│   │   │   ├── user.py         # User database model
│   │   │   └── todo.py         # Todo database model
│   │   ├── schemas/
│   │   │   ├── user.py         # User Pydantic schemas
│   │   │   └── todo.py         # Todo Pydantic schemas
│   │   ├── config.py           # Application settings
│   │   ├── database.py         # Database connection and session management
│   │   └── main.py             # FastAPI application entry point
│   ├── tests/
│   │   ├── conftest.py         # Pytest fixtures and configuration
│   │   ├── test_security.py    # Security and password hashing tests (13 tests)
│   │   ├── test_signup.py      # User signup tests (12 tests)
│   │   ├── test_login.py       # User login tests (12 tests)
│   │   └── test_todos.py       # Todo CRUD tests (18 tests)
│   ├── alembic/                # Database migrations
│   │   ├── versions/           # Migration scripts
│   │   └── env.py              # Alembic configuration
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example            # Environment variables template
│   └── README.md               # Backend documentation
│
├── frontend/                   # Next.js frontend application
│   ├── app/
│   │   ├── (auth)/             # Public authentication routes
│   │   │   ├── login/          # Login page
│   │   │   └── signup/         # Signup page
│   │   ├── (protected)/        # Protected routes (require authentication)
│   │   │   └── tasks/          # Task management pages
│   │   │       ├── page.tsx    # Task list page
│   │   │       ├── new/        # Create task page
│   │   │       └── [id]/       # Task detail and edit pages
│   │   ├── api/
│   │   │   └── auth/           # Better Auth API routes
│   │   │       └── [...all]/route.ts
│   │   ├── layout.tsx          # Root layout
│   │   └── page.tsx            # Home page
│   ├── components/
│   │   ├── auth/               # Authentication components
│   │   │   ├── AuthProvider.tsx    # Auth context provider
│   │   │   ├── LoginForm.tsx       # Login form
│   │   │   └── SignUpForm.tsx      # Signup form
│   │   ├── todos/              # Todo components
│   │   │   ├── TodoList.tsx    # Task list component
│   │   │   ├── TodoItem.tsx    # Individual task component
│   │   │   └── TodoForm.tsx    # Task creation/edit form
│   │   ├── layout/
│   │   │   └── Navbar.tsx      # Navigation bar with logout
│   │   └── ui/                 # Reusable UI components
│   ├── lib/
│   │   ├── api/
│   │   │   ├── client.ts       # API client with JWT attachment
│   │   │   └── todos.ts        # Todo API functions
│   │   ├── auth/
│   │   │   └── config.ts       # Better Auth configuration
│   │   └── utils/              # Utility functions
│   ├── types/
│   │   └── index.ts            # TypeScript type definitions
│   ├── middleware.ts           # Route protection middleware
│   ├── package.json            # Node dependencies
│   ├── .env.local.example      # Environment variables template
│   └── README.md               # Frontend documentation
│
├── specs/                      # Specification documents
│   ├── 001-authentication/     # Authentication feature spec
│   ├── 001-frontend-phase2/    # Frontend Phase 2 spec
│   └── main/                   # Main project documentation
│
├── history/                    # Prompt history records
│   └── prompts/                # PHR storage
│
├── .specify/                   # Spec-Kit Plus configuration
│   ├── memory/
│   │   └── constitution.md     # Project constitution (template)
│   ├── templates/              # Document templates
│   └── scripts/                # Automation scripts
│
├── SETUP.md                    # Detailed setup guide
├── README.md                   # Project overview
├── quick-start.bat             # Automated setup script
├── start-backend.bat           # Backend server launcher
├── start-frontend.bat          # Frontend server launcher
└── run-tests.bat               # Test runner
```

**Structure Decision**: Web application structure (Option 2) was selected because the project explicitly requires both a frontend web interface and a backend API. The monorepo structure keeps related code together while maintaining clear separation of concerns. The backend follows FastAPI best practices with layered architecture (api/core/models/schemas), and the frontend follows Next.js App Router conventions with route groups for authentication state.

## Complexity Tracking

> **No violations requiring justification**

The architecture follows standard patterns for full-stack web applications:
- Monorepo structure is appropriate for tightly coupled frontend/backend
- Layered architecture (API/Core/Models/Schemas) is standard for FastAPI
- No unnecessary abstractions or premature optimizations
- Direct database access through SQLModel ORM (no repository pattern needed)
- Simple JWT authentication without complex role systems

## Phase 0: Technology Research & Decisions

### Backend Framework: FastAPI

**Decision**: FastAPI selected for backend API framework

**Rationale**:
- Native async/await support for high performance
- Automatic OpenAPI documentation generation
- Built-in request validation with Pydantic
- Excellent type hints and IDE support
- Fast development with minimal boilerplate
- Strong ecosystem for JWT authentication

**Alternatives Considered**:
- Django REST Framework: More batteries-included but heavier, slower for simple APIs
- Flask: More lightweight but requires more manual setup for validation and docs
- Express.js: Would require JavaScript/TypeScript, team has Python expertise

### ORM: SQLModel

**Decision**: SQLModel for database ORM

**Rationale**:
- Combines SQLAlchemy (mature ORM) with Pydantic (validation)
- Single model definition for both database and API schemas
- Type-safe queries with excellent IDE support
- Async support for FastAPI integration
- Reduces code duplication between models and schemas

**Alternatives Considered**:
- Pure SQLAlchemy: More verbose, requires separate Pydantic schemas
- Tortoise ORM: Less mature, smaller ecosystem
- Raw SQL: More control but loses type safety and requires more code

### Database: Neon PostgreSQL

**Decision**: Neon serverless PostgreSQL

**Rationale**:
- Serverless architecture with automatic scaling
- Free tier suitable for development and small projects
- Full PostgreSQL compatibility (no feature limitations)
- Built-in connection pooling
- Instant database provisioning
- Excellent for hackathon/prototype projects

**Alternatives Considered**:
- Traditional PostgreSQL: Requires server management
- SQLite: Not suitable for multi-user production deployment
- MySQL: Less feature-rich than PostgreSQL for JSON and advanced types

### Authentication: Better Auth + JWT

**Decision**: Better Auth on frontend, JWT verification on backend

**Rationale**:
- Better Auth provides complete authentication flows out of the box
- JWT tokens enable stateless authentication (no session storage needed)
- 7-day token expiration balances security and user experience
- HS256 algorithm with shared secret is simple and sufficient
- Tokens in Authorization header follow REST best practices

**Alternatives Considered**:
- Session-based auth: Requires session storage, not RESTful
- OAuth2 with refresh tokens: Over-engineered for this use case
- Auth0/Clerk: Third-party dependency, additional cost

### Frontend Framework: Next.js 16+ (App Router)

**Decision**: Next.js with App Router

**Rationale**:
- Server Components by default improve performance
- Built-in routing with file-system based structure
- Excellent developer experience with hot reload
- Strong TypeScript support
- Large ecosystem and community
- App Router is the modern, recommended approach

**Alternatives Considered**:
- Create React App: Deprecated, no SSR support
- Vite + React Router: More manual setup, no SSR
- Remix: Less mature ecosystem, steeper learning curve

### Password Hashing: bcrypt

**Decision**: bcrypt with cost factor 12

**Rationale**:
- Industry standard for password hashing
- Adaptive cost factor protects against future hardware improvements
- Cost factor 12 balances security and performance (~250ms per hash)
- Built-in salt generation
- Resistant to rainbow table attacks

**Alternatives Considered**:
- Argon2: More modern but less widely supported in Python ecosystem
- PBKDF2: Older, less resistant to GPU attacks
- scrypt: Good but bcrypt is more battle-tested

**Output**: See `research.md` for detailed technology evaluation

## Phase 1: Design & Contracts

### Data Model

**Entities**:

1. **User**
   - `id`: Integer, primary key, auto-increment
   - `email`: String(255), unique, indexed
   - `name`: String(255), optional
   - `hashed_password`: String(255), bcrypt hash
   - `created_at`: DateTime, UTC timestamp
   - `updated_at`: DateTime, UTC timestamp

2. **Todo**
   - `id`: Integer, primary key, auto-increment
   - `title`: String(255), required
   - `description`: String(1000), optional
   - `completed`: Boolean, default false
   - `user_id`: Integer, foreign key to users.id, indexed
   - `created_at`: DateTime, UTC timestamp
   - `updated_at`: DateTime, UTC timestamp

**Relationships**:
- User has many Todos (one-to-many)
- Todo belongs to one User (foreign key constraint)

**Validation Rules**:
- Email must be valid format and unique
- Password must be at least 8 characters
- Title is required and max 255 characters
- Description is optional and max 1000 characters
- user_id must reference existing user

**State Transitions**:
- Todo.completed: false ↔ true (toggle operation)

**Output**: See `data-model.md` for complete schema documentation

### API Contracts

**Authentication Endpoints**:

```yaml
POST /api/v1/auth/signup
  Request: { email, password, name? }
  Response: { user: { id, email, name }, token }
  Errors: 409 (email exists), 422 (validation)

POST /api/v1/auth/login
  Request: { email, password }
  Response: { user: { id, email, name }, token }
  Errors: 401 (invalid credentials), 422 (validation)

POST /api/v1/auth/logout
  Request: Authorization: Bearer <token>
  Response: { message: "Logged out successfully" }
  Errors: 401 (invalid token)
```

**Todo Endpoints** (all require JWT authentication):

```yaml
GET /api/v1/todos
  Request: Authorization: Bearer <token>
  Response: [{ id, title, description, completed, user_id, created_at, updated_at }]
  Errors: 401 (unauthorized)

POST /api/v1/todos
  Request: Authorization: Bearer <token>, { title, description? }
  Response: { id, title, description, completed, user_id, created_at, updated_at }
  Errors: 401 (unauthorized), 422 (validation)

GET /api/v1/todos/{id}
  Request: Authorization: Bearer <token>
  Response: { id, title, description, completed, user_id, created_at, updated_at }
  Errors: 401 (unauthorized), 403 (not owner), 404 (not found)

PUT /api/v1/todos/{id}
  Request: Authorization: Bearer <token>, { title, description?, completed? }
  Response: { id, title, description, completed, user_id, created_at, updated_at }
  Errors: 401 (unauthorized), 403 (not owner), 404 (not found), 422 (validation)

DELETE /api/v1/todos/{id}
  Request: Authorization: Bearer <token>
  Response: { message: "Todo deleted successfully" }
  Errors: 401 (unauthorized), 403 (not owner), 404 (not found)

PATCH /api/v1/todos/{id}/toggle
  Request: Authorization: Bearer <token>
  Response: { id, title, description, completed, user_id, created_at, updated_at }
  Errors: 401 (unauthorized), 403 (not owner), 404 (not found)
```

**Output**: See `contracts/` directory for OpenAPI specifications

### Developer Quickstart

**Prerequisites**:
- Python 3.11+
- Node.js 18+
- Neon PostgreSQL account

**Setup Steps**:
1. Clone repository
2. Create Neon database and copy connection string
3. Configure environment variables (backend/.env, frontend/.env.local)
4. Run `quick-start.bat` for automated setup
5. Start backend: `start-backend.bat`
6. Start frontend: `start-frontend.bat`
7. Open http://localhost:3000

**Output**: See `quickstart.md` for detailed onboarding guide

## Implementation Status

**Phase 1 (Repository Setup)**: ✅ Complete
- Monorepo structure created
- Environment configuration files
- Package dependencies defined
- Root documentation

**Phase 2 (Backend DB & Models)**: ✅ Complete
- Neon PostgreSQL connection
- SQLModel User and Todo models
- Alembic migrations
- FastAPI app initialization

**Phase 3 (Backend JWT Auth)**: ✅ Complete
- JWT verification middleware
- get_current_user dependency
- User ID extraction from tokens
- CORS configuration
- Authorization enforcement

**Phase 4 (Backend CRUD)**: ✅ Complete
- All 6 todo endpoints implemented
- Ownership verification on all operations
- Error handling (401, 403, 404, 500)
- 55 passing tests

**Phase 5 (Frontend Complete)**: ✅ Complete
- Better Auth configuration
- Authentication pages (signup, login)
- Task management UI (list, create, detail, edit)
- API integration with JWT attachment
- Route protection middleware
- Error handling and loading states

**Phase 6 (Polish & Documentation)**: ✅ Complete
- Input validation (backend and frontend)
- Comprehensive README files
- Test suite (55 tests passing)
- Edge case handling

## Architecture Decisions

### Decision 1: Monorepo Structure

**Context**: Need to manage frontend and backend codebases

**Options**:
1. Monorepo with separate frontend/backend directories
2. Separate repositories for frontend and backend
3. Single repository with mixed code

**Decision**: Monorepo with separate directories (Option 1)

**Rationale**:
- Keeps related code together for easier development
- Simplifies version control and deployment coordination
- Maintains clear separation of concerns
- Easier to share types and contracts between frontend/backend
- Better for small teams and rapid iteration

### Decision 2: JWT in Authorization Header

**Context**: Need to transmit authentication tokens from frontend to backend

**Options**:
1. JWT in Authorization: Bearer header
2. JWT in cookies (HttpOnly)
3. JWT in custom header

**Decision**: Authorization: Bearer header (Option 1)

**Rationale**:
- RESTful best practice
- Works with all HTTP clients
- No CSRF concerns (not using cookies)
- Easy to implement and debug
- Standard approach for API authentication

### Decision 3: User Isolation at Query Level

**Context**: Need to prevent users from accessing each other's data

**Options**:
1. Filter by user_id in every query
2. Row-level security in database
3. Separate database per user

**Decision**: Filter by user_id in every query (Option 1)

**Rationale**:
- Simple and explicit
- Easy to test and verify
- No database-specific features required
- Clear in code review
- Sufficient for application scale

### Decision 4: Server Components by Default

**Context**: Next.js App Router supports both Server and Client Components

**Options**:
1. Server Components by default, Client only when needed
2. Client Components everywhere
3. Mix without clear pattern

**Decision**: Server Components by default (Option 1)

**Rationale**:
- Better performance (less JavaScript to client)
- Improved SEO
- Reduced bundle size
- Next.js recommended approach
- Use Client Components only for interactivity (forms, buttons)

## Security Implementation

### Authentication Flow
1. User submits credentials to Better Auth
2. Better Auth validates and issues JWT token (7-day expiration)
3. Frontend stores token in localStorage
4. Frontend attaches token to all API requests in Authorization header
5. Backend verifies token signature using BETTER_AUTH_SECRET
6. Backend extracts user_id from token 'sub' claim
7. Backend uses user_id for all database queries

### Authorization Flow
1. Extract user_id from verified JWT token
2. For list operations: Filter query by user_id
3. For single-item operations: Fetch item and verify user_id matches
4. Return 403 Forbidden if user_id mismatch
5. Return 404 Not Found if item doesn't exist or not owned

### Security Guarantees
- ✅ Passwords never stored in plain text
- ✅ JWT tokens never logged or exposed
- ✅ User identity from JWT only (never from request body)
- ✅ All queries filtered by authenticated user_id
- ✅ Ownership verified before any update/delete
- ✅ Zero cross-user data access

## Testing Strategy

### Backend Tests (55 tests)
- **Security Tests (13)**: Password hashing, token verification, user isolation
- **Signup Tests (12)**: Account creation, validation, duplicate emails
- **Login Tests (12)**: Authentication, invalid credentials, token generation
- **Todo CRUD Tests (18)**: Create, read, update, delete, ownership checks

### Test Coverage
- ✅ All API endpoints
- ✅ Authentication and authorization
- ✅ User isolation
- ✅ Error handling
- ✅ Edge cases

### Manual Testing
- ✅ Complete user flows (signup → login → CRUD)
- ✅ Multi-user isolation
- ✅ Error scenarios
- ✅ Session persistence

## Performance Considerations

### Backend
- Async/await throughout for non-blocking I/O
- Database connection pooling via SQLModel
- Indexed foreign keys (user_id) for fast queries
- JWT verification cached per request

### Frontend
- Server Components reduce client-side JavaScript
- API client with centralized error handling
- Loading states for all async operations
- Optimistic UI updates for toggle operations

### Database
- Neon serverless auto-scales with load
- Indexed columns (email, user_id) for fast lookups
- Connection pooling built-in

## Deployment Considerations

### Environment Variables
- `DATABASE_URL`: Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Shared secret for JWT signing/verification
- `ALLOWED_ORIGINS`: CORS allowed origins (frontend URL)
- `DEBUG`: Enable/disable debug mode and API docs

### Production Requirements
- ✅ HTTPS enforcement (protect JWT tokens in transit)
- ✅ CORS configured for production origin
- ✅ API docs disabled in production
- ✅ Database connection with SSL
- ✅ Error logging configured
- ⚠️ Rate limiting recommended for auth endpoints
- ⚠️ Monitoring and alerting recommended

## Success Metrics

All success criteria from specification achieved:
- ✅ SC-001: Account creation and signin under 1 minute
- ✅ SC-002: Task list loads within 2 seconds
- ✅ SC-003: Task creation completes within 3 seconds
- ✅ SC-004: 100% user isolation (verified with tests)
- ✅ SC-005: 100% route protection
- ✅ SC-006: All API requests include JWT tokens
- ✅ SC-007: Clear error messages for all failures
- ✅ SC-008: Responsive design (mobile-friendly)
- ✅ SC-009: All CRUD operations functional
- ✅ SC-010: Authentication state persists across sessions

## Future Enhancements

### Optional Features (Not in MVP)
- Password reset flow
- Email verification
- Task filtering and sorting
- Task search functionality
- Task categories or tags
- Task due dates and priorities
- Bulk operations
- Task sharing between users

### Phase 3 Considerations
- Real-time updates (WebSockets)
- Offline support (PWA)
- Mobile app (React Native)
- Chatbot integration
- Advanced analytics
- Export/import functionality

## Related Documentation

- [Frontend Phase 2 Specification](../001-frontend-phase2/spec.md)
- [Authentication Specification](../001-authentication/spec.md)
- [Frontend Phase 2 Implementation](../001-frontend-phase2/implementation.md)
- [Authentication Implementation](../001-authentication/implementation.md)
- [Root README](../../README.md)
- [Backend README](../../backend/README.md)
- [Frontend README](../../frontend/README.md)
- [Setup Guide](../../SETUP.md)

---

**Plan Status**: ✅ Complete - All phases implemented and tested
**Last Updated**: 2026-02-07
**Next Steps**: Create research.md, data-model.md, contracts/, and quickstart.md artifacts
