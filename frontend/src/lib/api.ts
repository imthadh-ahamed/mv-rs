import axios, { AxiosInstance, AxiosError } from 'axios';
import { toast } from 'react-hot-toast';
import type {
  Movie,
  Rating,
  RecommendationResponse,
  RatingPrediction,
  SearchParams,
  ApiError,
  ApiClient as ApiClientType,
} from '@/types';

class ApiClient implements ApiClientType {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        // Add auth token if available
        const token = localStorage.getItem('authToken');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError<ApiError>) => {
        const message = error.response?.data?.detail || error.message || 'An error occurred';
        toast.error(message);
        return Promise.reject(error);
      }
    );
  }

  async getRecommendations(userId: number, model?: string): Promise<RecommendationResponse> {
    const params = new URLSearchParams();
    params.append('user_id', userId.toString());
    if (model) params.append('model', model);

    const response = await this.client.get(`/recommendations?${params}`);
    return response.data;
  }

  async predictRating(userId: number, movieId: number): Promise<RatingPrediction> {
    const response = await this.client.post('/predict-rating', {
      user_id: userId,
      movie_id: movieId,
    });
    return response.data;
  }

  async submitRating(rating: Rating): Promise<void> {
    await this.client.post('/ratings', rating);
  }

  async getMovies(params?: SearchParams): Promise<{ movies: Movie[]; total: number }> {
    const searchParams = new URLSearchParams();
    
    if (params?.query) searchParams.append('query', params.query);
    if (params?.page) searchParams.append('page', params.page.toString());
    if (params?.limit) searchParams.append('limit', params.limit.toString());
    
    if (params?.filters) {
      const { genre, minRating, maxRating, sortBy, sortOrder } = params.filters;
      if (genre) searchParams.append('genre', genre);
      if (minRating) searchParams.append('min_rating', minRating.toString());
      if (maxRating) searchParams.append('max_rating', maxRating.toString());
      if (sortBy) searchParams.append('sort_by', sortBy);
      if (sortOrder) searchParams.append('sort_order', sortOrder);
    }

    const response = await this.client.get(`/movies?${searchParams}`);
    return response.data;
  }

  async getMovie(movieId: number): Promise<Movie> {
    const response = await this.client.get(`/movies/${movieId}`);
    return response.data;
  }

  async getPopularMovies(limit: number = 20): Promise<Movie[]> {
    const response = await this.client.get(`/movies/popular?limit=${limit}`);
    return response.data;
  }

  async getMoviesByGenre(genre: string, limit: number = 20): Promise<Movie[]> {
    const response = await this.client.get(`/movies/genre/${genre}?limit=${limit}`);
    return response.data;
  }

  async searchMovies(query: string, limit: number = 20): Promise<Movie[]> {
    const response = await this.client.get(`/search/movies?q=${encodeURIComponent(query)}&limit=${limit}`);
    return response.data;
  }
}

export const apiClient = new ApiClient();
export default apiClient;
