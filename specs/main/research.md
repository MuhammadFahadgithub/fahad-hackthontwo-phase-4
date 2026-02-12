# Technology Research & Decisions

**Feature**: Full-Stack Todo Application
**Date**: 2026-02-07
**Status**: Complete (Retrospective)

This document captures the technology research and decision-making process for the full-stack todo application.

## Research Questions

### Q1: Which backend framework should we use for the REST API?

**Options Evaluated**:
1. FastAPI (Python)
2. Django REST Framework (Python)
3. Flask (Python)
4. Express.js (Node.js)

**Research Findings**:

**FastAPI**:
- ✅ Native async/await support (high performance)
- ✅ Automatic OpenAPI documentation generation
- ✅ Built-in request validation with Pydantic
- ✅ Excellent type hints and IDE support
- ✅ Fast development with minimal boilerplate
- ✅ Strong ecosystem for JWT authentication
- ⚠️ Relatively newer (2018) but rapidly adopted

**Django REST Framework**:
- ✅ Mature and battle-tested
- ✅ Batteries-included (admin, ORM, auth)
- ✅ Large ecosystem and community
- ❌ Heavier framework (more overhead)
- ❌ Slower for simple APIs
- ❌ More opinionated structure

**Flask**:
- ✅ Lightweight and flexible
- ✅ Large ecosystem
- ❌ Requires more manual setup for validation
- ❌ No automatic API documentation
- ❌ More boilerplate for REST APIs

**Express.js**:
- ✅ Very popular and mature
- ✅ Large ecosystem
- ❌ Would require JavaScript/TypeScript (team has Python expertise)
- ❌ Less type safety than Python options
- ❌ More manual validation setup

**Decision**: FastAPI

**Rationale**: FastAPI provides the best balance of performance, developer experience, and built-in features for building REST APIs. The automatic OpenAPI documentation and Pydantic validation significantly reduce boilerplate while maintaining type safety.

---

### Q2: Which ORM should we use for database access?

**Options Evaluated**:
1. SQLModel
2. SQLAlchemy (pure)
3. Tortoise ORM
4. Raw SQL

**Research Findings**:

**SQLModel**:
- ✅ Combines SQLAlchemy (mature ORM) with Pydantic (validation)
- ✅ Single model definition for both database and API schemas
- ✅ Type-safe queries with excellent IDE support
- ✅ Async support for FastAPI integration
- ✅ Reduces code duplication
- ⚠️ Newer library (2021) but created by FastAPI author

**SQLAlchemy**:
- ✅ Most mature Python ORM
- ✅ Comprehensive feature set
- ✅ Large community
- ❌ Requires separate Pydantic schemas for API
- ❌ More verbose

**Tortoise ORM**:
- ✅ Async-first design
- ❌ Smaller ecosystem
- ❌ Less mature
- ❌ Fewer resources and examples

**Raw SQL**:
- ✅ Maximum control and performance
- ❌ Loses type safety
- ❌ More code to write and maintain
- ❌ More prone to SQL injection if not careful

**Decision**: SQLModel

**Rationale**: SQLModel eliminates the duplication between database models and API schemas while maintaining the maturity of SQLAlchemy. The type safety and reduced boilerplate make it ideal for rapid development.

---

### Q3: Which database should we use?

**Options Evaluated**:
1. Neon PostgreSQL (serverless)
2. Traditional PostgreSQL
3. SQLite
4. MySQL

**Research Findings**:

**Neon PostgreSQL**:
- ✅ Serverless architecture with automatic scaling
- ✅ Free tier suitable for development and small projects
- ✅ Full PostgreSQL compatibility
- ✅ Built-in connection pooling
- ✅ Instant provisioning (no server setup)
- ✅ Excellent for hackathon/prototype projects
- ⚠️ Newer service (2022)

**Traditional PostgreSQL**:
- ✅ Most mature and feature-rich
- ✅ Excellent for production
- ❌ Requires server management
- ❌ More complex setup

**SQLite**:
- ✅ Zero configuration
- ✅ Perfect for development
- ❌ Not suitable for multi-user production
- ❌ Limited concurrency

**MySQL**:
- ✅ Mature and widely used
- ❌ Less feature-rich than PostgreSQL
- ❌ Weaker support for JSON and advanced types

**Decision**: Neon PostgreSQL

