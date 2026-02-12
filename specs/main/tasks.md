---
description: "Backend implementation tasks for Full-Stack Todo Application"
---

# Tasks: Backend API (FastAPI + SQLModel + Neon PostgreSQL)

**Input**: Design documents from `/specs/main/`
**Prerequisites**: plan.md, data-model.md, contracts/ (auth-api.yaml, todos-api.yaml)

**Scope**: Backend API only - FastAPI with JWT authentication, SQLModel ORM, Neon PostgreSQL

**Tests**: Not included (not explicitly requested in specification)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each API endpoint.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Backend: `backend/app/` for application code
- Tests: `backend/tests/` for test files
- Migrations: `backend/alembic/` for database migrations

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend project structure with app/, tests/, alembic/ directories
- [x] T002 Initialize Python virtual environment and install FastAPI, SQLModel, python-jose, bcrypt, uvicorn dependencies in backend/requirements.txt
- [x] T003 [P] Create backend/.env.example with DATABASE_URL, BETTER_AUTH_SECRET, ALLOWED_ORIGINS, DEBUG placeholders
- [x] T004 [P] Create backend/README.md with setup instructions and API documentation links

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create application settings configuration in backend/app/config.py with Pydantic BaseSettings for environment variables
- [x] T006 [P] Setup database connection and session management in backend/app/database.py with SQLModel engine and session factory
- [x] T007 [P] Initialize Alembic for database migrations in backend/alembic/ with env.py configuration
- [x] T008 Create User model in backend/app/models/user.py with id, email, name, hashed_password, created_at, updated_at fields
- [x] T009 [P] Create Todo model in backend/app/models/todo.py with id, title, description, completed, user_id, created_at, updated_at fields
- [x] T010 Create initial Alembic migration for users and todos tables in backend/alembic/versions/
- [x] T011 Implement password hashing utilities in backend/app/core/security.py with bcrypt (cost factor 12)
- [x] T012 Implement JWT verification function in backend/app/core/auth.py using python-jose with BETTER_AUTH_SECRET
- [x] T013 Implement get_current_user dependency in backend/app/core/auth.py to extract user_id from JWT token
- [x] T014 Create FastAPI application instance in backend/app/main.py with CORS middleware configuration
- [x] T015 [P] Setup global exception handlers in backend/app/main.py for RequestValidationError (422), IntegrityError (409), and general exceptions (500)
- [x] T016 [P] Create shared database session dependency in backend/app/api/deps.py
- [x] T017 Create API v1 router in backend/app/api/v1/__init__.py with health check endpoint

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable users to create accounts, login, and logout with JWT-based authentication

**Independent Test**: Create account via POST /api/v1/auth/signup, login via POST /api/v1/auth/login, verify JWT token is returned, logout via POST /api/v1/auth/logout

**Backend Endpoints**: POST /auth/signup, POST /auth/login, POST /auth/logout

### Implementation for User Story 1

- [x] T018 [P] [US1] Create UserCreate schema in backend/app/schemas/user.py with email, password, name validation (email format, password min 8 chars)
- [x] T019 [P] [US1] Create UserResponse schema in backend/app/schemas/user.py with id, email, name fields (no password)
- [x] T020 [P] [US1] Create LoginRequest schema in backend/app/schemas/user.py with email and password fields
- [x] T021 [P] [US1] Create AuthResponse schema in backend/app/schemas/user.py with user and token fields
- [x] T022 [US1] Implement POST /api/v1/auth/signup endpoint in backend/app/api/v1/auth.py to create user with hashed password and return JWT token
- [x] T023 [US1] Add email uniqueness check in signup endpoint returning 409 Conflict if email exists
- [x] T024 [US1] Implement POST /api/v1/auth/login endpoint in backend/app/api/v1/auth.py to verify credentials and return JWT token
- [x] T025 [US1] Add password verification in login endpoint returning 401 Unauthorized for invalid credentials
- [x] T026 [US1] Implement POST /api/v1/auth/logout endpoint in backend/app/api/v1/auth.py requiring JWT authentication
- [x] T027 [US1] Include auth router in main API router in backend/app/api/v1/__init__.py with /auth prefix

**Checkpoint**: At this point, User Story 1 should be fully functional - users can signup, login, and logout with JWT tokens

---

## Phase 4: User Story 2 - View Personal Task List (Priority: P1)

**Goal**: Enable authenticated users to retrieve all their todos

