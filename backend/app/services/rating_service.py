from typing import List, Optional
from app.models.rating import RatingResponse
from app.database import get_ratings_collection
from pymongo.collection import Collection
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class RatingService:
    """Service for rating operations"""
    
    def __init__(self):
        self.ratings_collection: Collection = get_ratings_collection()
    
    async def create_or_update_rating(
        self, 
        user_id: int, 
        movie_id: int, 
        rating: float
    ) -> RatingResponse:
        """Create or update a rating"""
        try:
            # Check if rating already exists
            existing_rating = await self.ratings_collection.find_one({
                "user_id": user_id,
                "movie_id": movie_id
            })
            
            rating_data = {
                "user_id": user_id,
                "movie_id": movie_id,
                "rating": rating,
                "updated_at": datetime.utcnow()
            }
            
            if existing_rating:
                # Update existing rating
                await self.ratings_collection.update_one(
                    {"user_id": user_id, "movie_id": movie_id},
                    {"$set": rating_data}
                )
                created_at = existing_rating.get("created_at", datetime.utcnow())
            else:
                # Create new rating
                rating_data["created_at"] = datetime.utcnow()
                await self.ratings_collection.insert_one(rating_data)
                created_at = rating_data["created_at"]
            
            return RatingResponse(
                user_id=user_id,
                movie_id=movie_id,
                rating=rating,
                timestamp=existing_rating.get("timestamp") if existing_rating else None,
                created_at=created_at
            )
            
        except Exception as e:
            logger.error(f"Error creating/updating rating: {e}")
            raise
    
    async def get_user_ratings(
        self, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[RatingResponse]:
        """Get ratings for a specific user"""
        try:
            cursor = self.ratings_collection.find({"user_id": user_id}).skip(skip).limit(limit)
            ratings = []
            
            async for doc in cursor:
                rating = RatingResponse(
                    user_id=doc["user_id"],
                    movie_id=doc["movie_id"],
                    rating=doc["rating"],
                    timestamp=doc.get("timestamp"),
                    created_at=doc.get("created_at", datetime.utcnow())
                )
                ratings.append(rating)
            
            return ratings
            
        except Exception as e:
            logger.error(f"Error getting ratings for user {user_id}: {e}")
            raise
    
    async def get_movie_ratings(
        self, 
        movie_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[RatingResponse]:
        """Get ratings for a specific movie"""
        try:
            cursor = self.ratings_collection.find({"movie_id": movie_id}).skip(skip).limit(limit)
            ratings = []
            
            async for doc in cursor:
                rating = RatingResponse(
                    user_id=doc["user_id"],
                    movie_id=doc["movie_id"],
                    rating=doc["rating"],
                    timestamp=doc.get("timestamp"),
                    created_at=doc.get("created_at", datetime.utcnow())
                )
                ratings.append(rating)
            
            return ratings
            
        except Exception as e:
            logger.error(f"Error getting ratings for movie {movie_id}: {e}")
            raise
    
    async def get_all_ratings(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[RatingResponse]:
        """Get all ratings with pagination"""
        try:
            cursor = self.ratings_collection.find().skip(skip).limit(limit)
            ratings = []
            
            async for doc in cursor:
                rating = RatingResponse(
                    user_id=doc["user_id"],
                    movie_id=doc["movie_id"],
                    rating=doc["rating"],
                    timestamp=doc.get("timestamp"),
                    created_at=doc.get("created_at", datetime.utcnow())
                )
                ratings.append(rating)
            
            return ratings
            
        except Exception as e:
            logger.error(f"Error getting all ratings: {e}")
            raise
    
    async def delete_rating(self, user_id: int, movie_id: int) -> bool:
        """Delete a specific rating"""
        try:
            result = await self.ratings_collection.delete_one({
                "user_id": user_id,
                "movie_id": movie_id
            })
            
            return result.deleted_count > 0
            
        except Exception as e:
            logger.error(f"Error deleting rating: {e}")
            raise
