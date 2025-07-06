from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Movie(BaseModel):
    """Movie model for database"""
    movie_id: int = Field(..., description="Movie ID")
    title: str = Field(..., description="Movie title")
    genre: str = Field(..., description="Movie genre")
    release_date: Optional[str] = Field(None, description="Release date")
    overview: Optional[str] = Field(None, description="Movie overview")
    poster_path: Optional[str] = Field(None, description="Poster image path")
    vote_average: Optional[float] = Field(None, description="Average vote rating")
    vote_count: Optional[int] = Field(None, description="Number of votes")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        collection_name = "movies"
        populate_by_name = True

class MovieResponse(BaseModel):
    """Movie response model"""
    id: int = Field(..., description="Movie ID", alias="movie_id")
    title: str = Field(..., description="Movie title")
    genre: str = Field(..., description="Movie genre")
    release_date: Optional[str] = Field(None, description="Release date")
    overview: Optional[str] = Field(None, description="Movie overview")
    poster_path: Optional[str] = Field(None, description="Poster image path")
    vote_average: Optional[float] = Field(None, description="Average vote rating")
    vote_count: Optional[int] = Field(None, description="Number of votes")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "The Shawshank Redemption",
                "genre": "Drama",
                "release_date": "1994-09-23",
                "overview": "Two imprisoned men bond over a number of years...",
                "poster_path": "/path/to/poster.jpg",
                "vote_average": 9.3,
                "vote_count": 2500000
            }
        }

class MovieStats(BaseModel):
    """Movie statistics model"""
    movie_id: int = Field(..., description="Movie ID")
    title: str = Field(..., description="Movie title")
    total_ratings: int = Field(..., description="Total number of ratings")
    average_rating: float = Field(..., description="Average rating")
    genre: str = Field(..., description="Movie genre")
    popularity_score: float = Field(..., description="Popularity score")

class MovieSearch(BaseModel):
    """Movie search parameters"""
    query: Optional[str] = Field(None, description="Search query")
    genre: Optional[str] = Field(None, description="Filter by genre")
    min_rating: Optional[float] = Field(None, ge=0, le=10, description="Minimum rating")
    max_rating: Optional[float] = Field(None, ge=0, le=10, description="Maximum rating")
    sort_by: str = Field("title", description="Sort by field")
    sort_order: str = Field("asc", pattern="^(asc|desc)$", description="Sort order")
    skip: int = Field(0, ge=0, description="Number of items to skip")
    limit: int = Field(20, ge=1, le=100, description="Number of items to return")
