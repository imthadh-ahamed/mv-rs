from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Rating(BaseModel):
    """Rating model for database"""
    user_id: int = Field(..., description="User ID")
    movie_id: int = Field(..., description="Movie ID")
    rating: float = Field(..., ge=1.0, le=5.0, description="Rating value (1-5)")
    timestamp: Optional[int] = Field(None, description="Rating timestamp")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        collection_name = "ratings"
        populate_by_name = True

class RatingRequest(BaseModel):
    """Rating request model"""
    user_id: int = Field(..., description="User ID")
    movie_id: int = Field(..., description="Movie ID")
    rating: float = Field(..., ge=1.0, le=5.0, description="Rating value (1-5)")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "movie_id": 1,
                "rating": 4.5
            }
        }

class RatingResponse(BaseModel):
    """Rating response model"""
    user_id: int = Field(..., description="User ID")
    movie_id: int = Field(..., description="Movie ID")
    rating: float = Field(..., description="Rating value")
    timestamp: Optional[int] = Field(None, description="Rating timestamp")
    created_at: datetime = Field(..., description="Creation timestamp")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "movie_id": 1,
                "rating": 4.5,
                "timestamp": 1234567890,
                "created_at": "2023-01-01T00:00:00"
            }
        }

class RatingPrediction(BaseModel):
    """Rating prediction model"""
    user_id: int = Field(..., description="User ID")
    movie_id: int = Field(..., description="Movie ID")
    predicted_rating: float = Field(..., description="Predicted rating")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Prediction confidence")
    model_used: str = Field(..., description="Model used for prediction")
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": 1,
                "movie_id": 1,
                "predicted_rating": 4.2,
                "confidence": 0.85,
                "model_used": "svd"
            }
        }
