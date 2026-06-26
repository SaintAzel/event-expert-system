from fastapi import FastAPI

app = FastAPI(
    title="Event Expert System API",
    description="Expert System for Event Readiness Assessment",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {
        "message": "Event Expert System API",
        "version": "1.0.0",
    }


@app.get("/health")
async def health():
    return {
        "status": "ok",
    }