# Multi-AI-Agent System - Setup & Manual Execution Guide

This document provides a step-by-step manual for installing, configuring, running, and testing the **Multi-AI-Agent Software Developer System** backend.

---

## 📋 Prerequisites

Before starting, ensure you have the following installed on your system:
- **Python**: Version 3.11 or higher (`python3 --version`)
- **Git**: (`git --version`)
- **Docker & Docker Compose** *(Optional, for containerized deployment)*: (`docker --version`)

---

## 🚀 Step-by-Step Installation & Setup

### 1. Navigate to Project Directory
```bash
cd "/Users/satyam_007/Desktop/Multi -AI Agents/backend"
```

### 2. Configure Environment Variables
Copy the template configuration file:
```bash
cp .env.example .env
```
> [!NOTE]
> The default `.env` configuration includes fallback mock providers for LLM, Redis, and PostgreSQL, allowing the application to boot cleanly without external credentials.

### 3. Create & Activate Virtual Environment
```bash
# Create virtual environment named 'venv'
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🏃 Running the Server

You can run the backend server using any of the following methods:

### Method A: Standard Python Command (Recommended)
```bash
python -m app.main
```

### Method B: Uvicorn with Live Reload (For Active Development)
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Method C: Docker Compose (Runs Backend + PostgreSQL + Redis)
```bash
docker-compose up --build
```

---

## 🔍 Verification & Health Checks

1. **Root Status Endpoint**:
   ```bash
   curl http://localhost:8000/
   ```
   *Expected Response:*
   ```json
   {
     "message": "Welcome to Multi-Agent System API",
     "status": "online",
     "health_check": "/health",
     "api_docs": "/docs",
     "version": "1.0.0"
   }
   ```

2. **Health Check Endpoint**:
   ```bash
   curl http://localhost:8000/health
   ```

3. **Interactive API Documentation (Swagger UI)**:
   Open your browser to:
   [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Running Automated Unit Tests

Execute the full test suite using pytest:
```bash
pytest -v
```

---

## 🛠 Troubleshooting

### Port 8000 Already in Use (`Errno 48`)
If port 8000 is occupied by a background process, kill it using:
```bash
lsof -ti:8000 | xargs kill -9
```
Or run the server on a custom port:
```bash
uvicorn app.main:app --port 8001 --reload
```
