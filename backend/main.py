from fastapi import FastAPI
from backend.routers import customer , account ,loan ,repayment , credit_history , employment , validation , prediction

app = FastAPI()

app.include_router(customer.router)
app.include_router(account.router)
app.include_router(loan.router)
app.include_router(repayment.router)
app.include_router(credit_history.router)
app.include_router(employment.router)
app.include_router(validation.router)
app.include_router(prediction.router)

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
    