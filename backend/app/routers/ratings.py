from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List
from app.models.rating import RatingRequest, RatingResponse
from app.services.rating_service import RatingService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize rating service
rating_service = RatingService()

@router.post("/", response_model=RatingResponse)
async def create_rating(
    request: RatingRequest
):
    """Create or update a rating"""
    try:
        rating = await rating_service.create_or_update_rating(
            user_id=request.user_id,
            movie_id=request.movie_id,
            rating=request.rating
        )
        return rating
    except Exception as e:
        logger.error(f"Error creating rating: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/user/{user_id}", response_model=List[RatingResponse])
async def get_user_ratings(
    user_id: int,
    skip: int = Query(0, ge=0, description="Number of ratings to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of ratings to return")
):
    """Get ratings for a specific user"""
    try:
        ratings = await rating_service.get_user_ratings(user_id, skip, limit)
        return ratings
    except Exception as e:
        logger.error(f"Error getting ratings for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/movie/{movie_id}", response_model=List[RatingResponse])
async def get_movie_ratings(
    movie_id: int,
    skip: int = Query(0, ge=0, description="Number of ratings to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of ratings to return")
):
    """Get ratings for a specific movie"""
    try:
        ratings = await rating_service.get_movie_ratings(movie_id, skip, limit)
        return ratings
    except Exception as e:
        logger.error(f"Error getting ratings for movie {movie_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=List[RatingResponse])
async def get_all_ratings(
    skip: int = Query(0, ge=0, description="Number of ratings to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of ratings to return")
):
    """Get all ratings with pagination"""
    try:
        ratings = await rating_service.get_all_ratings(skip, limit)
        return ratings
    except Exception as e:
        logger.error(f"Error getting all ratings: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{user_id}/{movie_id}")
async def delete_rating(
    user_id: int,
    movie_id: int
):
    """Delete a specific rating"""
    try:
        success = await rating_service.delete_rating(user_id, movie_id)
        if not success:
            raise HTTPException(status_code=404, detail="Rating not found")
        return {"message": "Rating deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting rating: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
