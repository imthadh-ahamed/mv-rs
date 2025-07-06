from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class MovieRecommendation(BaseModel):
    """Individual movie recommendation"""
    movie_id: int = Field(..., description="Movie ID")
    title: str = Field(..., description="Movie title")
    genre: str = Field(..., description="Movie genre")
    score: float = Field(..., description="Recommendation score")
    reason: Optional[str] = Field(None, description="Reason for recommendation")

class RecommendationRequest(BaseModel):
    """Recommendation request model"""
    user_id: int = Field(..., description="User ID")
    model_type: str = Field("hybrid", description="Model type (popularity, collaborative, content, hybrid)")
    limit: int = Field(10, ge=1, le=50, description="Number of recommendations")
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": 1,
                "model_type": "hybrid",
                "limit": 10
            }
        }

class RecommendationResponse(BaseModel):
    """Recommendation response model"""
    user_id: int = Field(..., description="User ID")
    recommendations: List[MovieRecommendation] = Field(..., description="List of movie recommendations")
    model_used: str = Field(..., description="Model used for recommendations")
    total_count: int = Field(..., description="Total number of recommendations")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Generation timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": 1,
                "recommendations": [
                    {
                        "movie_id": 1,
                        "title": "The Shawshank Redemption",
                        "genre": "Drama",
                        "score": 4.8,
                        "reason": "High rating similarity with other users"
                    }
                ],
                "model_used": "hybrid",
                "total_count": 1,
                "generated_at": "2023-01-01T00:00:00"
            }
        }

class SimilarMovieResponse(BaseModel):
    """Similar movies response model"""
    movie_id: int = Field(..., description="Source movie ID")
    similar_movies: List[MovieRecommendation] = Field(..., description="List of similar movies")
    total_count: int = Field(..., description="Total number of similar movies")
    
    class Config:
        schema_extra = {
            "example": {
                "movie_id": 1,
                "similar_movies": [
                    {
                        "movie_id": 2,
                        "title": "The Godfather",
                        "genre": "Drama",
                        "score": 0.95,
                        "reason": "Similar genre and high user ratings"
                    }
                ],
                "total_count": 1
            }
        }
