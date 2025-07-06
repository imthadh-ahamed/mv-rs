from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from typing import Optional
import logging
from app.config import get_settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global database connection
_database: Optional[AsyncIOMotorDatabase] = None
_client: Optional[AsyncIOMotorClient] = None

def get_database() -> AsyncIOMotorDatabase:
    """Get database connection"""
    global _database, _client
    
    if _database is None:
        try:
            settings = get_settings()
            _client = AsyncIOMotorClient(settings.MONGODB_URL)
            _database = _client[settings.DATABASE_NAME]
            logger.info(f"Connected to MongoDB database: {settings.DATABASE_NAME}")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    return _database

def close_database():
    """Close database connection"""
    global _database, _client
    
    if _client:
        _client.close()
        _client = None
        _database = None
        logger.info("MongoDB connection closed")

# Collections
def get_movies_collection() -> AsyncIOMotorCollection:
    """Get movies collection"""
    db = get_database()
    return db.movies

def get_ratings_collection() -> AsyncIOMotorCollection:
    """Get ratings collection"""
    db = get_database()
    return db.ratings

def get_users_collection() -> AsyncIOMotorCollection:
    """Get users collection"""
    db = get_database()
    return db.users

def get_recommendations_collection() -> AsyncIOMotorCollection:
    """Get recommendations collection"""
    db = get_database()
    return db.recommendations

# Database initialization
async def init_database():
    """Initialize database with indexes"""
    try:
        db = get_database()
        
        # Create indexes for better performance
        movies_collection = get_movies_collection()
        ratings_collection = get_ratings_collection()
        users_collection = get_users_collection()
        recommendations_collection = get_recommendations_collection()
        
        # Movies indexes
        movies_collection.create_index("movie_id", unique=True)
        movies_collection.create_index("title")
        movies_collection.create_index("genre")
        
        # Ratings indexes
        ratings_collection.create_index([("user_id", 1), ("movie_id", 1)], unique=True)
        ratings_collection.create_index("user_id")
        ratings_collection.create_index("movie_id")
        
        # Users indexes
        users_collection.create_index("user_id", unique=True)
        
        # Recommendations indexes
        recommendations_collection.create_index([("user_id", 1), ("model_type", 1)])
        recommendations_collection.create_index("user_id")
        recommendations_collection.create_index("created_at")
        
        logger.info("Database initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
