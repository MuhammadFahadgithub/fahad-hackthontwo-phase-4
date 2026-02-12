# Tasks: Frontend Phase 2 Web Application (FAST)

**Input**: Design documents from `/specs/001-frontend-phase2/`
**Prerequisites**: plan.md, spec.md

**Organization**: Tasks organized by implementation phases for incremental GitHub pushes with git tags.

**Tests**: Optional - not included in this fast execution plan unless explicitly requested.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US7)
- Include exact file paths in descriptions

---

## Phase 1: Repository Setup & Skeleton 🏗️

**Purpose**: Initialize monorepo structure with minimal files for first commit

**Git Tag**: `phase-1-setup`

- [X] T001 Create monorepo folder structure: frontend/, backend/, specs/
- [X] T002 Create root .gitignore with node_modules, .env*, __pycache__, .venv
- [X] T003 [P] Create frontend/.env.example with NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET, BETTER_AUTH_URL
- [X] T004 [P] Create backend/.env.example with DATABASE_URL, BETTER_AUTH_SECRET, CORS_ORIGINS, JWT_ALGORITHM
- [X] T005 Create root README.md with project overview and setup instructions placeholder
- [X] T006 [P] Create frontend/package.json with Next.js 16+, TypeScript, Tailwind CSS, Better Auth dependencies
- [X] T007 [P] Create backend/requirements.txt with fastapi, sqlmodel, pyjwt, python-jose, psycopg2-binary, uvicorn
- [X] T008 Commit and push with tag phase-1-setup

**Checkpoint**: Repository structure ready, dependencies defined, ready for Phase 2

---

## Phase 2: Backend Database & Models 🗄️

**Purpose**: Setup Neon PostgreSQL connection and SQLModel Task model

**Git Tag**: `phase-2-backend-db`

**Dependencies**: Phase 1 complete

- [X] T009 Create backend/src/__init__.py (empty file for Python package)
- [X] T010 Create backend/src/database.py with Neon connection string from DATABASE_URL and SQLModel engine setup
- [X] T011 [P] Create backend/src/models/__init__.py
- [X] T012 [P] Create backend/src/models/task.py with Task SQLModel (id, title, description, completed, user_id, created_at, updated_at)
- [X] T013 Create backend/src/main.py with FastAPI app initialization and database startup (create_all tables)
- [X] T014 Test database connectivity by running uvicorn and checking logs for successful connection
- [X] T015 Commit and push with tag phase-2-backend-db

**Checkpoint**: Database connected, Task table created, FastAPI app runs

---

## Phase 3: Backend JWT Authentication 🔐

**Purpose**: Implement JWT verification and user_id enforcement

**Git Tag**: `phase-3-backend-api`

**Dependencies**: Phase 2 complete

**Maps to**: User Story 1 (User Authentication) - Backend part

- [X] T016 [P] Create backend/src/middleware/__init__.py
- [X] T017 Create backend/src/middleware/auth.py with JWT decode function using BETTER_AUTH_SECRET and HS256 algorithm
- [X] T018 Add get_current_user dependency in backend/src/middleware/auth.py that extracts Bearer token and returns user_id
- [X] T019 Add verify_user_id_match function in backend/src/middleware/auth.py that compares token user_id with path user_id (raises 403 if mismatch)
- [X] T020 Update backend/src/main.py to add CORS middleware with CORS_ORIGINS from environment
- [X] T021 Commit and push with tag phase-3-backend-api

**Checkpoint**: JWT verification working, user_id enforcement ready, CORS configured

---

## Phase 4: Backend CRUD Endpoints 📡

**Purpose**: Implement all task CRUD operations with ownership filtering

**Git Tag**: `phase-4-backend-crud`

**Dependencies**: Phase 3 complete

**Maps to**: User Stories 2-7 (All task operations) - Backend part

### Task List & Create (US2, US3)

- [X] T022 [P] Create backend/src/api/__init__.py
- [X] T023 [P] Create backend/src/api/tasks.py with APIRouter for /api/users/{user_id}/tasks
- [X] T024 [US2] Implement GET /api/users/{user_id}/tasks endpoint with JWT required, user_id match check, filter by user_id
- [X] T025 [US3] Implement POST /api/users/{user_id}/tasks endpoint with JWT required, user_id match check, create task with user_id from token

### Task Detail, Update, Delete (US4, US5, US6)

- [X] T026 [US4] Implement GET /api/users/{user_id}/tasks/{task_id} endpoint with JWT required, ownership check (404 if not found or not owned)
- [X] T027 [US5] Implement PUT /api/users/{user_id}/tasks/{task_id} endpoint with JWT required, ownership check, update only owned tasks
- [X] T028 [US6] Implement DELETE /api/users/{user_id}/tasks/{task_id} endpoint with JWT required, ownership check, delete only owned tasks

### Task Toggle Completion (US7)

