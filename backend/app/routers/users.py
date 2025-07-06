from fastapi import APIRouter, HTTPException, Query, Path
from typing import List
from app.models.user import UserResponse
from app.services.user_service import UserService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize user service
user_service = UserService()

@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of users to return")
):
    """Get users with pagination"""
    try:
        users = await user_service.get_users(skip, limit)
        return users
    except Exception as e:
        logger.error(f"Error getting users: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int = Path(..., description="User ID")
):
    """Get a specific user by ID"""
    try:
        user = await user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{user_id}/stats")
async def get_user_stats(
    user_id: int = Path(..., description="User ID")
):
    """Get user statistics"""
    try:
        stats = await user_service.get_user_stats(user_id)
        return stats
    except Exception as e:
        logger.error(f"Error getting user stats for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