**Rationale**: Neon provides the full power of PostgreSQL without the operational overhead. The serverless model is perfect for hackathon projects and can scale to production if needed.

---

### Q4: How should we handle authentication?

**Options Evaluated**:
1. Better Auth + JWT
2. Session-based authentication
3. OAuth2 with refresh tokens
4. Third-party services (Auth0, Clerk)

**Research Findings**:

**Better Auth + JWT**:
- ✅ Complete authentication flows out of the box
- ✅ JWT enables stateless authentication
- ✅ No session storage needed
- ✅ RESTful and scalable
- ✅ Simple to implement
- ⚠️ Tokens can't be revoked easily (use short expiration)

**Session-based auth**:
- ✅ Easy to revoke sessions
- ❌ Requires session storage (Redis, database)
- ❌ Not RESTful
- ❌ Harder to scale horizontally

**OAuth2 with refresh tokens**:
- ✅ Industry standard
- ✅ Supports token revocation
- ❌ More complex to implement
- ❌ Over-engineered for simple use case

**Third-party services**:
- ✅ Fully managed
- ✅ Advanced features (MFA, social login)
- ❌ External dependency
- ❌ Additional cost
- ❌ Less control

**Decision**: Better Auth + JWT

**Rationale**: Better Auth provides a complete authentication solution with minimal setup. JWT tokens enable stateless, RESTful authentication that scales well. The 7-day expiration balances security and user experience.

---

### Q5: Which frontend framework should we use?

**Options Evaluated**:
1. Next.js 16+ (App Router)
2. Create React App
3. Vite + React Router
4. Remix

**Research Findings**:

**Next.js (App Router)**:
- ✅ Server Components by default (better performance)
- ✅ Built-in routing with file-system structure
- ✅ Excellent developer experience
- ✅ Strong TypeScript support
- ✅ Large ecosystem and community
- ✅ App Router is the modern, recommended approach
- ⚠️ App Router is newer (2023) but stable

**Create React App**:
- ❌ Deprecated by React team
- ❌ No SSR support
- ❌ Not recommended for new projects

**Vite + React Router**:
- ✅ Fast development server
- ✅ Flexible
- ❌ More manual setup required
- ❌ No SSR out of the box

**Remix**:
- ✅ Modern approach to React
- ✅ Good performance
- ❌ Smaller ecosystem
- ❌ Steeper learning curve

**Decision**: Next.js 16+ (App Router)

**Rationale**: Next.js provides the best developer experience with built-in routing, Server Components, and excellent TypeScript support. The App Router is the future of Next.js and provides better performance through Server Components.

---

### Q6: How should we hash passwords?

**Options Evaluated**:
1. bcrypt
2. Argon2
3. PBKDF2
4. scrypt

**Research Findings**:

**bcrypt**:
- ✅ Industry standard for password hashing
- ✅ Adaptive cost factor (future-proof)
- ✅ Built-in salt generation
- ✅ Resistant to rainbow table attacks
- ✅ Well-supported in Python ecosystem
- ✅ Cost factor 12 balances security and performance (~250ms)

**Argon2**:
- ✅ Winner of Password Hashing Competition (2015)
- ✅ More modern algorithm
- ❌ Less widely supported in Python ecosystem
- ❌ Fewer resources and examples

**PBKDF2**:
- ✅ NIST recommended
- ✅ Well-supported
- ❌ Older algorithm
- ❌ Less resistant to GPU attacks than bcrypt

**scrypt**:
- ✅ Memory-hard (resistant to hardware attacks)
- ❌ Less battle-tested than bcrypt
- ❌ Smaller ecosystem

**Decision**: bcrypt with cost factor 12

**Rationale**: bcrypt is the industry standard with excellent support in the Python ecosystem. Cost factor 12 provides strong security while maintaining acceptable performance (~250ms per hash).

---

## Best Practices Research

### FastAPI Best Practices

**Researched Topics**:
- Dependency injection for database sessions
- JWT authentication with FastAPI Security
- Error handling and exception handlers
- CORS configuration
- API versioning strategies
- Async/await patterns

**Key Findings**:
- Use `Depends()` for dependency injection (database sessions, auth)
- Use `HTTPBearer` for JWT token extraction
- Implement global exception handlers for consistent error responses
- Configure CORS middleware with specific origins (not wildcard)
- Use `/api/v1` prefix for API versioning
- Use async/await throughout for non-blocking I/O

