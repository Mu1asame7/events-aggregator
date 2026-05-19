from fastapi import FastAPI

from app.api.v1 import health, sync

app = FastAPI(
    title="Events Aggregator",
    version="1.0.0",
)


app.include_router(health.router, prefix="/api", tags=["Healts"])
app.include_router(sync.router, prefix="/api", tags=["Sync"])


@app.get("/")
async def root():
    return {"message": "Servise running"}
