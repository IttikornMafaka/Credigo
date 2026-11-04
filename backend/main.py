from fastapi import FastAPI
from backend.routers import customer

app = FastAPI()

app.include_router(customer.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Credigo API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }