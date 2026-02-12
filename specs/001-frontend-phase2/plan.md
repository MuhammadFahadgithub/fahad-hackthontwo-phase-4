# Implementation Plan: Frontend Phase 2 Web Application (FAST)

**Branch**: `001-frontend-phase2` | **Date**: 2026-02-07 | **Spec**: [spec.md](./spec.md)

## Goal

Convert console todo app into secure multi-user web application with persistent database and authentication.

## Stack

- **Frontend**: Next.js 16+ (App Router, TypeScript, Tailwind CSS)
- **Backend**: FastAPI (Python)
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Auth**: Better Auth (JWT)
- **Workflow**: Spec-Driven Development

## Core Features

- User signup/signin
- Task CRUD (create, list, detail, update, delete)
- Toggle task completion
- User-isolated task access

## Security Model

- Better Auth issues JWT on frontend
- Frontend sends JWT in `Authorization: Bearer <token>` header
- Backend verifies JWT using shared secret (`BETTER_AUTH_SECRET`)
- Token `user_id` must match URL `user_id`
- Missing/invalid token → 401 Unauthorized
- User mismatch → 403 Forbidden
- All DB queries filtered by `user_id`

## API Endpoints

```
POST   /api/auth/signup
POST   /api/auth/signin
GET    /api/users/{user_id}/tasks
POST   /api/users/{user_id}/tasks
GET    /api/users/{user_id}/tasks/{task_id}
PUT    /api/users/{user_id}/tasks/{task_id}
DELETE /api/users/{user_id}/tasks/{task_id}
PATCH  /api/users/{user_id}/tasks/{task_id}/toggle
```

## Data Model

**Task Table**:
- `id` (UUID, primary key)
- `title` (string, required, max 200 chars)
- `description` (string, optional)
- `completed` (boolean, default false)
- `user_id` (string, indexed, foreign key)
- `created_at` (timestamp)
- `updated_at` (timestamp)

**User Table** (managed by Better Auth):
- `id` (string, primary key)
- `email` (string, unique)
- `password_hash` (string)
- `name` (string, optional)

## Repository Structure

```
todophs2/
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── (auth)/
│   │   │   │   ├── signin/page.tsx
│   │   │   │   └── signup/page.tsx
│   │   │   ├── (protected)/
│   │   │   │   └── tasks/
│   │   │   │       ├── page.tsx
│   │   │   │       ├── new/page.tsx
│   │   │   │       └── [id]/
│   │   │   │           ├── page.tsx
│   │   │   │           └── edit/page.tsx
│   │   │   └── layout.tsx
│   │   ├── components/
│   │   │   ├── auth/
│   │   │   ├── tasks/
│   │   │   ├── layout/
│   │   │   └── ui/
│   │   └── lib/
│   │       ├── api/
│   │       ├── auth/
│   │       └── types/
│   ├── .env.local
│   └── package.json
├── backend/
│   ├── src/
│   │   ├── models/
│   │   ├── api/
│   │   ├── services/
│   │   └── middleware/
│   ├── .env
│   └── requirements.txt
├── specs/
├── docker-compose.yml
└── README.md
```

## Phase Delivery

### Phase 1: Repository Setup
- Initialize monorepo structure
- Create frontend/ and backend/ folders
- Setup .gitignore
- Create README with setup instructions
- **Git tag**: `phase-1-setup`

### Phase 2: Backend Database & Models
- Setup Neon PostgreSQL connection
- Create SQLModel models (Task, User)
- Setup database migrations (Alembic or SQLModel.create_all)
- Test database connectivity
- **Git tag**: `phase-2-backend-db`

### Phase 3: Backend API & JWT Security
- Implement FastAPI routes for tasks
- Add JWT verification middleware
- Implement user_id validation
- Add CORS configuration
- Test all endpoints with Postman/curl
- **Git tag**: `phase-3-backend-api`

### Phase 4: Frontend Authentication
- Setup Better Auth configuration
- Create signup/signin pages
- Implement JWT token storage
- Create AuthGuard component
- Test auth flow end-to-end
- **Git tag**: `phase-4-frontend-auth`

### Phase 5: Frontend Task UI
- Create task list page
- Create task detail page
- Create task create/edit forms
- Implement API client with JWT injection
- Add loading/error states
- **Git tag**: `phase-5-frontend-ui`

### Phase 6: Testing & Documentation
- Write backend unit tests
- Write frontend component tests
- E2E smoke tests
- Update README with full setup
- Final security audit
- **Git tag**: `phase-6-complete`

## Environment Variables

**Frontend (.env.local)**:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
BETTER_AUTH_URL=http://localhost:3000
```

**Backend (.env)**:
```
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
CORS_ORIGINS=http://localhost:3000
JWT_ALGORITHM=HS256
```

## Quick Start Commands

**Frontend**:
```bash
cd frontend
npm install
npm run dev  # http://localhost:3000
```

**Backend**:
```bash
cd backend
pip install -r requirements.txt
uvicorn src.main:app --reload  # http://localhost:8000
```

**Database**:
```bash
# Get Neon connection string from dashboard
# Update .env files
# Run migrations
```

## Definition of Done

- ✅ User can signup and signin
- ✅ Authenticated user can create tasks
- ✅ User sees only their own tasks
- ✅ User can update/delete their tasks
- ✅ User can toggle task completion
- ✅ JWT required for all protected endpoints
- ✅ Data persists in Neon database
- ✅ All phases tagged in git
- ✅ README has complete setup instructions
- ✅ Project runs locally without errors

## Critical Path

1. Setup Neon database → Get connection string
2. Backend models → Task + User tables
3. Backend API → CRUD endpoints with JWT
4. Better Auth → JWT token generation
5. Frontend auth → Signup/signin pages
6. Frontend UI → Task management pages
7. Integration → Connect frontend to backend
8. Testing → Verify user isolation
9. Documentation → README + deployment guide
10. Submission → Git tags + final push

## Risks & Quick Mitigations

- **JWT mismatch**: Use same secret, same algorithm (HS256)
- **CORS errors**: Add frontend origin to backend CORS config
- **Neon connection**: Use connection pooling, handle SSL
- **Better Auth setup**: Follow official Next.js 16+ docs
- **User isolation**: Always filter queries by `user_id` from JWT

## Success Metrics

- All 7 user stories from spec completed
- 100% user data isolation verified
- <2s page load time
- >80% test coverage
- Zero security vulnerabilities
- Complete documentation

## Next Steps

1. Run `/sp.tasks` to generate task breakdown
2. Execute Phase 1: Repository setup
3. Execute Phase 2: Backend database
4. Execute Phase 3: Backend API + JWT
5. Execute Phase 4: Frontend auth
6. Execute Phase 5: Frontend UI
7. Execute Phase 6: Testing + docs
8. Tag each phase in git
9. Final submission

## Related Files

- [Feature Specification](./spec.md)
- [Requirements Checklist](./checklists/requirements.md)
- Research: Skip for fast execution
- Data Model: See "Data Model" section above
- Contracts: See "API Endpoints" section above
- Quickstart: See "Quick Start Commands" section above
