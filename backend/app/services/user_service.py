from typing import List, Optional
from app.models.user import UserResponse, UserStats
from app.database import get_users_collection, get_ratings_collection
from pymongo.collection import Collection
import logging

logger = logging.getLogger(__name__)

class UserService:
    """Service for user operations"""
    
    def __init__(self):
        self.users_collection: Collection = get_users_collection()
        self.ratings_collection: Collection = get_ratings_collection()
    
    async def get_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """Get users with pagination"""
        try:
            cursor = self.users_collection.find().skip(skip).limit(limit)
            users = []
            
            async for doc in cursor:
                user = UserResponse(
                    user_id=doc.get("user_id", doc.get("_id")),
                    age=doc.get("age"),
                    gender=doc.get("gender"),
                    occupation=doc.get("occupation"),
                    zip_code=doc.get("zip_code")
                )
                users.append(user)
            
            return users
            
        except Exception as e:
            logger.error(f"Error getting users: {e}")
            raise
    
    async def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        """Get user by ID"""
        try:
            doc = await self.users_collection.find_one({"user_id": user_id})
            
            if not doc:
                return None
            
            return UserResponse(
                user_id=doc.get("user_id", doc.get("_id")),
                age=doc.get("age"),
                gender=doc.get("gender"),
                occupation=doc.get("occupation"),
                zip_code=doc.get("zip_code")
            )
            
        except Exception as e:
            logger.error(f"Error getting user {user_id}: {e}")
            raise
    
    async def get_user_stats(self, user_id: int) -> dict:
        """Get user statistics"""
        try:
            # Get user's ratings
            ratings_cursor = self.ratings_collection.find({"user_id": user_id})
            ratings = []
            
            async for rating in ratings_cursor:
                ratings.append(rating)
            
            if not ratings:
                return {
                    "user_id": user_id,
                    "total_ratings": 0,
                    "average_rating": 0.0,
                    "favorite_genres": [],
                    "rating_distribution": {}
                }
            
            # Calculate statistics
            total_ratings = len(ratings)
            average_rating = sum(r["rating"] for r in ratings) / total_ratings
            
            # Rating distribution
            rating_distribution = {}
            for rating in ratings:
                rating_value = str(int(rating["rating"]))
                rating_distribution[rating_value] = rating_distribution.get(rating_value, 0) + 1
            
            # Get genre preferences (requires joining with movies)
            # This is a simplified version - in practice, you'd join with movies collection
            favorite_genres = []  # Would need to implement genre analysis
            
            return {
                "user_id": user_id,
                "total_ratings": total_ratings,
                "average_rating": round(average_rating, 2),
                "favorite_genres": favorite_genres,
                "rating_distribution": rating_distribution
            }
            
        except Exception as e:
            logger.error(f"Error getting user stats for user {user_id}: {e}")
            raise
