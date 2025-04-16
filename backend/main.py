from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import traceback

# Change from relative to absolute imports
import postgres_db.models as models
from postgres_db.database import engine
from backend import users

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create all tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Chronic Disease Management API")

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:8501",
    "http://127.0.0.1:8501",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"detail": f"An error occurred: {str(exc)}"}
    )

# Include routers
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Chronic Disease Management API"}