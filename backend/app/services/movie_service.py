from typing import List, Optional
from app.models.movie import MovieResponse, MovieStats
from app.database import get_movies_collection, get_ratings_collection
from motor.motor_asyncio import AsyncIOMotorCollection
import re
import logging

logger = logging.getLogger(__name__)

class MovieService:
    """Service for movie operations"""
    
    def __init__(self):
        self.movies_collection = get_movies_collection()
        self.ratings_collection = get_ratings_collection()
    
    async def get_movies(
        self,
        skip: int = 0,
        limit: int = 20,
        genre: Optional[str] = None,
        search: Optional[str] = None,
        sort_by: str = "title",
        sort_order: str = "asc"
    ) -> List[MovieResponse]:
        """Get movies with filtering and pagination"""
        try:
            # Build query
            query = {}
            
            if genre:
                query["genre"] = {"$regex": genre, "$options": "i"}
            
            if search:
                query["title"] = {"$regex": search, "$options": "i"}
            
            # Build sort
            sort_direction = 1 if sort_order == "asc" else -1
            sort_criteria = [(sort_by, sort_direction)]
            
            # Execute query
            cursor = self.movies_collection.find(query).sort(sort_criteria).skip(skip).limit(limit)
            movies = []
            
            async for doc in cursor:
                movie = MovieResponse(
                    movie_id=doc.get("movie_id", doc.get("_id")),
                    title=doc.get("title", ""),
                    genre=doc.get("genre", ""),
                    release_date=doc.get("release_date"),
                    overview=doc.get("overview"),
                    poster_path=doc.get("poster_path"),
                    vote_average=doc.get("vote_average"),
                    vote_count=doc.get("vote_count")
                )
                movies.append(movie)
            
            return movies
            
        except Exception as e:
            logger.error(f"Error getting movies: {e}")
            raise
    
    async def get_movie_by_id(self, movie_id: int) -> Optional[MovieResponse]:
        """Get movie by ID"""
        try:
            doc = await self.movies_collection.find_one({"movie_id": movie_id})
            
            if not doc:
                return None
            
            return MovieResponse(
                movie_id=doc.get("movie_id", doc.get("_id")),
                title=doc.get("title", ""),
                genre=doc.get("genre", ""),
                release_date=doc.get("release_date"),
                overview=doc.get("overview"),
                poster_path=doc.get("poster_path"),
                vote_average=doc.get("vote_average"),
                vote_count=doc.get("vote_count")
            )
            
        except Exception as e:
            logger.error(f"Error getting movie {movie_id}: {e}")
            raise
    
    async def get_popular_movies(self, limit: int = 20) -> List[MovieResponse]:
        """Get popular movies based on ratings"""
        try:
            # Aggregate to get movies with highest average ratings
            pipeline = [
                {
                    "$lookup": {
                        "from": "ratings",
                        "localField": "movie_id",
                        "foreignField": "movie_id",
                        "as": "ratings"
                    }
                },
                {
                    "$match": {
                        "ratings.10": {"$exists": True}  # At least 10 ratings
                    }
                },
                {
                    "$addFields": {
                        "avg_rating": {"$avg": "$ratings.rating"},
                        "rating_count": {"$size": "$ratings"}
                    }
                },
                {
                    "$sort": {"avg_rating": -1, "rating_count": -1}
                },
                {
                    "$limit": limit
                }
            ]
            
            cursor = self.movies_collection.aggregate(pipeline)
            movies = []
            
            async for doc in cursor:
                movie = MovieResponse(
                    movie_id=doc.get("movie_id", doc.get("_id")),
                    title=doc.get("title", ""),
                    genre=doc.get("genre", ""),
                    release_date=doc.get("release_date"),
                    overview=doc.get("overview"),
                    poster_path=doc.get("poster_path"),
                    vote_average=doc.get("avg_rating", doc.get("vote_average")),
                    vote_count=doc.get("rating_count", doc.get("vote_count"))
                )
                movies.append(movie)
            
            return movies
            
        except Exception as e:
            logger.error(f"Error getting popular movies: {e}")
            raise
    
    async def get_movies_by_genre(self, genre: str, limit: int = 20) -> List[MovieResponse]:
        """Get movies by genre"""
        try:
            query = {"genre": {"$regex": genre, "$options": "i"}}
            cursor = self.movies_collection.find(query).limit(limit)
            movies = []
            
            async for doc in cursor:
                movie = MovieResponse(
                    movie_id=doc.get("movie_id", doc.get("_id")),
                    title=doc.get("title", ""),
                    genre=doc.get("genre", ""),
                    release_date=doc.get("release_date"),
                    overview=doc.get("overview"),
                    poster_path=doc.get("poster_path"),
                    vote_average=doc.get("vote_average"),
                    vote_count=doc.get("vote_count")
                )
                movies.append(movie)
            
            return movies
            
        except Exception as e:
            logger.error(f"Error getting movies by genre {genre}: {e}")
            raise
    
    async def search_movies(self, query: str, limit: int = 20) -> List[MovieResponse]:
        """Search movies by title"""
        try:
            search_query = {"title": {"$regex": query, "$options": "i"}}
            cursor = self.movies_collection.find(search_query).limit(limit)
            movies = []
            
            async for doc in cursor:
                movie = MovieResponse(
                    movie_id=doc.get("movie_id", doc.get("_id")),
                    title=doc.get("title", ""),
                    genre=doc.get("genre", ""),
                    release_date=doc.get("release_date"),
                    overview=doc.get("overview"),
                    poster_path=doc.get("poster_path"),
                    vote_average=doc.get("vote_average"),
                    vote_count=doc.get("vote_count")
                )
                movies.append(movie)
            
            return movies
            
        except Exception as e:
            logger.error(f"Error searching movies with query '{query}': {e}")
            raise
