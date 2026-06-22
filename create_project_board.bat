@echo off
echo ============================================================
echo  ModelVault - GitHub Project Board Setup
echo ============================================================
echo.

REM Create the project board
echo Creating GitHub Project board...
gh project create --owner avase33 --title "ModelVault Startup Board" --format json > tmp_project.json
if %errorlevel% neq 0 (
    echo ERROR: Could not create project. Make sure you are logged in with: gh auth login
    pause
    exit /b 1
)

REM Extract project number from JSON
for /f "tokens=*" %%a in ('powershell -command "(Get-Content tmp_project.json | ConvertFrom-Json).number"') do set PROJECT_NUMBER=%%a
del tmp_project.json

echo Project #%PROJECT_NUMBER% created!
echo.

REM ── Create GitHub Issues (startup milestones) ──────────────────────────────
echo Creating startup milestone issues...

gh issue create --repo avase33/modelvault --title "Setup: Initialize PostgreSQL + Redis infrastructure" --body "Set up production-ready PostgreSQL 16 and Redis 7 instances.\n\n**Tasks:**\n- [ ] Provision PostgreSQL instance (RDS or self-hosted)\n- [ ] Provision Redis cluster\n- [ ] Configure connection pooling (PgBouncer)\n- [ ] Set up backups and monitoring\n- [ ] Document connection strings in .env" --label "infrastructure,setup" 2>nul

gh issue create --repo avase33/modelvault --title "Auth: Email verification flow" --body "Implement email verification for new user accounts.\n\n**Tasks:**\n- [ ] SMTP integration (SendGrid or AWS SES)\n- [ ] Verification token generation\n- [ ] Email template design\n- [ ] Resend verification endpoint\n- [ ] Expiry handling (24h)" --label "enhancement,backend" 2>nul

gh issue create --repo avase33/modelvault --title "Model Registry: S3 file storage integration" --body "Replace local file storage with S3-compatible object storage for production.\n\n**Tasks:**\n- [ ] Configure boto3 with IAM roles\n- [ ] Implement presigned URLs for secure uploads\n- [ ] Multipart upload for large model files (>100MB)\n- [ ] CDN integration for fast downloads\n- [ ] Storage cost monitoring" --label "enhancement,backend" 2>nul

gh issue create --repo avase33/modelvault --title "Training: Celery worker integration" --body "Wire up the Celery task queue for async training job execution.\n\n**Tasks:**\n- [ ] Implement run_training_job Celery task\n- [ ] Real-time progress updates via Redis Pub/Sub\n- [ ] Log streaming to database\n- [ ] GPU worker pool configuration\n- [ ] Job timeout and retry logic" --label "enhancement,backend" 2>nul

gh issue create --repo avase33/modelvault --title "Frontend: Model playground (browser inference)" --body "Add a browser-based inference playground where users can test models interactively.\n\n**Tasks:**\n- [ ] Inference form UI per model task type\n- [ ] Response visualizer (JSON, image, text)\n- [ ] Share inference link\n- [ ] Rate limiting indicator\n- [ ] Latency chart" --label "enhancement,frontend" 2>nul

gh issue create --repo avase33/modelvault --title "Infra: Kubernetes Helm chart" --body "Package ModelVault for Kubernetes deployment.\n\n**Tasks:**\n- [ ] Helm chart for backend (FastAPI)\n- [ ] Helm chart for frontend (nginx)\n- [ ] Horizontal Pod Autoscaler config\n- [ ] Ingress with TLS (cert-manager)\n- [ ] Secrets management (Vault or k8s secrets)" --label "infrastructure,devops" 2>nul

gh issue create --repo avase33/modelvault --title "SDK: Python client library" --body "Build and publish a Python SDK for ModelVault.\n\n**Tasks:**\n- [ ] pip install modelvault\n- [ ] Authentication (API key)\n- [ ] Upload model version\n- [ ] Run inference\n- [ ] List/search models\n- [ ] Publish to PyPI" --label "enhancement,sdk" 2>nul

gh issue create --repo avase33/modelvault --title "Monitoring: Prometheus + Grafana dashboards" --body "Set up observability stack for production.\n\n**Tasks:**\n- [ ] FastAPI Prometheus metrics (already instrumented)\n- [ ] Custom metrics: inference latency, job queue depth\n- [ ] Grafana dashboard templates\n- [ ] Alerting rules (PagerDuty)\n- [ ] Error tracking (Sentry)" --label "infrastructure,monitoring" 2>nul

gh issue create --repo avase33/modelvault --title "Feature: Model versioning diff & comparison" --body "Allow users to compare metrics across model versions.\n\n**Tasks:**\n- [ ] Side-by-side metrics comparison UI\n- [ ] Performance regression detection\n- [ ] Version changelog display\n- [ ] Export comparison as PDF report" --label "enhancement,frontend" 2>nul

gh issue create --repo avase33/modelvault --title "Security: Rate limiting + API abuse prevention" --body "Protect the inference API from abuse.\n\n**Tasks:**\n- [ ] Redis-based rate limiting middleware\n- [ ] Per-user and per-key limits\n- [ ] Tiered limits (free/pro/admin)\n- [ ] Abuse detection (anomaly scoring)\n- [ ] Auto-suspend flagged accounts" --label "security,backend" 2>nul

echo.
echo ============================================================
echo  All issues created! Now adding to project board...
echo ============================================================
echo.

REM Add all issues to the project
for /l %%i in (1,1,10) do (
    gh project item-add %PROJECT_NUMBER% --owner avase33 --url https://github.com/avase33/modelvault/issues/%%i 2>nul
)

echo.
echo ============================================================
echo  SUCCESS! Your ModelVault Project Board is ready.
echo.
echo  View it at:
echo  https://github.com/users/avase33/projects/%PROJECT_NUMBER%
echo.
echo  Repository:
echo  https://github.com/avase33/modelvault
echo ============================================================
echo.
pause