**Independent Test**: Authenticate as user, call GET /api/v1/todos, verify only user's todos are returned (test with multiple users to ensure isolation)

**Backend Endpoints**: GET /todos

### Implementation for User Story 2

- [x] T028 [P] [US2] Create TodoResponse schema in backend/app/schemas/todo.py with id, title, description, completed, user_id, created_at, updated_at fields
- [x] T029 [US2] Implement GET /api/v1/todos endpoint in backend/app/api/v1/todos.py to list all todos filtered by authenticated user_id
- [x] T030 [US2] Add JWT authentication requirement using get_current_user dependency in GET /todos endpoint
- [x] T031 [US2] Ensure query filters by user_id from JWT token (never from request body) returning 401 for missing/invalid token
- [x] T032 [US2] Include todos router in main API router in backend/app/api/v1/__init__.py with /todos prefix

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - users can authenticate and view their todo list

---

## Phase 5: User Story 3 - Create New Task (Priority: P1)

**Goal**: Enable authenticated users to create new todos

**Independent Test**: Authenticate as user, call POST /api/v1/todos with title and optional description, verify todo is created with user_id from token

**Backend Endpoints**: POST /todos

### Implementation for User Story 3

- [x] T033 [P] [US3] Create TodoCreate schema in backend/app/schemas/todo.py with title (required, 1-200 chars) and description (optional, max 1000 chars) validation
- [x] T034 [US3] Implement POST /api/v1/todos endpoint in backend/app/api/v1/todos.py to create todo with user_id from JWT token
- [x] T035 [US3] Add JWT authentication requirement using get_current_user dependency in POST /todos endpoint
- [x] T036 [US3] Set user_id from authenticated user (never from request body) and return 401 for missing/invalid token
- [x] T037 [US3] Add input validation returning 422 Unprocessable Entity for invalid title/description
- [x] T038 [US3] Return 201 Created status with created todo in response

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently - users can authenticate, view todos, and create new todos

---

## Phase 6: User Story 4 - View Single Task Details (Priority: P2)

**Goal**: Enable authenticated users to retrieve a specific todo by ID

**Independent Test**: Authenticate as user, create a todo, call GET /api/v1/todos/{id}, verify todo details are returned; test with another user's todo ID to verify 404 response

**Backend Endpoints**: GET /todos/{id}

### Implementation for User Story 4

