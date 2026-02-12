---
name: devops-deployment
description: |
  Comprehensive guide for DevOps practices including local development setup,
  Docker containerization, CI/CD pipelines, deployment strategies, and
  production monitoring for Next.js and FastAPI applications.

proficiency_level: "B2"
category: "DevOps"
use_when: |
  - Setting up local development environment
  - Containerizing applications with Docker
  - Configuring CI/CD pipelines
  - Deploying to production (Vercel, Railway, Render, etc.)
  - Setting up monitoring and logging
  - Troubleshooting deployment issues
---

# DevOps and Deployment Guide

## Role
You are a DevOps specialist focused on containerization, deployment automation, and production operations for full-stack applications.

## Local Development Setup

### Prerequisites

**Required Tools:**
```bash
# Node.js (v18+)
node --version

# Python (v3.11+)
python --version

# Git
git --version

# Docker (optional but recommended)
docker --version
docker-compose --version
```

### Project Structure

```
todophs2/
├── frontend/              # Next.js application
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── .env.local
│   ├── package.json
│   └── next.config.js
├── backend/               # FastAPI application
│   ├── app/
│   ├── alembic/
│   ├── tests/
│   ├── .env
│   ├── requirements.txt
│   └── main.py
├── docker-compose.yml     # Local development
├── .github/
│   └── workflows/         # CI/CD pipelines
└── README.md
```

### Environment Variables

**Frontend (.env.local):**
```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
BETTER_AUTH_URL=http://localhost:3000

# Database (for Better Auth)
DATABASE_URL=postgresql://user:password@localhost:5432/auth_db
```

**Backend (.env):**
```bash
# Database
DATABASE_URL=postgresql://user:password@ep-xxx.neon.tech/neondb?sslmode=require

# Auth
BETTER_AUTH_SECRET=your-secret-key-min-32-chars

# API
API_V1_PREFIX=/api/v1
PROJECT_NAME=Todo API
DEBUG=True

# CORS
ALLOWED_ORIGINS=["http://localhost:3000"]
```

**Environment Variable Management:**
```bash
# Create .env files from templates
cp frontend/.env.example frontend/.env.local
cp backend/.env.example backend/.env

# Never commit .env files
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore
```

### Running Locally

**Backend (FastAPI):**
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend (Next.js):**
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

**Access Application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Docker Containerization

### Dockerfile - Backend

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run migrations and start server
CMD alembic upgrade head && \
    uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Dockerfile - Frontend

```dockerfile
# frontend/Dockerfile
FROM node:18-alpine AS base

# Install dependencies only when needed
FROM base AS deps
WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm ci

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build application
RUN npm run build

# Production image
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production

# Create non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy built application
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000

CMD ["node", "server.js"]
```

### Docker Compose - Development

```yaml
# docker-compose.yml
version: '3.8'

services:
  # PostgreSQL Database (optional - can use Neon instead)
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: todo_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Backend API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/todo_db
      BETTER_AUTH_SECRET: ${BETTER_AUTH_SECRET}
      DEBUG: "True"
      ALLOWED_ORIGINS: '["http://localhost:3000"]'
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

  # Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
      BETTER_AUTH_SECRET: ${BETTER_AUTH_SECRET}
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/todo_db
    depends_on:
      - backend
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm run dev

volumes:
  postgres_data:
```

**Development Dockerfile for Frontend:**
```dockerfile
# frontend/Dockerfile.dev
FROM node:18-alpine

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
```

### Docker Commands

```bash
# Build and start all services
docker-compose up --build

# Start services in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f backend

# Rebuild specific service
docker-compose build backend

# Execute command in running container
docker-compose exec backend alembic upgrade head

# Remove volumes (clean slate)
docker-compose down -v
```

## CI/CD Pipelines

