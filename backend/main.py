from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import apply, status, claim, admin

app = FastAPI(title="BlindHire Backend")

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route groups
app.include_router(apply.router, prefix="/api")
app.include_router(status.router, prefix="/api")
app.include_router(claim.router, prefix="/api")
app.include_router(admin.router, prefix="/api")

@app.get("/")
def home():
    return {"message": "BlindHire backend running!"}