- [x] T039 [US4] Implement GET /api/v1/todos/{id} endpoint in backend/app/api/v1/todos.py to retrieve single todo by ID
- [x] T040 [US4] Add JWT authentication requirement using get_current_user dependency in GET /todos/{id} endpoint
- [x] T041 [US4] Add ownership verification: query filters by both id AND user_id from JWT token
- [x] T042 [US4] Return 404 Not Found if todo doesn't exist or doesn't belong to authenticated user (don't reveal existence)
- [x] T043 [US4] Return 401 Unauthorized for missing/invalid token

**Checkpoint**: At this point, User Stories 1-4 should all work independently - users can view individual todo details with ownership enforcement

---

## Phase 7: User Story 5 - Update Existing Task (Priority: P2)

**Goal**: Enable authenticated users to update their todos

**Independent Test**: Authenticate as user, create a todo, call PUT /api/v1/todos/{id} with updated data, verify changes are persisted; test with another user's todo ID to verify 403/404 response

**Backend Endpoints**: PUT /todos/{id}

### Implementation for User Story 5

- [x] T044 [P] [US5] Create TodoUpdate schema in backend/app/schemas/todo.py with optional title, description, completed fields (all optional for partial updates)
- [x] T045 [US5] Implement PUT /api/v1/todos/{id} endpoint in backend/app/api/v1/todos.py to update todo
- [x] T046 [US5] Add JWT authentication requirement using get_current_user dependency in PUT /todos/{id} endpoint
- [x] T047 [US5] Add ownership verification: fetch todo by id AND user_id, return 404 if not found or not owned
- [x] T048 [US5] Update todo fields with validated input returning 422 for validation errors
- [x] T049 [US5] Update updated_at timestamp to current UTC time
- [x] T050 [US5] Return 401 Unauthorized for missing/invalid token, 403 Forbidden for user mismatch

**Checkpoint**: At this point, User Stories 1-5 should all work independently - users can update their todos with ownership enforcement

---

## Phase 8: User Story 6 - Delete Task (Priority: P2)

**Goal**: Enable authenticated users to delete their todos

**Independent Test**: Authenticate as user, create a todo, call DELETE /api/v1/todos/{id}, verify todo is removed; test with another user's todo ID to verify 403/404 response

**Backend Endpoints**: DELETE /todos/{id}

### Implementation for User Story 6

- [x] T051 [US6] Implement DELETE /api/v1/todos/{id} endpoint in backend/app/api/v1/todos.py to delete todo
- [x] T052 [US6] Add JWT authentication requirement using get_current_user dependency in DELETE /todos/{id} endpoint
- [x] T053 [US6] Add ownership verification: fetch todo by id AND user_id, return 404 if not found or not owned
- [x] T054 [US6] Delete todo from database and return 200 OK with success message
- [x] T055 [US6] Return 401 Unauthorized for missing/invalid token, 403 Forbidden for user mismatch

**Checkpoint**: At this point, User Stories 1-6 should all work independently - users can delete their todos with ownership enforcement

---

## Phase 9: User Story 7 - Toggle Task Completion (Priority: P2)

**Goal**: Enable authenticated users to toggle todo completion status

**Independent Test**: Authenticate as user, create a todo, call PATCH /api/v1/todos/{id}/toggle, verify completed status is toggled; call again to verify it toggles back

**Backend Endpoints**: PATCH /todos/{id}/toggle

### Implementation for User Story 7

- [x] T056 [US7] Implement PATCH /api/v1/todos/{id}/toggle endpoint in backend/app/api/v1/todos.py to toggle completed status
- [x] T057 [US7] Add JWT authentication requirement using get_current_user dependency in PATCH /todos/{id}/toggle endpoint
- [x] T058 [US7] Add ownership verification: fetch todo by id AND user_id, return 404 if not found or not owned
- [x] T059 [US7] Toggle completed field (False → True or True → False) and update updated_at timestamp
- [x] T060 [US7] Return updated todo with new completed status
- [x] T061 [US7] Return 401 Unauthorized for missing/invalid token, 403 Forbidden for user mismatch

**Checkpoint**: All user stories should now be independently functional - complete backend API with authentication and CRUD operations

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T062 [P] Add comprehensive logging for all authentication operations in backend/app/core/auth.py (never log tokens or passwords)
- [x] T063 [P] Add comprehensive logging for all todo operations in backend/app/api/v1/todos.py with timestamps
- [x] T064 [P] Verify all error responses follow consistent format with detail field
- [x] T065 [P] Add API documentation strings (docstrings) to all endpoints for OpenAPI/Swagger docs
- [x] T066 [P] Verify CORS configuration restricts to frontend origin only in backend/app/main.py
- [x] T067 [P] Add rate limiting consideration documentation for auth endpoints in backend/README.md
- [x] T068 [P] Create backend/DEPLOYMENT.md with production deployment checklist (HTTPS, secrets, CORS, etc.)
- [x] T069 Verify all endpoints return correct HTTP status codes per API contracts (401, 403, 404, 422, 500)
- [x] T070 Run manual integration test following backend/README.md quickstart guide
- [x] T071 [P] Update backend/README.md with all implemented endpoints and example requests
- [x] T072 [P] Document environment variables and their purposes in backend/.env.example

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-9)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P2)
- **Polish (Phase 10)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1) - Authentication**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1) - List Todos**: Depends on US1 for authentication - Can start after US1 complete
- **User Story 3 (P1) - Create Todo**: Depends on US1 for authentication - Can start after US1 complete
- **User Story 4 (P2) - Get Todo**: Depends on US1 for authentication - Can start after US1 complete
- **User Story 5 (P2) - Update Todo**: Depends on US1 for authentication - Can start after US1 complete
- **User Story 6 (P2) - Delete Todo**: Depends on US1 for authentication - Can start after US1 complete
- **User Story 7 (P2) - Toggle Todo**: Depends on US1 for authentication - Can start after US1 complete

**Note**: US2-US7 all depend on US1 (authentication) but are otherwise independent of each other

### Within Each User Story

- Schemas before endpoints (schemas define request/response structure)
- Authentication middleware before protected endpoints
- Ownership verification before data operations
- Input validation before database operations
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003, T004)
- All Foundational tasks marked [P] can run in parallel within Phase 2 (T006, T007, T009, T015, T016)
- Once US1 (Authentication) completes, US2-US7 can start in parallel (if team capacity allows)
- All schemas within a story marked [P] can run in parallel
- All Polish tasks marked [P] can run in parallel (T062-T068, T071-T072)