### GitHub Actions - Testing

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  backend-tests:
    name: Backend Tests
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
          BETTER_AUTH_SECRET: test-secret-key-for-ci-testing
        run: |
          cd backend
          pytest --cov=app --cov-report=xml --cov-report=term

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml
          flags: backend

  frontend-tests:
    name: Frontend Tests
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Install dependencies
        run: |
          cd frontend
          npm ci

      - name: Run linter
        run: |
          cd frontend
          npm run lint

      - name: Run tests
        run: |
          cd frontend
          npm test -- --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./frontend/coverage/lcov.info
          flags: frontend

  e2e-tests:
    name: E2E Tests
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: |
          cd frontend
          npm ci

      - name: Install Playwright
        run: |
          cd frontend
          npx playwright install --with-deps

      - name: Run E2E tests
        run: |
          cd frontend
          npx playwright test

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: frontend/playwright-report/
```

### GitHub Actions - Deployment

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    name: Deploy Backend
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Deploy to Railway
        uses: bervProject/railway-deploy@main
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
          service: backend

  deploy-frontend:
    name: Deploy Frontend
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
```

## Deployment Strategies

### Frontend Deployment (Vercel)

**1. Install Vercel CLI:**
```bash
npm install -g vercel
```

**2. Configure Vercel:**
```json
// vercel.json
{
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "nextjs",
  "env": {
    "NEXT_PUBLIC_API_URL": "@api-url",
    "BETTER_AUTH_SECRET": "@auth-secret",
    "DATABASE_URL": "@database-url"
  }
}
```

**3. Deploy:**
```bash
cd frontend
vercel --prod
```

**4. Set Environment Variables:**
```bash
vercel env add NEXT_PUBLIC_API_URL production
vercel env add BETTER_AUTH_SECRET production
vercel env add DATABASE_URL production
```

### Backend Deployment (Railway)

**1. Install Railway CLI:**
```bash
npm install -g @railway/cli
```

**2. Login:**
```bash
railway login
```

**3. Initialize Project:**
```bash
cd backend
railway init
```

**4. Configure Railway:**
```toml
# railway.toml
[build]
builder = "DOCKERFILE"
dockerfilePath = "Dockerfile"

[deploy]
startCommand = "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 100
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

**5. Set Environment Variables:**
```bash
railway variables set DATABASE_URL="postgresql://..."
railway variables set BETTER_AUTH_SECRET="..."
railway variables set ALLOWED_ORIGINS='["https://your-frontend.vercel.app"]'
```

**6. Deploy:**
```bash
railway up
```

### Alternative: Render

**Backend (render.yaml):**
```yaml
services:
  - type: web
    name: todo-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        sync: false
      - key: BETTER_AUTH_SECRET
        sync: false
      - key: PYTHON_VERSION
        value: 3.11.0
```

**Frontend:**
```yaml
services:
  - type: web
    name: todo-frontend
    env: node
    buildCommand: npm install && npm run build
    startCommand: npm start
    envVars:
      - key: NEXT_PUBLIC_API_URL
        value: https://todo-api.onrender.com
      - key: BETTER_AUTH_SECRET
        sync: false
```

## Production Configuration

### Backend Production Settings

```python
# app/config.py
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Environment
    ENVIRONMENT: str = "production"

    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # Auth
    BETTER_AUTH_SECRET: str

    # API
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Todo API"
    DEBUG: bool = False

    # CORS
    ALLOWED_ORIGINS: List[str]

    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

### Frontend Production Settings

```javascript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,

  // Output standalone for Docker
  output: 'standalone',

  // Environment variables
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },

  // Security headers
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-DNS-Prefetch-Control',
            value: 'on'
          },
          {
            key: 'Strict-Transport-Security',
            value: 'max-age=63072000; includeSubDomains; preload'
          },
          {
            key: 'X-Frame-Options',
            value: 'SAMEORIGIN'
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff'
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block'
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin'
          }
        ]
      }
    ]
  }
}

module.exports = nextConfig
```

## Monitoring and Logging

### Backend Logging

```python
# app/core/logging.py
import logging
import sys
from app.config import settings

def setup_logging():
    """Configure application logging."""
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Reduce noise from libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

# app/main.py
from app.core.logging import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutting down")
```

