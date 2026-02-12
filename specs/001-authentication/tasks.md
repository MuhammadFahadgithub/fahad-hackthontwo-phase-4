# Tasks: User Authentication

**Input**: Design documents from `/specs/001-authentication/`
**Prerequisites**: plan.md (✅ complete), spec.md (✅ complete)

**Tests**: Tests are included as this is a security-critical feature requiring comprehensive testing.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

**Web Application Structure** (as defined in constitution):

- **Backend**: `backend/app/`, `backend/tests/`
  - Models: `backend/app/models/`
  - Schemas: `backend/app/schemas/`
  - API routes: `backend/app/api/v1/`
  - Core: `backend/app/core/` (auth, security)
  - Tests: `backend/tests/`

- **Frontend**: `frontend/app/`, `frontend/components/`, `frontend/lib/`
  - Pages: `frontend/app/`
  - Components: `frontend/components/`
  - API client: `frontend/lib/api/`
  - Auth: `frontend/lib/auth/`
  - Types: `frontend/types/`

- **Specs**: `specs/001-authentication/`
  - Specification: `specs/001-authentication/spec.md`
  - Plan: `specs/001-authentication/plan.md`
  - Tasks: `specs/001-authentication/tasks.md`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create backend directory structure (app/, tests/, alembic/)
- [ ] T002 Create frontend directory structure (app/, components/, lib/, types/)
- [ ] T003 [P] Initialize backend with FastAPI dependencies in requirements.txt
- [ ] T004 [P] Initialize frontend with Next.js and install dependencies (better-auth, etc.)
- [ ] T005 [P] Create .env.example files for backend and frontend
- [ ] T006 [P] Configure linting and formatting tools (ESLint, Prettier, Ruff)
- [ ] T007 Create .gitignore to exclude .env files and sensitive data

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database & Models (Backend)

- [ ] T008 Setup Neon PostgreSQL connection in backend/app/database.py
- [ ] T009 Configure SQLModel engine with connection pooling
- [ ] T010 Setup Alembic for database migrations in backend/alembic/
- [ ] T011 [P] Create User model in backend/app/models/user.py with all fields (id, email, name, hashed_password, email_verified, timestamps)
- [ ] T012 [P] Create Alembic migration for users table with indexes (email unique, email index)
- [ ] T013 [P] Create sessions table migration (Better Auth requirement)
- [ ] T014 [P] Create verification_tokens table migration (password reset)

### Authentication & Security (Constitution Principles II-V)

**Reference**: Constitution v1.0.0 - Principles II (Authentication), III (Identity), IV (Authorization), V (Isolation)

- [ ] T015 [P] Configure Better Auth in frontend/lib/auth/config.ts with Neon database
- [ ] T016 [P] Create Better Auth API route in frontend/app/api/auth/[...all]/route.ts
- [ ] T017 [P] Implement JWT verification function in backend/app/core/auth.py using python-jose
- [ ] T018 [P] Implement password hashing utilities in backend/app/core/security.py using passlib/bcrypt
- [ ] T019 [P] Create get_current_user dependency in backend/app/api/deps.py (extracts user from JWT)
- [ ] T020 [P] Setup BETTER_AUTH_SECRET in environment variables (.env files for both frontend and backend)
- [ ] T021 [P] Create AuthProvider context in frontend/lib/auth/AuthProvider.tsx
- [ ] T022 [P] Implement auth client functions in frontend/lib/auth/client.ts (signUp, signIn, signOut, getSession)
- [ ] T023 [P] Create protected route middleware in frontend/middleware.ts

### API Infrastructure (Backend)

- [ ] T024 Setup FastAPI application in backend/app/main.py
- [ ] T025 Configure CORS middleware with allowed origins (frontend URL only)
- [ ] T026 Setup API router structure in backend/app/api/v1/__init__.py
- [ ] T027 [P] Implement HTTPException error handlers in backend/app/main.py
- [ ] T028 [P] Create health check endpoint in backend/app/api/v1/health.py
- [ ] T029 [P] Create Pydantic schemas for auth in backend/app/schemas/auth.py (SignUpRequest, LoginRequest, TokenResponse, UserResponse)

### Frontend Infrastructure