- [X] T029 [US7] Implement PATCH /api/users/{user_id}/tasks/{task_id}/toggle endpoint with JWT required, ownership check, toggle completed field

### Integration & Error Handling

- [X] T030 Update backend/src/main.py to include tasks router with prefix /api
- [X] T031 Add proper error responses: 401 for missing/invalid token, 403 for user_id mismatch, 404 for not found, 500 for server errors
- [X] T032 Test all endpoints with curl or Postman: verify JWT required, user isolation, proper status codes
- [X] T033 Commit and push with tag phase-4-backend-crud

**Checkpoint**: All backend CRUD endpoints working, user isolation enforced, ready for frontend

---

## Phase 5: Frontend Authentication & Task UI 🎨

**Purpose**: Setup Better Auth and build complete task management UI

**Git Tag**: `phase-5-frontend-complete`

**Dependencies**: Phase 4 complete (backend API available)

**Maps to**: User Stories 1-7 (All features) - Frontend part

### Project Setup & Better Auth (US1)

- [X] T034 Initialize Next.js 16+ project in frontend/ with TypeScript and Tailwind CSS (npx create-next-app@latest)
- [X] T035 Install Better Auth: npm install better-auth
- [X] T036 [P] Create frontend/src/lib/auth/better-auth.ts with Better Auth configuration (JWT secret, session settings)
- [X] T037 [P] Create frontend/src/lib/types/user.ts with User interface (id, email, name)
- [X] T038 [P] Create frontend/src/lib/types/task.ts with Task interface (id, title, description, completed, user_id, created_at, updated_at)

### API Client (All User Stories)

- [X] T039 [P] Create frontend/src/lib/api/client.ts with base API client that attaches JWT from Better Auth to Authorization header
- [X] T040 [P] Create frontend/src/lib/api/auth.ts with signUp and signIn functions calling Better Auth
- [X] T041 [P] Create frontend/src/lib/api/tasks.ts with getTasks, getTask, createTask, updateTask, deleteTask, toggleTaskCompletion functions

### Authentication Pages (US1)

- [X] T042 [US1] Create frontend/src/app/(auth)/signup/page.tsx with signup form (email, password, name)
- [X] T043 [US1] Create frontend/src/app/(auth)/signin/page.tsx with signin form (email, password)
- [X] T044 [US1] Create frontend/src/components/auth/AuthGuard.tsx that checks session and redirects to /signin if not authenticated
- [X] T045 [US1] Create frontend/src/components/layout/Navbar.tsx with user info and logout button

### Task List & Create (US2, US3)

- [X] T046 [US2] Create frontend/src/app/(protected)/tasks/page.tsx with task list view, empty state, loading state
- [X] T047 [US2] Create frontend/src/components/tasks/TaskList.tsx component to display array of tasks
- [X] T048 [US2] Create frontend/src/components/tasks/TaskItem.tsx component for individual task display with completion toggle
- [X] T049 [US3] Create frontend/src/app/(protected)/tasks/new/page.tsx with task creation form
- [X] T050 [US3] Create frontend/src/components/tasks/TaskForm.tsx reusable form component for create/edit

### Task Detail, Update, Delete (US4, US5, US6)

- [X] T051 [US4] Create frontend/src/app/(protected)/tasks/[id]/page.tsx with task detail view
- [X] T052 [US5] Create frontend/src/app/(protected)/tasks/[id]/edit/page.tsx with task edit form using TaskForm component
- [X] T053 [US6] Add delete button to task detail page with confirmation dialog

### Task Toggle (US7)

- [X] T054 [US7] Add toggle completion checkbox to TaskItem component that calls toggleTaskCompletion API

### Layout & Error Handling

- [X] T055 [P] Create frontend/src/components/ui/LoadingState.tsx component for loading indicators
- [X] T056 [P] Create frontend/src/components/ui/ErrorState.tsx component for error messages
- [X] T057 Create frontend/src/app/layout.tsx with root layout including Navbar and AuthGuard for protected routes
- [X] T058 Update frontend/src/app/page.tsx to redirect authenticated users to /tasks, unauthenticated to /signin

### Testing & Validation

- [X] T059 Test complete user flow: signup → signin → create task → view list → edit task → toggle completion → delete task
- [X] T060 Test user isolation: create two users, verify each sees only their own tasks
- [X] T061 Test error handling: invalid credentials, network errors, unauthorized access attempts
- [X] T062 Commit and push with tag phase-5-frontend-complete

**Checkpoint**: Full application working end-to-end, all user stories functional

---

## Phase 6: Final Polish & Documentation 🎯

**Purpose**: CORS configuration, validations, documentation, optional tests

**Git Tag**: `phase-6-complete`

**Dependencies**: Phase 5 complete

