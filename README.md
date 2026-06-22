<div align="center">

```
 __  __           _      _ __   __         _ _
|  \/  | ___   __| | ___| |\ \ / /_ _ _ __| | |_
| |\/| |/ _ \ / _` |/ _ \ | \ V / _` | '__| | __|
| |  | | (_) | (_| |  __/ |  | | (_| | |  | | |_
|_|  |_|\___/ \__,_|\___|_|  |_|\__,_|_|  |_|\__|
```

### **AI/ML Model Registry and Deployment Platform**

*Version, deploy, and monitor your machine learning models at startup scale.*

<br/>

[![CI](https://github.com/avase33/modelvault/actions/workflows/ci.yml/badge.svg)](https://github.com/avase33/modelvault/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-Proprietary-red)

<br/>

> **ModelVault** is a production-ready ML model management platform for teams that need full control over their AI assets: register models, track datasets, orchestrate training jobs, and serve predictions via a secure inference API -- all from a single dashboard.

</div>

---

## Why ModelVault?

The ML ecosystem is fragmented. Models live in S3 buckets, experiment results scatter across notebooks, and deploying a new version means SSH-ing into a server. ModelVault centralizes the entire ML lifecycle into one auditable, team-friendly platform.

---

## Feature Highlights

### Model Registry

- Register models from any framework: PyTorch, TensorFlow, scikit-learn, ONNX, HuggingFace, XGBoost
- Full semantic versioning with description and metadata per version
- File upload for model artifacts with SHA-256 checksum verification
- Public/private model visibility

### Dataset Management

- Upload and catalog training datasets with automatic row/column statistics
- Link datasets to training jobs for full lineage tracking
- Storage-agnostic: local filesystem in dev, S3-compatible in production

### Training Job Orchestration

- Queue and monitor CPU/GPU training jobs with real-time log streaming
- Cancel in-flight jobs with graceful cleanup
- Job status lifecycle: QUEUED -> RUNNING -> COMPLETED / FAILED / CANCELLED

### Inference API

- Deploy any registered model version as a live prediction endpoint
- REST API: `POST /api/v1/inference/{model_id}/predict`
- API key authentication for CI/CD and external integrations
- Request logging with latency tracking

### Team Management

- Multi-tenant with FREE / PRO / ADMIN roles
- Full API key management: create, list, revoke
- Per-user model and dataset ownership with visibility controls

---

## Architecture

```
+--------------------------------------------------------------+
|                      CLIENT (Browser)                        |
|  React 18 - TypeScript - Vite - Tailwind CSS                |
|  Zustand (auth) - TanStack Query (server) - Recharts        |
+------------------------+-------------------------------------+
                         |
                         |  REST  +  Bearer JWT  /  X-API-Key
                         |
+------------------------v-------------------------------------+
|                    BACKEND (Python 3.11)                     |
|  FastAPI - SQLAlchemy 2.0 async - Pydantic - Alembic        |
|                                                              |
|  +--------+  +---------+  +----------+  +-----------+      |
|  |  Auth  |  | Models  |  | Training |  | Inference |      |
|  | Routes |  | Routes  |  |  Routes  |  |  Routes   |      |
|  +--------+  +---------+  +----------+  +-----------+      |
|                                         Celery Workers      |
+------------------------+-------------------------------------+
                         |
                    Async ORM (SQLAlchemy)
                         |
       +-----------------+------------------+
       |                                    |
+------v------+                     +-------v------+
| PostgreSQL  |                     |   Redis 7    |
|     16      |                     | (queue/cache)|
+-------------+                     +--------------+
```

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Runtime** | Python 3.11 | Backend server |
| **Framework** | FastAPI | Async REST API |
| **ORM** | SQLAlchemy 2.0 (async) | Database layer |
| **Database** | PostgreSQL 16 | Primary data store |
| **Cache/Queue** | Redis 7, Celery | Background jobs |
| **Auth** | JWT (python-jose) + bcrypt | Stateless auth |
| **Frontend** | React 18, TypeScript, Vite | UI application |
| **Styling** | Tailwind CSS | Dark-theme design |
| **State** | Zustand + TanStack Query | Client state + caching |
| **Charts** | Recharts | Dashboard metrics |
| **Containers** | Docker, Docker Compose | Service orchestration |
| **CI** | GitHub Actions | Build and lint on push |

---

## Quick Start

### Option A: Docker (recommended)

```bash
# 1. Clone
git clone https://github.com/avase33/modelvault.git
cd modelvault

# 2. Configure
cp .env.example .env
# Edit .env -- set SECRET_KEY, DATABASE_URL, REDIS_URL

# 3. Start all services
docker compose up -d
```

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| API | http://localhost:8000 |
| Swagger Docs | http://localhost:8000/docs |

### Option B: Local Development

**Backend**

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example .env
uvicorn app.main:app --reload
```

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

---

## API Reference

All endpoints under `/api/v1`. Auth: `Authorization: Bearer <token>` or `X-API-Key: <key>`.

| Module | Method | Endpoint | Description |
|---|---|---|---|
| **Auth** | POST | `/auth/register` | Create account |
| | POST | `/auth/login` | Get JWT tokens |
| | GET | `/auth/me` | Current user profile |
| **Models** | GET | `/models` | Browse models |
| | POST | `/models` | Create model |
| | POST | `/models/{id}/versions` | Add version |
| | POST | `/models/{id}/versions/{vid}/upload` | Upload artifact |
| **Datasets** | GET | `/datasets` | List datasets |
| | POST | `/datasets` | Create dataset |
| | DELETE | `/datasets/{id}` | Remove dataset |
| **Training** | GET | `/training` | List jobs |
| | POST | `/training` | Create job |
| | GET | `/training/{id}/logs` | Stream logs |
| | POST | `/training/{id}/cancel` | Cancel job |
| **Inference** | POST | `/inference/{model_id}/predict` | Run prediction |
| **API Keys** | GET | `/api-keys` | List keys |
| | POST | `/api-keys` | Create key |
| | DELETE | `/api-keys/{id}` | Revoke key |

---

## Project Structure

```
modelvault/
+-- backend/
|   \-- app/
|       +-- core/            # Config, database, security
|       +-- models/          # SQLAlchemy ORM (User, MLModel, Dataset, TrainingJob)
|       +-- schemas/         # Pydantic request/response schemas
|       +-- api/v1/          # auth | models | datasets | training | inference | api-keys
|       \-- main.py          # App entry, CORS, routers
+-- frontend/
|   \-- src/
|       +-- pages/           # Dashboard, Models, Datasets, Training, API Keys
|       +-- components/      # Layout, shared UI
|       +-- store/           # Zustand auth store
|       \-- lib/             # Axios API client
+-- docker-compose.yml
+-- .env.example
\-- LICENSE
```

---

## Roadmap

- [ ] Model playground -- browser-based live inference
- [ ] Experiment tracking with metric charts
- [ ] Python SDK (`pip install modelvault`)
- [ ] Kubernetes Helm chart for production deployment
- [ ] Model A/B testing and shadow mode
- [ ] Webhooks for job lifecycle events
- [ ] SAML/SSO for enterprise teams
- [ ] Cost and compute analytics dashboard

---

## License

```
Copyright (c) 2026 Akhil Vase. All rights reserved.

This source code is the proprietary property of Akhil Vase.
Unauthorized copying, distribution, or modification is strictly prohibited.
```

---

<div align="center">

**Built for AI teams that need production-grade model ops from day one.**

*ModelVault -- Version it. Deploy it. Monitor it.*

</div>
