from fastapi import APIRouter
from app.api.v1 import auth, models, datasets, training, inference

router = APIRouter(prefix="/v1")
router.include_router(auth.router)
router.include_router(models.router)
router.include_router(datasets.router)
router.include_router(training.router)
router.include_router(inference.router)
