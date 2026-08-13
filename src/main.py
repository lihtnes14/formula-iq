from fastapi import FastAPI

from src.api.routes import router


app = FastAPI(
    title="F1 Analytics Copilot",
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "F1 Analytics Copilot API",
        "status": "running",
    }