### Health Check Endpoints

```python
# app/api/v1/health.py
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.database import get_session

router = APIRouter()

@router.get("/health")
async def health_check():
    """Basic health check."""
    return {"status": "healthy"}

@router.get("/health/db")
async def database_health_check(session: Session = Depends(get_session)):
    """Database health check."""
    try:
        # Simple query to check database connection
        session.exec(select(1)).first()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}
```

### Error Tracking (Sentry)

**Backend:**
```python
# app/main.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

if settings.ENVIRONMENT == "production":
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        integrations=[FastApiIntegration()],
        traces_sample_rate=0.1,
        environment=settings.ENVIRONMENT,
    )
```

**Frontend:**
```javascript
// app/layout.tsx
import * as Sentry from "@sentry/nextjs";

if (process.env.NODE_ENV === 'production') {
  Sentry.init({
    dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
    tracesSampleRate: 0.1,
    environment: process.env.NODE_ENV,
  });
}
```

## Security Best Practices

### Production Checklist

**Backend:**
- [ ] Use HTTPS only
- [ ] Set secure CORS origins
- [ ] Use environment variables for secrets
- [ ] Enable rate limiting
- [ ] Implement request validation
- [ ] Use secure headers
- [ ] Enable SQL injection protection (SQLModel does this)
- [ ] Implement proper error handling
- [ ] Use secure session management
- [ ] Enable logging and monitoring

**Frontend:**
- [ ] Use HTTPS only
- [ ] Implement CSP headers
- [ ] Sanitize user input
- [ ] Use httpOnly cookies for tokens
- [ ] Implement CSRF protection
- [ ] Enable XSS protection
- [ ] Use secure dependencies (npm audit)
- [ ] Implement proper error boundaries
- [ ] Enable logging and monitoring

### Environment Variables Security

```bash
# Never commit these files
.env
.env.local
.env.production

# Use secrets management
# GitHub: Repository Secrets
# Vercel: Environment Variables
# Railway: Variables
# Render: Environment Variables
```

## Troubleshooting

### Common Deployment Issues

**1. Database Connection Errors:**
```
Error: could not connect to server
```

**Solution:**
- Verify DATABASE_URL is correct
- Check if database is accessible from deployment platform
- Verify SSL mode is set correctly
- Check firewall rules

**2. CORS Errors:**
```
Error: CORS policy blocked
```

**Solution:**
```python
# Update ALLOWED_ORIGINS in backend
ALLOWED_ORIGINS=["https://your-frontend.vercel.app"]
```

**3. Build Failures:**
```
Error: Module not found
```

**Solution:**
- Verify all dependencies are in package.json/requirements.txt
- Check Node.js/Python version compatibility
- Clear build cache and rebuild

**4. Environment Variables Not Loading:**
```
Error: Environment variable not found
```

**Solution:**
- Verify variables are set in deployment platform
- Check variable names match exactly
- Restart application after setting variables

## Best Practices

### ✅ DO:
- Use environment variables for configuration
- Implement health check endpoints
- Set up monitoring and logging
- Use CI/CD for automated deployments
- Test in staging before production
- Implement proper error handling
- Use HTTPS in production
- Keep dependencies updated
- Implement database backups
- Use connection pooling

### ❌ DON'T:
- Commit secrets to version control
- Skip testing before deployment
- Use DEBUG=True in production
- Ignore security headers
- Deploy without health checks
- Skip database migrations
- Use weak secrets
- Ignore error logs
- Deploy without backups
- Skip monitoring setup

## Summary

Successful deployment requires:
1. **Local Development**: Proper environment setup
2. **Containerization**: Docker for consistency
3. **CI/CD**: Automated testing and deployment
4. **Production Config**: Secure, optimized settings
5. **Monitoring**: Logging and error tracking
6. **Security**: Best practices and hardening

Follow this guide to deploy a robust, production-ready application.
