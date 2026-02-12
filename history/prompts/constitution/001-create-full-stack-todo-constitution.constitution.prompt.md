---
id: 001
title: Create Full-Stack Todo Constitution
stage: constitution
date: 2026-02-06
surface: agent
model: claude-sonnet-4-5
feature: none
branch: master
user: Zaib's
command: /sp.constitution
labels: ["constitution", "security", "authentication", "spec-driven"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (documentation only)
---

## Prompt

sp.constitution — Full-Stack Todo Web Application (Phase 2)

ROLE
You are a Full-Stack Developer working on a multi-user Todo web application.
You must follow Spec-Kit Plus and Claude Code for spec-driven development.

Tech Stack:
- Frontend: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (Frontend) + JWT (Backend)
- Workflow: Spec-Kit Plus + Claude Code

--------------------------------------------------

GOLDEN RULES (MANDATORY)

1. SPEC FIRST DEVELOPMENT
- Always read relevant specs before coding.
- Reference specs using Spec-Kit paths:
  @specs/features/task-crud.md
  @specs/features/authentication.md
  @specs/api/rest-endpoints.md
  @specs/database/schema.md
  @specs/ui/pages.md
- If behavior changes, update the spec first.

2. AUTHENTICATION & JWT
- Every API request MUST include a JWT token.
- JWT must be sent in header:
  Authorization: Bearer <token>
- Backend must verify token using BETTER_AUTH_SECRET.
- Requests without valid token return 401 Unauthorized.

3. USER IDENTITY & ISOLATION
- Never trust user_id from request body.
- Extract authenticated user ONLY from JWT.
- If user_id exists in URL, it MUST match JWT user id.
- Mismatch results in 403 Forbidden.

4. QUERY-LEVEL AUTHORIZATION
- Authorization checks must happen before database access.
- All database queries MUST filter by authenticated user id.
- Example rule:
  Task.user_id == current_user.id

5. NO CROSS-USER DATA ACCESS
- Users can only see their own tasks.
- Users can only update, delete, or complete their own tasks.
- Do not leak existence of other users' tasks.

--------------------------------------------------

API REQUIREMENTS

The following endpoints must be implemented and secured:

- GET    /api/{user_id}/tasks
- POST   /api/{user_id}/tasks
- GET    /api/{user_id}/tasks/{id}
- PUT    /api/{user_id}/tasks/{id}
- DELETE /api/{user_id}/tasks/{id}
- PATCH  /api/{user_id}/tasks/{id}/complete

API RULES:
- All endpoints require JWT
- User id in URL must match JWT user
- Return correct HTTP status codes:
  401 Unauthorized
  403 Forbidden
  404 Not Found

--------------------------------------------------

DATABASE REQUIREMENTS

Use SQLModel with Neon PostgreSQL.

Tasks table fields:
- id (integer, primary key)
- user_id (string, foreign key)
- title (required, 1–200 chars)
- description (optional, max 1000 chars)
- completed (boolean, default false)
- created_at (timestamp)
- updated_at (timestamp)

Indexes:
- tasks.user_id
- tasks.completed

--------------------------------------------------

FRONTEND RULES

- Use Next.js App Router
- Use server components by default
- Client components only for interactivity
- All API calls go through a central API client
- JWT token must be attached to every request
- UI must be responsive and accessible

--------------------------------------------------

BACKEND RULES

- All routes under /api/
- Use FastAPI dependencies for auth
- Verify JWT on every request
- Use SQLModel for all DB operations
- Handle errors with HTTPException

--------------------------------------------------

DEVELOPMENT WORKFLOW

1. Read feature spec
2. Read API spec
3. Read database spec
4. Implement backend
5. Implement frontend
6. Test authentication and user isolation
7. Ensure all acceptance criteria are met

--------------------------------------------------

SECURITY BASELINE

- No logging of JWT secrets or tokens
- No trusting client-provided roles or IDs
- Reject expired or invalid tokens
- Enforce ownership at query level
- Prefer 404 when resource is not owned by user

--------------------------------------------------

DEFAULT BEHAVIOR

If in doubt:
- Choose secure behavior
- Deny access rather than guess
- Follow specs over assumptions
- Maintain consistency across frontend and backend

## Response snapshot

Created comprehensive constitution (v1.0.0) for Full-Stack Todo Web Application (Phase 2) with 6 core non-negotiable principles:

1. **Spec-First Development** - All implementation must start with reading specs
2. **Authentication & JWT Security** - Mandatory JWT on all protected endpoints
3. **User Identity & Isolation** - Never trust client-provided user_id, extract from JWT only
4. **Query-Level Authorization** - All queries must filter by authenticated user_id
5. **Zero Cross-User Data Access** - Strict data isolation between users
6. **API Contract Compliance** - RESTful conventions with correct HTTP status codes

Constitution includes:
- Technology stack specifications (Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL)
- Database schema requirements with mandatory indexes
- Development workflow (8-step implementation sequence)
- Security baseline with mandatory controls
- Governance rules with semantic versioning

File created at: `.specify/memory/constitution.md`

Sync Impact Report included in file header noting pending template reviews for:
- plan-template.md
- spec-template.md
- tasks-template.md

## Outcome

- ✅ Impact: Constitution v1.0.0 established as authoritative governance document for project
- 🧪 Tests: N/A (documentation artifact)
- 📁 Files: Created .specify/memory/constitution.md (226 lines)
- 🔁 Next prompts: Review and align dependent templates (plan, spec, tasks); Create feature specs following constitution principles
- 🧠 Reflection: Constitution provides clear security-first principles with emphasis on JWT authentication, user isolation, and query-level authorization. All principles are non-negotiable and testable.

## Evaluation notes (flywheel)

- Failure modes observed: None - constitution creation successful
- Graders run and results (PASS/FAIL): N/A (initial creation)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Validate constitution principles against existing codebase (if any) to identify gaps or conflicts
