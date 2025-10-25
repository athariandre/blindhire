from fastapi import FastAPI
from routes import apply, status, claim

app = FastAPI(title="BlindHire Backend")

# Register route groups
app.include_router(apply.router, prefix="/api")
app.include_router(status.router, prefix="/api")
app.include_router(claim.router, prefix="/api")

@app.get("/")
def home():
    return {"message": "BlindHire backend running!"}
