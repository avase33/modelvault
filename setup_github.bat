@echo off
echo ============================================
echo  ModelVault - GitHub Setup Script
echo ============================================

REM Create GitHub repo via gh CLI
gh repo create modelvault --public --description "AI/ML Model Management Platform - FastAPI + React startup project" --homepage "https://github.com/avase33/modelvault"

REM Initialize git
git init
git add .
git commit -m "feat: initial commit - ModelVault AI/ML Platform

Full-stack AI/ML platform startup project:
- FastAPI backend with JWT auth, model registry, dataset management,
  training job orchestration, and inference API
- React + TypeScript frontend with dashboard, model browser,
  dataset manager, training monitor, and API key management
- PostgreSQL + Redis + Celery for production workloads
- Docker Compose for local development
- GitHub Actions CI/CD pipeline"

git branch -M main
git remote add origin https://github.com/avase33/modelvault.git
git push -u origin main

echo.
echo Done! Visit: https://github.com/avase33/modelvault
pause