- [X] T063 [P] Add input validation to backend endpoints: title max 200 chars, required fields
- [X] T064 [P] Add client-side form validation to frontend forms: required fields, max lengths
- [X] T065 Update root README.md with complete setup instructions: prerequisites, environment setup, running locally
- [X] T066 [P] Create backend/README.md with backend-specific setup and API documentation
- [X] T067 [P] Create frontend/README.md with frontend-specific setup and component documentation
- [X] T068 [P] Add error logging to backend for debugging (structured logging with timestamps)
- [X] T069 Test all edge cases: session expiration, network failures, concurrent edits, malformed requests
- [X] T070 [OPTIONAL] Create backend/tests/test_tasks.py with basic unit tests for task endpoints
- [X] T071 [OPTIONAL] Create smoke test checklist in TESTING.md for manual validation
- [X] T072 Final commit and push with tag phase-6-complete

**Checkpoint**: Production-ready application with documentation and validation

---

## Dependencies & Execution Order

### Phase Dependencies (Sequential)

1. **Phase 1: Repository Setup** → No dependencies
2. **Phase 2: Backend DB & Models** → Depends on Phase 1
3. **Phase 3: Backend JWT Auth** → Depends on Phase 2
4. **Phase 4: Backend CRUD** → Depends on Phase 3
5. **Phase 5: Frontend** → Depends on Phase 4 (needs backend API)
6. **Phase 6: Polish** → Depends on Phase 5

### Within Each Phase

- Tasks marked [P] can run in parallel (different files)
- Tasks without [P] should run sequentially (dependencies on previous tasks)
- All tasks within a phase must complete before moving to next phase

### User Story Mapping

- **US1 (User Authentication)**: T016-T021 (backend), T034-T045 (frontend)
- **US2 (View Task List)**: T024 (backend), T046-T048 (frontend)
- **US3 (Create Task)**: T025 (backend), T049-T050 (frontend)
- **US4 (View Task Detail)**: T026 (backend), T051 (frontend)
- **US5 (Update Task)**: T027 (backend), T052 (frontend)
- **US6 (Delete Task)**: T028 (backend), T053 (frontend)
- **US7 (Toggle Completion)**: T029 (backend), T054 (frontend)

---

## Parallel Opportunities

### Phase 1 (Setup)
- T003, T004 (env files) can run in parallel
- T006, T007 (dependency files) can run in parallel

### Phase 2 (Backend DB)
- T011, T012 (model files) can run in parallel

### Phase 3 (Backend Auth)
- T016, T017 (initial auth files) can run in parallel

### Phase 5 (Frontend)
- T036, T037, T038 (type definitions) can run in parallel
- T039, T040, T041 (API client files) can run in parallel
- T055, T056 (UI components) can run in parallel

### Phase 6 (Polish)
- T063, T064 (validation) can run in parallel
- T066, T067 (documentation) can run in parallel
- T068, T070, T071 (testing/logging) can run in parallel

---

## Implementation Strategy

### Incremental GitHub Pushes

1. **After Phase 1**: Push with tag `phase-1-setup` → Repository structure visible
2. **After Phase 2**: Push with tag `phase-2-backend-db` → Database working
3. **After Phase 3**: Push with tag `phase-3-backend-api` → Auth working
4. **After Phase 4**: Push with tag `phase-4-backend-crud` → Backend complete
5. **After Phase 5**: Push with tag `phase-5-frontend-complete` → Full app working
6. **After Phase 6**: Push with tag `phase-6-complete` → Production ready

### MVP Scope (Minimum Viable Product)

**Phases 1-5 = MVP**: Complete authenticated multi-user task management application

**Phase 6 = Polish**: Optional improvements and hardening

### Testing Strategy

- **After Phase 2**: Test database connection (T014)
- **After Phase 4**: Test all backend endpoints with curl/Postman (T032)
- **After Phase 5**: Test complete user flows (T059-T061)
- **After Phase 6**: Test edge cases and run optional tests (T069-T071)

---

## Critical Path

1. T001-T008: Setup repository structure
2. T009-T015: Setup database and models
3. T016-T021: Implement JWT authentication
4. T022-T033: Implement all CRUD endpoints
5. T034-T062: Build complete frontend
6. T063-T072: Polish and document

**Total Tasks**: 72 tasks across 6 phases

**Estimated Completion**:
- Phase 1: 1-2 hours
- Phase 2: 2-3 hours
- Phase 3: 2-3 hours
- Phase 4: 4-6 hours
- Phase 5: 8-12 hours
- Phase 6: 2-4 hours

---

## Notes

- Each phase ends with a git tag for tracking progress
- Tasks are small and specific for incremental commits
- [P] tasks can be parallelized if multiple developers available
- User story labels [US1-US7] map tasks to specification requirements
- Backend must be complete (Phase 4) before starting frontend (Phase 5)
- Tests are optional (T070-T071) - include if time permits
- Focus on MVP (Phases 1-5) first, then polish (Phase 6)
- Each phase checkpoint validates functionality before proceeding