### SQLModel Best Practices

**Researched Topics**:
- Model definition patterns
- Relationship handling
- Query optimization
- Migration strategies with Alembic

**Key Findings**:
- Define models with `table=True` for database tables
- Use `Field()` for column constraints and defaults
- Index foreign keys for query performance
- Use Alembic for database migrations (not `create_all()` in production)
- Separate read and write schemas when needed

### Next.js App Router Best Practices

**Researched Topics**:
- Server vs Client Components
- Route organization
- Data fetching patterns
- Authentication with middleware

**Key Findings**:
- Use Server Components by default (better performance)
- Use Client Components only for interactivity (`'use client'`)
- Organize routes with route groups `(auth)`, `(protected)`
- Use middleware for route protection
- Fetch data in Server Components when possible

### JWT Security Best Practices

**Researched Topics**:
- Token expiration strategies
- Token storage (localStorage vs cookies)
- Token transmission (header vs cookie)
- Token revocation strategies

**Key Findings**:
- Use reasonable expiration (7 days balances security and UX)
- Store tokens in localStorage for SPA (or httpOnly cookies for SSR)
- Transmit tokens in Authorization: Bearer header (RESTful)
- For revocation, use short expiration or maintain token blacklist
- Never log or expose token contents

---

## Integration Patterns

### Frontend-Backend Integration

**Pattern**: REST API with JWT authentication

**Flow**:
1. Frontend authenticates with Better Auth
2. Better Auth issues JWT token
3. Frontend stores token in localStorage
4. Frontend attaches token to all API requests
5. Backend verifies token and extracts user identity
6. Backend filters all queries by authenticated user

**Benefits**:
- Stateless authentication (no session storage)
- RESTful design (scalable)
- Clear separation of concerns
- Easy to test and debug

### Database Access Pattern

**Pattern**: Query-level user isolation

**Implementation**:
- Extract user_id from JWT token
- Filter all queries by user_id
- Verify ownership before updates/deletes
- Return 403 for ownership violations

**Benefits**:
- Simple and explicit
- Easy to test and verify
- No database-specific features required
- Clear in code review

---

## Performance Considerations

### Backend Performance

**Optimizations**:
- Async/await throughout (non-blocking I/O)
- Database connection pooling
- Indexed foreign keys (user_id)
- JWT verification cached per request

**Expected Performance**:
- API latency: <200ms p95
- Database queries: <50ms average
- Password hashing: ~250ms (bcrypt cost 12)

### Frontend Performance

**Optimizations**:
- Server Components (less JavaScript to client)
- Code splitting (automatic with Next.js)
- Optimistic UI updates (toggle operations)
- Loading states for async operations

**Expected Performance**:
- Page load: <2 seconds
- Task creation: <3 seconds
- Task list rendering: 100+ tasks without degradation

---

## Security Considerations

### Authentication Security

**Measures**:
- Passwords hashed with bcrypt (cost factor 12)
- JWT tokens with 7-day expiration
- Tokens transmitted in Authorization header
- HTTPS required in production

### Authorization Security

**Measures**:
- User identity from JWT only (never from request body)
- All queries filtered by authenticated user_id
- Ownership verification before updates/deletes
- 403 Forbidden for ownership violations

### Data Protection

**Measures**:
- No sensitive data in logs
- CORS restricted to frontend origin
- Input validation on all endpoints
- SQL injection prevention (ORM parameterized queries)

---

## Deployment Considerations

### Environment Variables

**Required**:
- `DATABASE_URL`: Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Shared secret for JWT signing/verification
- `ALLOWED_ORIGINS`: CORS allowed origins
- `DEBUG`: Enable/disable debug mode

### Production Requirements

**Must Have**:
- HTTPS enforcement
- CORS configured for production origin
- API docs disabled
- Database connection with SSL
- Error logging configured

**Recommended**:
- Rate limiting on auth endpoints
- Monitoring and alerting
- Automated backups
- Health check endpoints

---

## Conclusion

All technology choices have been validated through research and align with industry best practices. The selected stack (FastAPI + SQLModel + Neon + Next.js + Better Auth) provides:

- ✅ Rapid development velocity
- ✅ Strong type safety
- ✅ Excellent developer experience
- ✅ Production-ready security
- ✅ Scalable architecture
- ✅ Comprehensive testing support

**Status**: All research questions resolved. Ready for implementation.
