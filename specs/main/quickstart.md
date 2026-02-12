# Developer Quickstart Guide

**Feature**: Full-Stack Todo Application
**Date**: 2026-02-07
**Estimated Setup Time**: 10-15 minutes

This guide will help you set up and run the full-stack todo application on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Git** - [Download](https://git-scm.com/)
- **Neon PostgreSQL Account** - [Sign up free](https://neon.tech)

**Verify installations**:
```bash
python --version    # Should show 3.11 or higher
node --version      # Should show 18.0 or higher
npm --version       # Should show 9.0 or higher
git --version       # Should show 2.0 or higher
```

---

## Step 1: Get the Code

Clone the repository:

```bash
git clone <repository-url>
cd todophs2
```

---

## Step 2: Set Up Database

### Create Neon Database

1. Go to [neon.tech](https://neon.tech) and sign up (free tier available)
2. Click "Create Project"
3. Choose a project name (e.g., "todo-app")
4. Select a region close to you
5. Click "Create Project"

### Get Connection String

1. In your Neon dashboard, click on your project
2. Click "Connection Details"
3. Copy the connection string (it looks like this):
   ```
   postgresql://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
   ```
4. Keep this handy - you'll need it in the next step

---

## Step 3: Configure Environment Variables

### Backend Configuration

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Copy the example environment file:
   ```bash
   copy .env.example .env
   ```

3. Edit `.env` and fill in the values:
   ```env
   # Database
   DATABASE_URL=postgresql://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require

   # Authentication (generate a random 32-character string)
   BETTER_AUTH_SECRET=your-secret-key-here-min-32-chars

   # CORS (frontend URL)
   ALLOWED_ORIGINS=http://localhost:3000

   # Debug mode
   DEBUG=true
   ```

   **Generate BETTER_AUTH_SECRET**:
   ```bash
   # On Windows (PowerShell)
   -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | % {[char]$_})

   # On Linux/Mac
   openssl rand -base64 32
   ```

### Frontend Configuration

1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```

2. Copy the example environment file:
   ```bash
   copy .env.local.example .env.local
   ```

3. Edit `.env.local` and fill in the values:
   ```env
   # Backend API URL
   NEXT_PUBLIC_API_URL=http://localhost:8000

   # Better Auth Secret (MUST match backend)
   BETTER_AUTH_SECRET=your-secret-key-here-min-32-chars

   # Better Auth URL
   BETTER_AUTH_URL=http://localhost:3000

   # Database URL (same as backend)
   DATABASE_URL=postgresql://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
   ```

   ⚠️ **Important**: `BETTER_AUTH_SECRET` must be identical in both `.env` files!

---

## Step 4: Automated Setup (Recommended)

From the project root directory, run:

```bash
quick-start.bat
```

This script will:
- ✅ Create Python virtual environment
- ✅ Install backend dependencies
- ✅ Run database migrations
- ✅ Install frontend dependencies
- ✅ Verify configuration

**If the script succeeds**, skip to Step 6 (Start Servers).

**If the script fails**, continue with manual setup below.

---

## Step 5: Manual Setup (If Automated Setup Failed)

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create and activate virtual environment:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run database migrations:
   ```bash
   alembic upgrade head
   ```

5. Verify setup:
   ```bash
   pytest tests/ -v
   ```
   You should see 55 tests passing.

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd ../frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Verify setup:
   ```bash
   npm run build
   ```
   Build should complete without errors.

---

## Step 6: Start the Servers

You'll need **two terminal windows** (or tabs).

### Terminal 1: Start Backend

```bash
cd backend
venv\Scripts\activate    # Windows
# source venv/bin/activate  # Linux/Mac
uvicorn app.main:app --reload --port 8000
```

**Expected output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Or use the convenience script**:
```bash
start-backend.bat
```

### Terminal 2: Start Frontend

```bash
cd frontend
npm run dev
```

**Expected output**:
```
  ▲ Next.js 14.x.x
  - Local:        http://localhost:3000
  - Ready in 2.5s
```

**Or use the convenience script**:
```bash
start-frontend.bat
```

---

## Step 7: Verify Installation

### Check Backend

1. Open browser to: http://localhost:8000
2. You should see: `{"message": "Todo API", "version": "1.0.0"}`

3. Check API docs: http://localhost:8000/docs
4. You should see the interactive API documentation

### Check Frontend

1. Open browser to: http://localhost:3000
2. You should see the todo application home page
3. Click "Sign Up" to create an account

---

## Step 8: Create Your First Todo

1. **Sign Up**:
   - Click "Sign Up" button
   - Enter email and password
   - Click "Create Account"
   - You should be redirected to the tasks page

2. **Create a Todo**:
   - Click "New Task" button
   - Enter a title (e.g., "My first todo")
   - Optionally add a description
   - Click "Create"
   - You should see your todo in the list

3. **Test Features**:
   - ✅ Toggle completion checkbox
   - ✅ Click on todo to view details
   - ✅ Edit the todo
   - ✅ Delete the todo
   - ✅ Logout and login again

---

## Common Issues & Solutions

### Issue: "Database connection failed"

**Symptoms**: Backend fails to start with database error

**Solutions**:
1. Verify `DATABASE_URL` is correct in both `.env` files
2. Check that your Neon database is active (not paused)
3. Ensure connection string includes `?sslmode=require`
4. Test connection:
   ```bash
   cd backend
   python -c "from app.database import engine; engine.connect()"
   ```

### Issue: "Module not found" errors

**Symptoms**: Import errors when starting backend

**Solutions**:
1. Ensure virtual environment is activated:
   ```bash
   # You should see (venv) in your prompt
   venv\Scripts\activate
   ```
2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Issue: "Authentication not working"

**Symptoms**: Login fails or JWT errors

**Solutions**:
1. Verify `BETTER_AUTH_SECRET` is identical in both `.env` files
2. Ensure secret is at least 32 characters
3. Restart both servers after changing environment variables
4. Clear browser localStorage:
   ```javascript
   // In browser console
   localStorage.clear()
   ```

### Issue: "Port already in use"

**Symptoms**: "Address already in use" error

**Solutions**:
1. Check if another process is using the port:
   ```bash
   # Windows
   netstat -ano | findstr :8000
   netstat -ano | findstr :3000

   # Linux/Mac
   lsof -i :8000
   lsof -i :3000
   ```
2. Kill the process or use different ports:
   ```bash
   # Backend on different port
   uvicorn app.main:app --reload --port 8001

   # Frontend on different port
   npm run dev -- -p 3001
   ```

### Issue: "CORS errors in browser"

**Symptoms**: Network errors in browser console

**Solutions**:
1. Verify `ALLOWED_ORIGINS` in backend `.env` matches frontend URL
2. Ensure both servers are running
3. Check that frontend is using correct API URL in `.env.local`

---

## Development Workflow

### Making Backend Changes

1. Edit code in `backend/app/`
2. Server auto-reloads (watch terminal for errors)
3. Run tests:
   ```bash
   cd backend
   pytest tests/ -v
   ```

### Making Frontend Changes

1. Edit code in `frontend/app/` or `frontend/components/`
2. Next.js auto-reloads (watch browser for changes)
3. Check browser console for errors

### Database Changes

1. Create migration:
   ```bash
   cd backend
   alembic revision -m "description of change"
   ```

2. Edit migration file in `backend/alembic/versions/`

3. Apply migration:
   ```bash
   alembic upgrade head
   ```

4. Rollback if needed:
   ```bash
   alembic downgrade -1
   ```

---

## Running Tests

### Backend Tests (55 tests)

```bash
cd backend
venv\Scripts\activate
pytest tests/ -v
```

**Or use the convenience script**:
```bash
run-tests.bat
```

**Test categories**:
- Security tests (13): Password hashing, JWT verification
- Signup tests (12): User registration
- Login tests (12): Authentication
- Todo CRUD tests (18): Create, read, update, delete

### Frontend Tests

Currently no automated frontend tests. Manual testing recommended:
- Test all user flows (signup, login, CRUD operations)
- Test error handling (network errors, invalid input)
- Test on different browsers (Chrome, Firefox, Safari)

---

## Project Structure Overview

```
todophs2/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/v1/       # API endpoints
│   │   ├── core/         # Auth & security
│   │   ├── models/       # Database models
│   │   └── schemas/      # Pydantic schemas
│   ├── tests/            # 55 passing tests
│   └── alembic/          # Database migrations
│
├── frontend/             # Next.js frontend
│   ├── app/              # Pages and routes
│   ├── components/       # React components
│   └── lib/              # API client & utilities
│
└── specs/                # Documentation
    └── main/             # This guide and more
```

---

## API Endpoints Reference

### Authentication (Public)
- `POST /api/v1/auth/signup` - Create account
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/logout` - Logout

### Todos (Requires Authentication)
- `GET /api/v1/todos` - List all user's todos
- `POST /api/v1/todos` - Create new todo
- `GET /api/v1/todos/{id}` - Get single todo
- `PUT /api/v1/todos/{id}` - Update todo
- `DELETE /api/v1/todos/{id}` - Delete todo
- `PATCH /api/v1/todos/{id}/toggle` - Toggle completion

### Health
- `GET /api/v1/health` - Health check

**Full API documentation**: http://localhost:8000/docs (when backend is running)

---

## Next Steps

Now that you have the application running:

1. **Explore the code**:
   - Backend: `backend/app/api/v1/todos.py` - Todo endpoints
   - Frontend: `frontend/app/(protected)/tasks/page.tsx` - Task list page

2. **Read the documentation**:
   - [Implementation Plan](plan.md) - Architecture decisions
   - [Data Model](data-model.md) - Database schema
   - [Research](research.md) - Technology choices

3. **Try the features**:
   - Create multiple todos
   - Test with multiple user accounts
   - Verify user isolation (users can't see each other's todos)

4. **Make changes**:
   - Add a new field to todos (e.g., priority)
   - Add filtering to the todo list
   - Customize the UI styling

---

## Getting Help

**Documentation**:
- Root README: `../../README.md`
- Backend README: `../../backend/README.md`
- Frontend README: `../../frontend/README.md`
- Setup Guide: `../../SETUP.md`

**Common Commands**:
```bash
# Start backend
start-backend.bat

# Start frontend
start-frontend.bat

# Run tests
run-tests.bat

# Full setup
quick-start.bat
```

**Troubleshooting**:
- Check both terminal windows for error messages
- Verify environment variables are set correctly
- Ensure both servers are running
- Clear browser cache and localStorage if needed

---

## Success Checklist

Before considering setup complete, verify:

- ✅ Backend starts without errors on port 8000
- ✅ Frontend starts without errors on port 3000
- ✅ Can access http://localhost:8000/docs
- ✅ Can access http://localhost:3000
- ✅ Can create a user account
- ✅ Can login with created account
- ✅ Can create, view, edit, and delete todos
- ✅ Backend tests pass (55/55)
- ✅ No CORS errors in browser console

**If all items are checked**, you're ready to develop! 🎉

---

**Last Updated**: 2026-02-07
**Estimated Setup Time**: 10-15 minutes
**Support**: See documentation links above