- [ ] T030 Create API client base in frontend/lib/api/client.ts with JWT attachment
- [ ] T031 [P] Setup TypeScript types in frontend/types/index.ts (User, AuthResponse, etc.)
- [ ] T032 [P] Create reusable UI components in frontend/components/ui/ (Button, Input, Card)
- [ ] T033 [P] Create root layout in frontend/app/layout.tsx with AuthProvider
- [ ] T034 [P] Create home page in frontend/app/page.tsx

### Security Testing (Constitution Compliance)

**⚠️ CRITICAL**: These tests MUST pass before any user story implementation

- [ ] T035 [P] Test: JWT verification rejects invalid tokens (401) in backend/tests/test_auth.py
- [ ] T036 [P] Test: JWT verification rejects expired tokens (401) in backend/tests/test_auth.py
- [ ] T037 [P] Test: Missing Authorization header returns 401 in backend/tests/test_auth.py
- [ ] T038 [P] Test: User identity extracted from JWT only (not request body) in backend/tests/test_auth.py
- [ ] T039 [P] Test: Password hashing and verification works in backend/tests/test_security.py
- [ ] T040 [P] Create pytest configuration in backend/pytest.ini
- [ ] T041 [P] Create test fixtures in backend/tests/conftest.py (test database, test client)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Signup (Priority: P1) 🎯 MVP

**Goal**: Enable new users to create accounts with email, name, and password

**Independent Test**: Create account through signup form, verify user record created, JWT token returned, can access protected routes

### Tests for User Story 1 (MANDATORY) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T042 [P] [US1] Integration test: Successful signup with valid data in backend/tests/test_auth.py
- [ ] T043 [P] [US1] Integration test: Signup with existing email returns 409 in backend/tests/test_auth.py
- [ ] T044 [P] [US1] Integration test: Signup with invalid email returns 422 in backend/tests/test_auth.py
- [ ] T045 [P] [US1] Integration test: Signup with short password returns 422 in backend/tests/test_auth.py
- [ ] T046 [P] [US1] Frontend component test: SignUpForm renders and validates in frontend/components/auth/__tests__/SignUpForm.test.tsx

### Security Tests for User Story 1 (MANDATORY - Constitution Compliance) 🔒

**Reference**: Constitution Principles IV-V (Authorization, Isolation)

- [ ] T047 [P] [US1] Test: Password is hashed before storing (never plain text) in backend/tests/test_auth.py
- [ ] T048 [P] [US1] Test: JWT token contains user_id in 'sub' claim in backend/tests/test_auth.py
- [ ] T049 [P] [US1] Test: JWT token expires in 7 days in backend/tests/test_auth.py
- [ ] T050 [P] [US1] Test: Duplicate email prevented by database constraint in backend/tests/test_auth.py
- [ ] T051 [P] [US1] Test: Generic error message for duplicate email (no enumeration) in backend/tests/test_auth.py

### Backend Implementation for User Story 1

- [ ] T052 [US1] Implement POST /api/auth/signup endpoint in backend/app/api/v1/auth.py
- [ ] T053 [US1] Add email validation in signup endpoint (format check)
- [ ] T054 [US1] Add password validation in signup endpoint (min 8 chars)
- [ ] T055 [US1] Hash password with bcrypt before storing
- [ ] T056 [US1] Create user record in database with hashed password
- [ ] T057 [US1] Generate JWT token with user_id in 'sub' claim and 7-day expiration
- [ ] T058 [US1] Return user data and JWT token in response (201 Created)
- [ ] T059 [US1] Handle duplicate email error (return 409 Conflict with generic message)
- [ ] T060 [US1] Handle validation errors (return 422 Unprocessable Entity)

### Frontend Implementation for User Story 1

- [ ] T061 [P] [US1] Create SignUpForm component in frontend/components/auth/SignUpForm.tsx
- [ ] T062 [P] [US1] Create signup page in frontend/app/(auth)/signup/page.tsx
- [ ] T063 [US1] Implement client-side validation (email format, password length)
- [ ] T064 [US1] Implement form submission with Better Auth signUp function
- [ ] T065 [US1] Handle success (store token, redirect to dashboard)
- [ ] T066 [US1] Handle errors (display validation errors, duplicate email error)
- [ ] T067 [US1] Add loading state during signup
- [ ] T068 [US1] Add link to login page for existing users

**Checkpoint**: At this point, User Story 1 should be fully functional, secure, and testable independently

---

## Phase 4: User Story 2 - User Login (Priority: P2)

**Goal**: Enable existing users to authenticate with email and password

