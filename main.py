from fastapi import FastAPI
import logging
from contextlib import asynccontextmanager
from fastapi.middleware.cors  import CORSMiddleware
from api.routes import users
from db.session import create_db_and_tables

logger = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create database and tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    logger.info("Creating the database and tables...")
    yield
  
app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(users.router)
