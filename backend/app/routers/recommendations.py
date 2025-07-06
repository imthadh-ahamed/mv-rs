from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from app.models.recommendation import RecommendationRequest, RecommendationResponse
from app.services.recommendation_service import RecommendationService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize recommendation service
recommendation_service = RecommendationService()

@router.post("/", response_model=RecommendationResponse)
async def get_recommendations(
    request: RecommendationRequest
):
    """Get movie recommendations for a user"""
    try:
        recommendations = await recommendation_service.get_recommendations(
            user_id=request.user_id,
            model_type=request.model_type,
            limit=request.limit
        )
        return recommendations
    except Exception as e:
        logger.error(f"Error getting recommendations for user {request.user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=RecommendationResponse)
async def get_recommendations_by_params(
    user_id: int = Query(..., description="User ID"),
    model_type: str = Query("hybrid", description="Model type (popularity, collaborative, content, hybrid)"),
    limit: int = Query(10, ge=1, le=50, description="Number of recommendations")
):
    """Get movie recommendations using query parameters"""
    try:
        recommendations = await recommendation_service.get_recommendations(
            user_id=user_id,
            model_type=model_type,
            limit=limit
        )
        return recommendations
    except Exception as e:
        logger.error(f"Error getting recommendations for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/predict-rating")
async def predict_rating(
    user_id: int = Query(..., description="User ID"),
    movie_id: int = Query(..., description="Movie ID")
):
    """Predict rating for a user-movie pair"""
    try:
        prediction = await recommendation_service.predict_rating(user_id, movie_id)
        return prediction
    except Exception as e:
        logger.error(f"Error predicting rating for user {user_id}, movie {movie_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/similar/{movie_id}")
async def get_similar_movies(
    movie_id: int,
    limit: int = Query(10, ge=1, le=50, description="Number of similar movies")
):
    """Get movies similar to a given movie"""
    try:
        similar_movies = await recommendation_service.get_similar_movies(movie_id, limit)
        return similar_movies
    except Exception as e:
        logger.error(f"Error getting similar movies for movie {movie_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