---

## Parallel Example: User Story 1 (Authentication)

```bash
# Launch all schemas for User Story 1 together:
Task: "Create UserCreate schema in backend/app/schemas/user.py"
Task: "Create UserResponse schema in backend/app/schemas/user.py"
Task: "Create LoginRequest schema in backend/app/schemas/user.py"
Task: "Create AuthResponse schema in backend/app/schemas/user.py"

# Then implement endpoints sequentially (they share the same file):
Task: "Implement POST /api/v1/auth/signup endpoint"
Task: "Implement POST /api/v1/auth/login endpoint"
Task: "Implement POST /api/v1/auth/logout endpoint"
```

---

## Parallel Example: After US1 Complete

```bash
# Once authentication is working, these can all start in parallel:
Task: "Implement GET /api/v1/todos endpoint" (US2)
Task: "Implement POST /api/v1/todos endpoint" (US3)
Task: "Implement GET /api/v1/todos/{id} endpoint" (US4)
Task: "Implement PUT /api/v1/todos/{id} endpoint" (US5)
Task: "Implement DELETE /api/v1/todos/{id} endpoint" (US6)
Task: "Implement PATCH /api/v1/todos/{id}/toggle endpoint" (US7)
```

---

## Implementation Strategy

### MVP First (User Stories 1-3 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Authentication)
4. Complete Phase 4: User Story 2 (List Todos)
5. Complete Phase 5: User Story 3 (Create Todo)
6. **STOP and VALIDATE**: Test authentication + list + create independently
7. Deploy/demo if ready - this is a functional MVP!

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Auth) → Test independently → Deploy/Demo
3. Add User Story 2 (List) → Test independently → Deploy/Demo
4. Add User Story 3 (Create) → Test independently → Deploy/Demo (MVP!)
5. Add User Story 4 (Get) → Test independently → Deploy/Demo
6. Add User Story 5 (Update) → Test independently → Deploy/Demo
7. Add User Story 6 (Delete) → Test independently → Deploy/Demo
8. Add User Story 7 (Toggle) → Test independently → Deploy/Demo
9. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Developer A: User Story 1 (Authentication) - MUST complete first
3. Once US1 is done, split remaining stories:
   - Developer A: User Stories 2, 3 (List, Create)
   - Developer B: User Stories 4, 5 (Get, Update)
   - Developer C: User Stories 6, 7 (Delete, Toggle)
4. Stories complete and integrate independently

---

## Security Checklist

**CRITICAL**: Verify these security requirements are met:

- [x] ✅ SR-001: Passwords hashed with bcrypt (cost factor 12) before storage
- [x] ✅ SR-002: JWT tokens sent in Authorization: Bearer <token> header
- [x] ✅ SR-003: Backend verifies JWT tokens using BETTER_AUTH_SECRET
- [x] ✅ SR-004: Invalid/missing tokens return 401 Unauthorized
- [x] ✅ SR-005: JWT secrets NEVER logged or exposed
- [x] ✅ SR-006: User identity extracted from JWT only (never from request body)
- [x] ✅ AR-001: All database queries filter by authenticated user_id
- [x] ✅ AR-002: Ownership verification before any update/delete operation
- [x] ✅ AR-003: User mismatch returns 403 Forbidden
- [x] ✅ AR-004: Non-existent or unauthorized resources return 404 Not Found
- [x] ✅ AC-001: RESTful API design with proper HTTP methods
- [x] ✅ AC-002: Consistent error responses with status codes
- [x] ✅ AC-003: CORS restricted to frontend origin only
- [x] ✅ AC-004: API versioning with /api/v1 prefix

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- All endpoints require JWT authentication except /auth/signup and /auth/login
- User isolation enforced at query level (filter by user_id from token)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Total Task Count

- **Setup**: 4 tasks
- **Foundational**: 13 tasks (BLOCKING)
- **User Story 1 (Auth)**: 10 tasks
- **User Story 2 (List)**: 5 tasks
- **User Story 3 (Create)**: 6 tasks
- **User Story 4 (Get)**: 5 tasks
- **User Story 5 (Update)**: 7 tasks
- **User Story 6 (Delete)**: 5 tasks
- **User Story 7 (Toggle)**: 6 tasks
- **Polish**: 11 tasks

**Total**: 72 tasks

**MVP Scope** (Recommended): Phases 1-5 (User Stories 1-3) = 38 tasks