**Independent Test**: Login with correct credentials, verify JWT token returned, can access protected routes

### Tests for User Story 2 (MANDATORY) ⚠️

- [ ] T069 [P] [US2] Integration test: Successful login with correct credentials in backend/tests/test_auth.py
- [ ] T070 [P] [US2] Integration test: Login with incorrect password returns 401 in backend/tests/test_auth.py
- [ ] T071 [P] [US2] Integration test: Login with non-existent email returns 401 in backend/tests/test_auth.py
- [ ] T072 [P] [US2] Integration test: Generic error message for failed login in backend/tests/test_auth.py
- [ ] T073 [P] [US2] Frontend component test: SignInForm renders and validates in frontend/components/auth/__tests__/SignInForm.test.tsx

### Security Tests for User Story 2 (MANDATORY - Constitution Compliance) 🔒

- [ ] T074 [P] [US2] Test: Password verification uses bcrypt compare in backend/tests/test_auth.py
- [ ] T075 [P] [US2] Test: JWT token generated on successful login in backend/tests/test_auth.py
- [ ] T076 [P] [US2] Test: Failed login attempts logged for security monitoring in backend/tests/test_auth.py
- [ ] T077 [P] [US2] Test: Generic error prevents email enumeration in backend/tests/test_auth.py

### Backend Implementation for User Story 2

- [ ] T078 [US2] Implement POST /api/auth/login endpoint in backend/app/api/v1/auth.py
- [ ] T079 [US2] Query user by email from database
- [ ] T080 [US2] Verify password using bcrypt compare
- [ ] T081 [US2] Generate JWT token on successful authentication
- [ ] T082 [US2] Return user data and JWT token (200 OK)
- [ ] T083 [US2] Return generic error for invalid credentials (401 Unauthorized)
- [ ] T084 [US2] Log failed login attempts for security monitoring
- [ ] T085 [US2] Handle validation errors (422 Unprocessable Entity)

### Frontend Implementation for User Story 2

- [ ] T086 [P] [US2] Create SignInForm component in frontend/components/auth/SignInForm.tsx
- [ ] T087 [P] [US2] Create login page in frontend/app/(auth)/login/page.tsx
- [ ] T088 [US2] Implement client-side validation (email format)
- [ ] T089 [US2] Implement form submission with Better Auth signIn function
- [ ] T090 [US2] Handle success (store token, redirect to dashboard)
- [ ] T091 [US2] Handle errors (display authentication error)
- [ ] T092 [US2] Add loading state during login
- [ ] T093 [US2] Add links to signup and password reset pages

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - User Logout (Priority: P3)

**Goal**: Enable logged-in users to end their session

**Independent Test**: Logout, verify token cleared, cannot access protected routes

### Tests for User Story 3 (MANDATORY) ⚠️

- [ ] T094 [P] [US3] Integration test: Logout clears session in backend/tests/test_auth.py
- [ ] T095 [P] [US3] Integration test: Protected route access fails after logout in backend/tests/test_auth.py
- [ ] T096 [P] [US3] Frontend test: Token cleared from storage after logout in frontend/lib/auth/__tests__/client.test.ts

### Security Tests for User Story 3 (MANDATORY - Constitution Compliance) 🔒

- [ ] T097 [P] [US3] Test: Token cleared from client storage in frontend/lib/auth/__tests__/client.test.ts
- [ ] T098 [P] [US3] Test: User redirected to login after logout in frontend/middleware.test.ts

### Backend Implementation for User Story 3

- [ ] T099 [US3] Implement POST /api/auth/logout endpoint in backend/app/api/v1/auth.py
- [ ] T100 [US3] Return success message (200 OK)
- [ ] T101 [US3] Log logout event for security monitoring

### Frontend Implementation for User Story 3

- [ ] T102 [US3] Implement logout function in frontend/lib/auth/client.ts (calls Better Auth signOut)
- [ ] T103 [US3] Clear JWT token from client storage
- [ ] T104 [US3] Redirect user to login page after logout
- [ ] T105 [US3] Add logout button to navigation/header component
- [ ] T106 [US3] Handle logout errors gracefully

**Checkpoint**: All core authentication flows (signup, login, logout) should now be independently functional

---

## Phase 6: User Story 4 - Password Reset (Priority: P4)

**Goal**: Enable users to reset forgotten passwords via email

