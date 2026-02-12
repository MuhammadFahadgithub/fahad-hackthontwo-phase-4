---
id: 002
title: Update Templates for Constitution Alignment
stage: constitution
date: 2026-02-06
surface: agent
model: claude-sonnet-4-5
feature: none
branch: master
user: Zaib's
command: update templates
labels: ["constitution", "templates", "security", "alignment"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/templates/plan-template.md
  - .specify/templates/spec-template.md
  - .specify/templates/tasks-template.md
  - .specify/templates/checklist-template.md
tests:
  - N/A (documentation only)
---

## Prompt

update the templates

## Response snapshot

Updated all dependent templates to align with Constitution v1.0.0:

**1. plan-template.md**
- Replaced generic technical context with Full-Stack Todo specific stack (Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL)
- Expanded Constitution Check section with all 6 principles as checkboxes:
  - I. Spec-First Development
  - II. Authentication & JWT Security
  - III. User Identity & Isolation
  - IV. Query-Level Authorization
  - V. Zero Cross-User Data Access
  - VI. API Contract Compliance
- Updated Source Code structure to show complete web application layout (backend/ and frontend/ with detailed subdirectories)
- Removed generic options, provided concrete structure matching constitution requirements

**2. spec-template.md**
- Added comprehensive "Security Requirements" section (mandatory for all features)
- Mapped security requirements to Constitution Principles II-V
- Defined 17 security requirements (SR-001 through SR-017):
  - Authentication requirements (SR-001 to SR-005)
  - User identity & isolation (SR-006 to SR-008)
  - Authorization requirements (SR-009 to SR-011)
  - Data isolation requirements (SR-012 to SR-015)
  - API contract requirements (SR-016 to SR-017)
- Included all required HTTP status codes with descriptions

**3. tasks-template.md**
- Updated Path Conventions to reflect web application structure (backend/app/, frontend/app/)
- Expanded Phase 2 (Foundational) with specific tasks:
  - Database & Models setup (T004-T008)
  - Authentication & Security tasks referencing Constitution Principles II-V (T009-T015)
  - API Infrastructure (T016-T020)
  - Frontend Infrastructure (T021-T023)
  - Security Testing - 5 mandatory tests for foundation (T024-T028)
- Enhanced Phase 3 (User Story 1) with:
  - Security Tests section (5 mandatory tests: T033-T037)
  - Backend Implementation with JWT auth and ownership checks (T038-T046)
  - Frontend Implementation with JWT token attachment (T047-T053)
- Enhanced Phase N (Polish) with:
  - Security Validation section (8 mandatory checks)
  - API Contract Validation (4 checks)
  - Deployment Readiness (5 checks)

**4. checklist-template.md**
- Added Constitution reference to header
- Created comprehensive "Constitution Compliance" section (mandatory for all features)
- Organized 27 constitution compliance checks (CHK001-CHK027) across all 6 principles:
  - Spec-First Development (4 checks)
  - Authentication & JWT Security (6 checks)
  - User Identity & Isolation (4 checks)
  - Query-Level Authorization (4 checks)
  - Zero Cross-User Data Access (5 checks)
  - API Contract Compliance (4 checks + detailed HTTP status code sub-checks)

All templates now enforce constitution principles through concrete, actionable checkpoints.

## Outcome

- ✅ Impact: All 4 dependent templates aligned with Constitution v1.0.0, ensuring spec-driven development with security-first principles
- 🧪 Tests: N/A (documentation artifacts)
- 📁 Files: Updated 4 template files with constitution-aligned content
- 🔁 Next prompts: Create first feature spec following updated templates; Implement foundational authentication infrastructure
- 🧠 Reflection: Templates now provide concrete, actionable guidance for implementing constitution principles. Security requirements are no longer optional or implicit - they're mandatory checkpoints at every phase.

## Evaluation notes (flywheel)

- Failure modes observed: None - template updates successful
- Graders run and results (PASS/FAIL): N/A (template updates)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test template effectiveness by creating a real feature spec and validating that all constitution principles are naturally enforced through the template structure
