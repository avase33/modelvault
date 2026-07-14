# ModelVault Changelog

## [Unreleased] -- 2026-07-14

### Added
- Pydantic schemas: ModelCreate, ModelResponse with framework and status enums
- ModelRegistry service: joblib artifact save/load/delete with metadata JSON
- Full model CRUD API with status transitions (registered -> training -> deployed)
- Classification metrics: accuracy, precision, recall, F1, AUC-ROC
- Regression metrics: MSE, RMSE, MAE, R2, MAPE
- Data drift detection via z-score comparison
- Semantic versioning utilities: bump major/minor/patch, compare, stability check

## [v1.07141243] -- 2026-07-14
- Run: 20260714124319