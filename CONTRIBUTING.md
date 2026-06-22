# Contributing to ModelVault

Thank you for your interest in contributing!

## Development Setup

\\\ash
git clone https://github.com/avase33/modelvault.git
cd modelvault
cp .env.example .env
docker compose up -d
\\\`n
## Branch Naming

| Type | Pattern | Example |
|---|---|---|
| Feature | feat/description | feat/add-onnx-export |
| Bug fix | fix/description | fix/training-timeout |
| Docs | docs/description | docs/api-reference |

## Commit Messages

Follow Conventional Commits:
\\\`nfeat: add ONNX model export endpoint
fix: resolve training job timeout on large datasets
docs: add API reference for /models/deploy
\\\`n
## Code Style

- Python: Black formatter, isort, type hints required
- TypeScript: ESLint + Prettier, strict mode
- Tests: Minimum 80% coverage for new modules

---

Copyright (c) 2026 Akhil Vase. All rights reserved.