**Independent Test**: Request password reset, receive token, use token to set new password, login with new password

### Tests for User Story 4 (OPTIONAL - P4 priority) ⚠️

- [ ] T107 [P] [US4] Integration test: Password reset request sends email in backend/tests/test_auth.py
- [ ] T108 [P] [US4] Integration test: Password reset with valid token succeeds in backend/tests/test_auth.py
- [ ] T109 [P] [US4] Integration test: Password reset with expired token fails in backend/tests/test_auth.py
- [ ] T110 [P] [US4] Integration test: Generic success message prevents enumeration in backend/tests/test_auth.py

### Security Tests for User Story 4 (MANDATORY - Constitution Compliance) 🔒

- [ ] T111 [P] [US4] Test: Reset token expires after 1 hour in backend/tests/test_auth.py
- [ ] T112 [P] [US4] Test: Reset token is single-use (invalidated after use) in backend/tests/test_auth.py
- [ ] T113 [P] [US4] Test: New password is hashed before storing in backend/tests/test_auth.py

### Backend Implementation for User Story 4

- [ ] T114 [US4] Implement POST /api/auth/password-reset/request endpoint in backend/app/api/v1/auth.py
- [ ] T115 [US4] Generate random reset token (secure random string)
- [ ] T116 [US4] Store reset token in verification_tokens table with 1-hour expiration
- [ ] T117 [US4] Send password reset email with token link (email service integration)
- [ ] T118 [US4] Return generic success message (200 OK)
- [ ] T119 [US4] Implement POST /api/auth/password-reset/confirm endpoint in backend/app/api/v1/auth.py
- [ ] T120 [US4] Verify reset token exists and not expired
- [ ] T121 [US4] Hash new password with bcrypt
- [ ] T122 [US4] Update user password in database
- [ ] T123 [US4] Invalidate reset token (delete from verification_tokens)
- [ ] T124 [US4] Return success message (200 OK)
- [ ] T125 [US4] Handle expired/invalid token errors (400 Bad Request)

### Frontend Implementation for User Story 4

- [ ] T126 [P] [US4] Create PasswordResetForm component in frontend/components/auth/PasswordResetForm.tsx
- [ ] T127 [P] [US4] Create password reset request page in frontend/app/(auth)/password-reset/page.tsx
- [ ] T128 [P] [US4] Create password reset confirm page in frontend/app/(auth)/password-reset/[token]/page.tsx
- [ ] T129 [US4] Implement reset request form (email input)
- [ ] T130 [US4] Implement reset confirm form (new password input with confirmation)
- [ ] T131 [US4] Handle success messages
- [ ] T132 [US4] Handle errors (expired token, validation errors)
- [ ] T133 [US4] Add password strength indicator
- [ ] T134 [US4] Add links back to login page

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Protected Routes & Dashboard

**Purpose**: Implement protected routes and basic dashboard

- [ ] T135 [P] Create dashboard layout in frontend/app/(dashboard)/layout.tsx
- [ ] T136 [P] Create dashboard home page in frontend/app/(dashboard)/page.tsx
- [ ] T137 [P] Implement ProtectedRoute wrapper in frontend/components/auth/ProtectedRoute.tsx
- [ ] T138 [US1-3] Test: Unauthenticated users redirected to login in frontend/middleware.test.ts
- [ ] T139 [US1-3] Test: Authenticated users can access dashboard in frontend/middleware.test.ts
- [ ] T140 [P] Create GET /api/auth/me endpoint in backend/app/api/v1/auth.py (returns current user)
- [ ] T141 [P] Test: /api/auth/me requires valid JWT in backend/tests/test_auth.py
- [ ] T142 [P] Test: /api/auth/me returns current user data in backend/tests/test_auth.py

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final security validation

### Security Validation (Constitution Compliance) 🔒

**Reference**: Constitution v1.0.0 - All Principles

**⚠️ MANDATORY**: These checks MUST pass before deployment

