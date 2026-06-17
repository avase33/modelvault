# 🧠 ModelVault — AI/ML Model Management Platform

> The open platform to host, version, and deploy your machine learning models at scale.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)
![React](https://img.shields.io/badge/React-18-61DAFB)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

- **Model Registry** — Upload, version, and tag ML models (PyTorch, TensorFlow, scikit-learn, ONNX, HuggingFace, XGBoost)
- **Dataset Management** — Store and share training datasets with automatic stats
- **Training Job Orchestration** — Queue, monitor, and cancel training runs (CPU/GPU)
- **Inference API** — Deploy models and run predictions via REST API or Python SDK
- **API Keys** — Secure programmatic access for integrations and CI/CD
- **Multi-tenant** — Full user management with FREE / PRO / ADMIN roles
- **CI/CD Ready** — GitHub Actions pipeline with Docker build and deploy

---

## 🏗️ Architecture

```
modelvault/
├── backend/               # Python + FastAPI
│   ├── app/
│   │   ├── core/          # Config, DB, Security
│   │   ├── models/        # SQLAlchemy ORM models
│   │   ├── schemas/       # Pydantic schemas
│   │   └── api/v1/        # REST endpoints
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/              # React + Vite + Tailwind
│   ├── src/
│   │   ├── pages/         # Dashboard, Models, Datasets, Training, API Keys
│   │   ├── components/    # Layout, shared components
│   │   ├── store/         # Zustand state management
│   │   └── lib/           # Axios API client
│   └── Dockerfile
├── docker-compose.yml     # Full stack local dev
└── .github/workflows/     # CI/CD pipeline
```

---

## 🚀 Quick Start

### With Docker (recommended)

```bash
git clone https://github.com/avase33/modelvault.git
cd modelvault
cp .env.example .env
docker compose up -d
```

- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000

### Local Development

**Backend:**
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env  # edit as needed
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## 📡 API Reference

### Authentication
```http
POST /api/v1/auth/register   # Create account
POST /api/v1/auth/login      # Get JWT tokens
GET  /api/v1/auth/me         # Current user
```

### Models
```http
GET    /api/v1/models              # Browse public models
POST   /api/v1/models              # Create model
GET    /api/v1/models/{id}         # Get model details
POST   /api/v1/models/{id}/versions  # Add version
POST   /api/v1/models/{id}/versions/{vid}/upload  # Upload file
```

### Inference
```http
POST /api/v1/inference/{model_id}/predict
# Headers: X-API-Key: mv_your_key OR Authorization: Bearer <token>
# Body: {"inputs": {...}, "parameters": {...}}
```

### Training
```http
GET  /api/v1/training         # List jobs
POST /api/v1/training         # Create job
GET  /api/v1/training/{id}    # Job status
POST /api/v1/training/{id}/cancel
GET  /api/v1/training/{id}/logs
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11, FastAPI, SQLAlchemy 2.0 (async) |
| Database | PostgreSQL 16 |
| Cache / Queue | Redis 7, Celery |
| Auth | JWT (python-jose) + bcrypt |
| Frontend | React 18, TypeScript, Vite, Tailwind CSS |
| State | Zustand + TanStack Query |
| Charts | Recharts |
| Containerization | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Storage | Local FS (dev) / S3-compatible (prod) |

---

## 🗺️ Roadmap

- [ ] Model playground (browser-based inference)
- [ ] Experiment tracking (MLflow integration)
- [ ] Kubernetes Helm chart
- [ ] Python SDK (`pip install modelvault`)
- [ ] Model comparison & A/B testing
- [ ] Webhooks for job events
- [ ] SAML/SSO for enterprise
- [ ] Cost & compute analytics

---

## 🤝 Contributing

1. Fork the repo
2. Create your branch: `git checkout -b feature/awesome-feature`
3. Commit your changes: `git commit -m 'Add awesome feature'`
4. Push to the branch: `git push origin feature/awesome-feature`
5. Open a Pull Request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

Built with ❤️ by the ModelVault team.
