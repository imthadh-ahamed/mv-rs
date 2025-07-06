import React from 'react';
import { Heart, Star, Calendar } from 'lucide-react';
import RatingStars from './RatingStars';
import type { Movie } from '@/types';

interface MovieCardProps {
  movie: Movie;
  onRate?: (rating: number) => void;
  userRating?: number;
  showRating?: boolean;
}

export default function MovieCard({ 
  movie, 
  onRate, 
  userRating, 
  showRating = true 
}: MovieCardProps) {
  const [isLiked, setIsLiked] = React.useState(false);
  
  const posterUrl = movie.poster_path 
    ? `https://image.tmdb.org/t/p/w500${movie.poster_path}`
    : `https://via.placeholder.com/300x450/374151/ffffff?text=${encodeURIComponent(movie.title)}`;

  const getGenreColor = (genre: string) => {
    const colors: Record<string, string> = {
      Action: 'bg-red-500',
      Comedy: 'bg-yellow-500',
      Drama: 'bg-green-600',
      Horror: 'bg-red-700',
      Romance: 'bg-rose-500',
      'Science Fiction': 'bg-cyan-500',
      Adventure: 'bg-orange-500',
      Animation: 'bg-purple-500',
      Crime: 'bg-gray-700',
      Documentary: 'bg-blue-500',
      Family: 'bg-pink-500',
      Fantasy: 'bg-violet-500',
      Musical: 'bg-indigo-500',
      Mystery: 'bg-gray-600',
      Thriller: 'bg-slate-600',
      War: 'bg-amber-700',
      Western: 'bg-orange-700',
    };
    return colors[genre] || 'bg-gray-500';
  };

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-200">
      <div className="relative">
        <img
          src={posterUrl}
          alt={movie.title}
          className="w-full h-64 object-cover"
        />
        <button
          onClick={() => setIsLiked(!isLiked)}
          className="absolute top-2 right-2 p-2 rounded-full bg-white bg-opacity-80 hover:bg-opacity-100 transition-all"
        >
          <Heart
            className={`w-5 h-5 ${
              isLiked ? 'fill-red-500 text-red-500' : 'text-gray-600'
            }`}
          />
        </button>
      </div>
      
      <div className="p-4">
        <h3 className="font-semibold text-lg mb-2 line-clamp-2">{movie.title}</h3>
        
        <div className="flex items-center gap-2 mb-2">
          <span
            className={`${getGenreColor(movie.genre)} text-white text-xs px-2 py-1 rounded-full`}
          >
            {movie.genre}
          </span>
          {movie.release_date && (
            <div className="flex items-center text-gray-500 text-sm">
              <Calendar className="w-4 h-4 mr-1" />
              {new Date(movie.release_date).getFullYear()}
            </div>
          )}
        </div>

        {movie.vote_average && (
          <div className="flex items-center mb-2">
            <Star className="w-4 h-4 text-yellow-400 fill-current mr-1" />
            <span className="text-sm text-gray-600">
              {movie.vote_average.toFixed(1)} ({movie.vote_count} votes)
            </span>
          </div>
        )}

        {movie.overview && (
          <p className="text-gray-600 text-sm mb-3 line-clamp-3">
            {movie.overview}
          </p>
        )}

        {showRating && (
          <div className="border-t pt-3">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-500">Rate this movie:</span>
              <RatingStars
                rating={userRating || 0}
                onRate={onRate}
                size="sm"
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
