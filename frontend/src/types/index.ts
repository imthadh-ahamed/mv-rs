// Movie and rating types
export interface Movie {
  id: number;
  title: string;
  genre: string;
  release_date?: string;
  overview?: string;
  poster_path?: string;
  vote_average?: number;
  vote_count?: number;
}

export interface Rating {
  user_id: number;
  movie_id: number;
  rating: number;
  timestamp?: number;
}

export interface User {
  id: number;
  age?: number;
  gender?: string;
  occupation?: string;
  zip_code?: string;
}

// API response types
export interface MovieRecommendation {
  movie_id: number;
  title: string;
  genre: string;
  score: number;
  reason?: string;
}

export interface RecommendationResponse {
  recommendations: MovieRecommendation[];
  model_used: string;
  total_count: number;
}

export interface RatingPrediction {
  user_id: number;
  movie_id: number;
  predicted_rating: number;
  confidence: number;
}

export interface ApiError {
  detail: string;
  status_code: number;
}

// Component props types
export interface MovieCardProps {
  movie: Movie;
  onRate?: (rating: number) => void;
  userRating?: number;
  showRating?: boolean;
}

export interface RecommendationCardProps {
  recommendation: MovieRecommendation;
  onRate?: (rating: number) => void;
}

export interface RatingStarsProps {
  rating: number;
  onRate?: (rating: number) => void;
  readonly?: boolean;
  size?: 'sm' | 'md' | 'lg';
}

// Filter and search types
export interface FilterOptions {
  genre?: string;
  minRating?: number;
  maxRating?: number;
  sortBy?: 'popularity' | 'rating' | 'release_date' | 'title';
  sortOrder?: 'asc' | 'desc';
}

export interface SearchParams {
  query?: string;
  page?: number;
  limit?: number;
  filters?: FilterOptions;
}

// Store types
export interface UserState {
  userId: number | null;
  ratings: Rating[];
  preferences: {
    favoriteGenres: string[];
    dislikedGenres: string[];
  };
  setUserId: (id: number) => void;
  addRating: (rating: Rating) => void;
  updateRating: (rating: Rating) => void;
  setPreferences: (preferences: UserState['preferences']) => void;
}

export interface RecommendationState {
  recommendations: MovieRecommendation[];
  loading: boolean;
  error: string | null;
  lastUpdated: Date | null;
  modelUsed: string | null;
  fetchRecommendations: (userId: number, model?: string) => Promise<void>;
  clearRecommendations: () => void;
}

// API client types
export interface ApiClient {
  getRecommendations: (userId: number, model?: string) => Promise<RecommendationResponse>;
  predictRating: (userId: number, movieId: number) => Promise<RatingPrediction>;
  submitRating: (rating: Rating) => Promise<void>;
  getMovies: (params?: SearchParams) => Promise<{ movies: Movie[]; total: number }>;
  getMovie: (movieId: number) => Promise<Movie>;
  getPopularMovies: (limit?: number) => Promise<Movie[]>;
}