- [ ] T143 [P] Verify all protected endpoints require JWT authentication
- [ ] T144 [P] Verify user identity extracted from JWT only (never request body)
- [ ] T145 [P] Verify all database queries filter by authenticated user_id (when applicable)
- [ ] T146 [P] Verify ownership checks before update/delete operations (when applicable)
- [ ] T147 [P] Verify cross-user data isolation (User A cannot access User B's data)
- [ ] T148 [P] Verify correct HTTP status codes (401, 403, 404) returned
- [ ] T149 [P] Verify JWT secrets not logged or exposed
- [ ] T150 [P] Run security test suite across all user stories
- [ ] T151 [P] Verify password hashing (100% coverage, zero plain text)
- [ ] T152 [P] Verify rate limiting configured (10 req/min on auth endpoints)

### API Contract Validation (Constitution Principle VI)

- [ ] T153 [P] Verify RESTful endpoint conventions followed
- [ ] T154 [P] Verify API documentation complete and accurate
- [ ] T155 [P] Verify error responses consistent across endpoints
- [ ] T156 [P] Test all endpoints with invalid/expired JWT tokens

### Code Quality & Documentation

- [ ] T157 [P] Update README.md with authentication setup instructions
- [ ] T158 [P] Document environment variables in .env.example files
- [ ] T159 [P] Create API documentation (OpenAPI/Swagger)
- [ ] T160 Code cleanup and refactoring
- [ ] T161 Performance optimization (if needed)
- [ ] T162 [P] Add JSDoc comments to frontend functions
- [ ] T163 [P] Add docstrings to backend functions

### Deployment Readiness

- [ ] T164 [P] Environment variables documented and configured for production
- [ ] T165 [P] Database migrations tested and ready
- [ ] T166 [P] CORS configuration verified for production origin
- [ ] T167 [P] Rate limiting configured and tested
- [ ] T168 [P] Logging and monitoring setup verified
- [ ] T169 [P] HTTPS enforcement verified (production only)
- [ ] T170 [P] Create deployment guide in docs/

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Protected Routes (Phase 7)**: Depends on US1-US3 completion
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1 - Signup)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2 - Login)**: Can start after Foundational (Phase 2) - Independent of US1 but typically follows
- **User Story 3 (P3 - Logout)**: Can start after Foundational (Phase 2) - Independent but requires auth context
- **User Story 4 (P4 - Password Reset)**: Can start after Foundational (Phase 2) - Independent, optional for MVP

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Backend implementation before frontend integration
- Security tests MUST pass before moving to next story
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Backend and frontend tasks within a story can run in parallel (different developers)
- Different user stories can be worked on in parallel by different team members

---

## Implementation Strategy

### MVP First (User Stories 1-3 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Signup)
4. Complete Phase 4: User Story 2 (Login)
5. Complete Phase 5: User Story 3 (Logout)
6. Complete Phase 7: Protected Routes & Dashboard
7. **STOP and VALIDATE**: Test all authentication flows
8. Complete Phase 8: Security validation and polish
9. Deploy/demo MVP

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Signup) → Test independently → Deploy/Demo
3. Add User Story 2 (Login) → Test independently → Deploy/Demo
4. Add User Story 3 (Logout) → Test independently → Deploy/Demo
5. Add Protected Routes → Test → Deploy/Demo (MVP complete!)
6. Add User Story 4 (Password Reset) → Test → Deploy/Demo (optional enhancement)

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Signup) - Backend + Frontend
   - Developer B: User Story 2 (Login) - Backend + Frontend
   - Developer C: User Story 3 (Logout) + Protected Routes
3. Stories complete and integrate independently
4. Team validates security together (Phase 8)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Security tests are MANDATORY (not optional) for this feature
- Password reset (US4) is P4 priority - can be deferred for MVP
- All constitution principles must be verified in Phase 8

---

## Task Summary

**Total Tasks**: 170 tasks
- Phase 1 (Setup): 7 tasks
- Phase 2 (Foundational): 34 tasks (including 7 security tests)
- Phase 3 (US1 - Signup): 27 tasks (including 10 tests)
- Phase 4 (US2 - Login): 25 tasks (including 9 tests)
- Phase 5 (US3 - Logout): 13 tasks (including 5 tests)
- Phase 6 (US4 - Password Reset): 28 tasks (including 7 tests) - OPTIONAL for MVP
- Phase 7 (Protected Routes): 8 tasks
- Phase 8 (Polish & Security): 28 tasks

**MVP Tasks** (excluding US4): 142 tasks
**Full Feature Tasks** (including US4): 170 tasks

**Estimated Effort**:
- MVP: 3-4 weeks (1 developer) or 1-2 weeks (2-3 developers in parallel)
- Full Feature: 4-5 weeks (1 developer) or 2-3 weeks (2-3 developers in parallel)
