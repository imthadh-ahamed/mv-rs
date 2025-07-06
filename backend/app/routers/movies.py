from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Optional
from app.models.movie import Movie, MovieResponse
from app.services.movie_service import MovieService
from app.database import get_movies_collection
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize movie service
movie_service = MovieService()

@router.get("/", response_model=List[MovieResponse])
async def get_movies(
    skip: int = Query(0, ge=0, description="Number of movies to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of movies to return"),
    genre: Optional[str] = Query(None, description="Filter by genre"),
    search: Optional[str] = Query(None, description="Search in movie titles"),
    sort_by: str = Query("title", description="Sort by field"),
    sort_order: str = Query("asc", pattern="^(asc|desc)$", description="Sort order")
):
    """Get movies with filtering and pagination"""
    try:
        movies = await movie_service.get_movies(
            skip=skip,
            limit=limit,
            genre=genre,
            search=search,
            sort_by=sort_by,
            sort_order=sort_order
        )
        return movies
    except Exception as e:
        logger.error(f"Error getting movies: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{movie_id}", response_model=MovieResponse)
async def get_movie(
    movie_id: int = Path(..., description="Movie ID")
):
    """Get a specific movie by ID"""
    try:
        movie = await movie_service.get_movie_by_id(movie_id)
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        return movie
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting movie {movie_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/popular/", response_model=List[MovieResponse])
async def get_popular_movies(
    limit: int = Query(20, ge=1, le=100, description="Number of movies to return")
):
    """Get popular movies based on ratings"""
    try:
        movies = await movie_service.get_popular_movies(limit)
        return movies
    except Exception as e:
        logger.error(f"Error getting popular movies: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/genre/{genre}", response_model=List[MovieResponse])
async def get_movies_by_genre(
    genre: str = Path(..., description="Movie genre"),
    limit: int = Query(20, ge=1, le=100, description="Number of movies to return")
):
    """Get movies by genre"""
    try:
        movies = await movie_service.get_movies_by_genre(genre, limit)
        return movies
    except Exception as e:
        logger.error(f"Error getting movies by genre {genre}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/search/", response_model=List[MovieResponse])
async def search_movies(
    q: str = Query(..., description="Search query"),
    limit: int = Query(20, ge=1, le=100, description="Number of movies to return")
):
    """Search movies by title"""
    try:
        movies = await movie_service.search_movies(q, limit)
        return movies
    except Exception as e:
        logger.error(f"Error searching movies with query '{q}': {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
