# hackaton-platanus-25

## Setup

Start PostgreSQL:

```bash
docker compose up
```

### Backend (FastAPI)

```bash
cd backend
# Install dependencies (using uv)
uv sync   # creates a virtual environment and installs deps
# Run the API
uv run uvicorn app.main:app --reload
```

### Frontend (Vite + React)

```bash
cd frontend
npm install
npm run dev
```

### VSCode Debugger

A VSCode launch configuration for debugging the FastAPI API is provided in `.vscode/launch.json`.
