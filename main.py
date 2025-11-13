from fastapi import FastAPI
from app.api import auth

# Initialize FastAPI application
app = FastAPI(
    title="SNAMS API",
    description="Smart Network Automation & Monitoring System API",
    version="0.1.0",
)

# --- Include Routers ---
app.include_router(auth.router, prefix="/api/v1")

# --- Root Endpoint ---
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "SNAMS API running. Navigate to /docs for OpenAPI specification."}
