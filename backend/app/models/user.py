from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class User(BaseModel):
    """User model for database"""
    user_id: int = Field(..., description="User ID")
    age: Optional[int] = Field(None, description="User age")
    gender: Optional[str] = Field(None, description="User gender")
    occupation: Optional[str] = Field(None, description="User occupation")
    zip_code: Optional[str] = Field(None, description="User zip code")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        collection_name = "users"
        populate_by_name = True

class UserResponse(BaseModel):
    """User response model"""
    id: int = Field(..., description="User ID", alias="user_id")
    age: Optional[int] = Field(None, description="User age")
    gender: Optional[str] = Field(None, description="User gender")
    occupation: Optional[str] = Field(None, description="User occupation")
    zip_code: Optional[str] = Field(None, description="User zip code")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "age": 24,
                "gender": "M",
                "occupation": "technician",
                "zip_code": "85711"
            }
        }

class UserStats(BaseModel):
    """User statistics model"""
    user_id: int = Field(..., description="User ID")
    total_ratings: int = Field(..., description="Total number of ratings given")
    average_rating: float = Field(..., description="Average rating given")
    favorite_genres: list[str] = Field(..., description="Top favorite genres")
    most_rated_genre: str = Field(..., description="Most rated genre")
    rating_distribution: dict[str, int] = Field(..., description="Rating distribution")

class UserPreferences(BaseModel):
    """User preferences model"""
    user_id: int = Field(..., description="User ID")
    favorite_genres: list[str] = Field([], description="Favorite genres")
    disliked_genres: list[str] = Field([], description="Disliked genres")
    preferred_rating_range: tuple[float, float] = Field((1.0, 10.0), description="Preferred rating range")
    updated_at: datetime = Field(default_factory=datetime.utcnow)
