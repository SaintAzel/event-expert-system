from fastapi import FastAPI

app = FastAPI(
    title="Event Expert System API",
    version="1.0.0",
    description="Expert System for Event Readiness Assessment"
)


@app.get("/")
def root():
    return {
        "message": "Event Expert System API",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }