from fastapi import APIRouter

router = APIRouter(tags=["System"])


@router.get("/")
async def root():
    return {
        "message": "Event Expert System API",
        "version": "1.0.0",
    }


@router.get("/version")
async def version():
    return {
        "api_version": "1.0.0",
        "knowledge_version": "1.0.0",
    }