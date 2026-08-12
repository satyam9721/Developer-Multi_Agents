# Multi-AI-Agent System - Base Backend

Autonomous multi-agent backend architecture built with FastAPI, Pydantic, SQLAlchemy, Celery, and structured agent workflows.

## Features
- **Manager-Orchestrated System**: Specialized agents (`Planner`, `Researcher`, `Coder`, `Reviewer`, `Tester`, `Browser`) orchestrated safely by `ManagerAgent`.
- **Policy Engine**: Command, Git, Permission, and Production deployment policies to guard high-risk operations.
- **Isolated Workspace Sandbox**: All tasks run within isolated repository workspaces.
- **Graceful Fallbacks**: Boots locally without requiring external services (PostgreSQL, Redis, GitHub API, LLM API keys) to be configured.

## Quickstart

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Environment Setup
```bash
cp .env.example .env
```

### 3. Run Locally
```bash
python -m app.main
```
Or:
```bash
uvicorn app.main:app --reload --port 8000
```

### 4. Health Check
```bash
curl http://localhost:8000/health
```

### 5. Running Tests
```bash
pytest
```
