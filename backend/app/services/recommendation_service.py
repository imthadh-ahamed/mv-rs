from typing import List, Optional
from app.models.recommendation import RecommendationResponse, MovieRecommendation
from app.models.rating import RatingPrediction
from app.database import get_movies_collection, get_ratings_collection
from pymongo.collection import Collection
import pickle
import numpy as np
import pandas as pd
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)

class RecommendationService:
    """Service for recommendation operations"""
    
    def __init__(self):
        self.movies_collection: Collection = get_movies_collection()
        self.ratings_collection: Collection = get_ratings_collection()
        self.models = {}
        self.load_models()
    
    def load_models(self):
        """Load ML models from files"""
        try:
            models_path = "ml_models"
            if os.path.exists(models_path):
                # Load saved models if they exist
                model_files = [
                    "popularity_model.pkl",
                    "user_cf_model.pkl",
                    "item_cf_model.pkl",
                    "svd_model.pkl",
                    "content_model.pkl",
                    "hybrid_model.pkl"
                ]
                
                for model_file in model_files:
                    model_path = os.path.join(models_path, model_file)
                    if os.path.exists(model_path):
                        with open(model_path, 'rb') as f:
                            model_name = model_file.replace('.pkl', '')
                            self.models[model_name] = pickle.load(f)
                            logger.info(f"Loaded model: {model_name}")
                
                logger.info(f"Loaded {len(self.models)} models")
            else:
                logger.warning("Models directory not found, using mock recommendations")
                
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            # Continue without models - will use mock data
    
    async def get_recommendations(
        self, 
        user_id: int, 
        model_type: str = "hybrid", 
        limit: int = 10
    ) -> RecommendationResponse:
        """Get movie recommendations for a user"""
        try:
            # If models are loaded, use them
            if model_type in self.models:
                recommendations = await self._get_model_recommendations(
                    user_id, model_type, limit
                )
            else:
                # Fall back to mock recommendations
                recommendations = await self._get_mock_recommendations(user_id, limit)
            
            return RecommendationResponse(
                user_id=user_id,
                recommendations=recommendations,
                model_used=model_type,
                total_count=len(recommendations),
                generated_at=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Error getting recommendations for user {user_id}: {e}")
            raise
    
    async def _get_model_recommendations(
        self, 
        user_id: int, 
        model_type: str, 
        limit: int
    ) -> List[MovieRecommendation]:
        """Get recommendations using loaded ML models"""
        try:
            model = self.models[model_type]
            
            # Get user's ratings
            user_ratings = await self.ratings_collection.find({"user_id": user_id}).to_list(None)
            
            if not user_ratings:
                # If user has no ratings, use popularity-based recommendations
                return await self._get_popular_recommendations(limit)
            
            # Create user-item matrix (simplified version)
            # In a real implementation, you'd use the exact same preprocessing as in training
            user_item_matrix = await self._create_user_item_matrix()
            
            # Get recommendations from model
            if hasattr(model, 'recommend'):
                movie_ids = model.recommend(user_id, limit)
            else:
                # Fallback to popular movies
                return await self._get_popular_recommendations(limit)
            
            # Convert to MovieRecommendation objects
            recommendations = []
            for movie_id in movie_ids:
                movie = await self.movies_collection.find_one({"movie_id": movie_id})
                if movie:
                    recommendation = MovieRecommendation(
                        movie_id=movie_id,
                        title=movie.get("title", ""),
                        genre=movie.get("genre", ""),
                        score=4.0,  # Default score
                        reason=f"Recommended by {model_type} model"
                    )
                    recommendations.append(recommendation)
            
            return recommendations[:limit]
            
        except Exception as e:
            logger.error(f"Error getting model recommendations: {e}")
            return await self._get_mock_recommendations(user_id, limit)
    
    async def _get_mock_recommendations(
        self, 
        user_id: int, 
        limit: int
    ) -> List[MovieRecommendation]:
        """Get mock recommendations when models are not available"""
        try:
            # Get top-rated movies as recommendations
            cursor = self.movies_collection.find().limit(limit)
            recommendations = []
            
            async for movie in cursor:
                recommendation = MovieRecommendation(
                    movie_id=movie.get("movie_id", movie.get("_id")),
                    title=movie.get("title", ""),
                    genre=movie.get("genre", ""),
                    score=4.0,
                    reason="Popular movie recommendation"
                )
                recommendations.append(recommendation)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting mock recommendations: {e}")
            return []
    
    async def _get_popular_recommendations(self, limit: int) -> List[MovieRecommendation]:
        """Get popular movie recommendations"""
        try:
            # Simple popularity based on rating count
            cursor = self.movies_collection.find().limit(limit)
            recommendations = []
            
            async for movie in cursor:
                recommendation = MovieRecommendation(
                    movie_id=movie.get("movie_id", movie.get("_id")),
                    title=movie.get("title", ""),
                    genre=movie.get("genre", ""),
                    score=movie.get("vote_average", 4.0),
                    reason="Popular movie"
                )
                recommendations.append(recommendation)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting popular recommendations: {e}")
            return []
    
    async def _create_user_item_matrix(self) -> pd.DataFrame:
        """Create user-item matrix from ratings"""
        try:
            # Get all ratings
            cursor = self.ratings_collection.find()
            ratings_data = []
            
            async for rating in cursor:
                ratings_data.append({
                    'user_id': rating['user_id'],
                    'movie_id': rating['movie_id'],
                    'rating': rating['rating']
                })
            
            # Create DataFrame
            df = pd.DataFrame(ratings_data)
            
            # Pivot to create user-item matrix
            user_item_matrix = df.pivot_table(
                index='user_id', 
                columns='movie_id', 
                values='rating',
                fill_value=0
            )
            
            return user_item_matrix
            
        except Exception as e:
            logger.error(f"Error creating user-item matrix: {e}")
            return pd.DataFrame()
    
    async def predict_rating(self, user_id: int, movie_id: int) -> RatingPrediction:
        """Predict rating for a user-movie pair"""
        try:
            # Simple prediction logic
            # In practice, you'd use your trained models
            
            # Get user's average rating
            user_ratings = await self.ratings_collection.find({"user_id": user_id}).to_list(None)
            
            if user_ratings:
                user_avg = sum(r['rating'] for r in user_ratings) / len(user_ratings)
            else:
                user_avg = 3.0  # Default
            
            # Get movie's average rating
            movie_ratings = await self.ratings_collection.find({"movie_id": movie_id}).to_list(None)
            
            if movie_ratings:
                movie_avg = sum(r['rating'] for r in movie_ratings) / len(movie_ratings)
            else:
                movie_avg = 3.0  # Default
            
            # Simple prediction: average of user and movie averages
            predicted_rating = (user_avg + movie_avg) / 2
            
            return RatingPrediction(
                user_id=user_id,
                movie_id=movie_id,
                predicted_rating=round(predicted_rating, 2),
                confidence=0.7,  # Mock confidence
                model_used="simple_average"
            )
            
        except Exception as e:
            logger.error(f"Error predicting rating: {e}")
            raise
    
    async def get_similar_movies(self, movie_id: int, limit: int = 10) -> List[MovieRecommendation]:
        """Get movies similar to a given movie"""
        try:
            # Get the target movie
            target_movie = await self.movies_collection.find_one({"movie_id": movie_id})
            
            if not target_movie:
                return []
            
            # Find movies with the same genre
            genre = target_movie.get("genre", "")
            cursor = self.movies_collection.find({
                "genre": genre,
                "movie_id": {"$ne": movie_id}  # Exclude the target movie
            }).limit(limit)
            
            similar_movies = []
            async for movie in cursor:
                recommendation = MovieRecommendation(
                    movie_id=movie.get("movie_id", movie.get("_id")),
                    title=movie.get("title", ""),
                    genre=movie.get("genre", ""),
                    score=0.8,  # Mock similarity score
                    reason=f"Similar genre: {genre}"
                )
                similar_movies.append(recommendation)
            
            return similar_movies
            
        except Exception as e:
            logger.error(f"Error getting similar movies: {e}")
            return []
