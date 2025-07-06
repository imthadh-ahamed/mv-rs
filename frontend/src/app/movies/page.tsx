"use client";

import React, { useState, useEffect } from 'react';
import MovieCard from '@/components/MovieCard';
import { Film, Search, Filter, Grid, List } from 'lucide-react';

interface Movie {
  id: number;
  title: string;
  genre: string;
  release_date?: string;
  overview?: string;
  vote_average?: number;
  vote_count?: number;
  poster_path?: string;
}

interface MoviesResponse {
  movies: Movie[];
  total?: number;
  page?: number;
  total_pages?: number;
}

export default function MoviesPage() {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedGenre, setSelectedGenre] = useState<string>('');
  const [sortBy, setSortBy] = useState<string>('title');
  const [sortOrder, setSortOrder] = useState<string>('asc');
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  const genres = [
    'Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary',
    'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Mystery',
    'Romance', 'Science Fiction', 'TV Movie', 'Thriller', 'War', 'Western'
  ];

  // Mock data for demonstration
  const mockMovies: Movie[] = [
    {
      id: 1,
      title: "The Shawshank Redemption",
      genre: "Drama",
      release_date: "1994-09-23",
      overview: "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
      vote_average: 9.3,
      vote_count: 2500000,
      poster_path: "/path-to-poster.jpg"
    },
    {
      id: 2,
      title: "The Dark Knight",
      genre: "Action",
      release_date: "2008-07-18",
      overview: "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological tests.",
      vote_average: 9.0,
      vote_count: 2300000,
      poster_path: "/path-to-poster.jpg"
    },
    {
      id: 3,
      title: "Pulp Fiction",
      genre: "Crime",
      release_date: "1994-10-14",
      overview: "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence.",
      vote_average: 8.9,
      vote_count: 2100000,
      poster_path: "/path-to-poster.jpg"
    },
    {
      id: 4,
      title: "Forrest Gump",
      genre: "Drama",
      release_date: "1994-07-06",
      overview: "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal unfold from an Alabama man's perspective.",
      vote_average: 8.8,
      vote_count: 2000000,
      poster_path: "/path-to-poster.jpg"
    },
    {
      id: 5,
      title: "The Matrix",
      genre: "Science Fiction",
      release_date: "1999-03-31",
      overview: "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
      vote_average: 8.7,
      vote_count: 2400000,
      poster_path: "/path-to-poster.jpg"
    },
    {
      id: 6,
      title: "Goodfellas",
      genre: "Crime",
      release_date: "1990-09-21",
      overview: "The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen Hill and his mob partners.",
      vote_average: 8.7,
      vote_count: 1200000,
      poster_path: "/path-to-poster.jpg"
    },
    {
      id: 7,
      title: "The Lord of the Rings: The Fellowship of the Ring",
      genre: "Fantasy",
      release_date: "2001-12-19",
      overview: "A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring.",
      vote_average: 8.8,
      vote_count: 1800000,
      poster_path: "/path-to-poster.jpg"
    },
    {
      id: 8,
      title: "Star Wars: Episode V - The Empire Strikes Back",
      genre: "Science Fiction",
      release_date: "1980-05-21",
      overview: "The Rebels scatter after the Empire's attack on their base. Luke Skywalker begins training with Yoda.",
      vote_average: 8.7,
      vote_count: 1500000,
      poster_path: "/path-to-poster.jpg"
    }
  ];

  const fetchMovies = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';
      const params = new URLSearchParams({
        skip: ((currentPage - 1) * 20).toString(),
        limit: '20',
        sort_by: sortBy,
        sort_order: sortOrder,
        ...(searchQuery && { search: searchQuery }),
        ...(selectedGenre && { genre: selectedGenre })
      });
      
      const response = await fetch(`${apiUrl}/movies?${params}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data: Movie[] = await response.json();
      setMovies(data || []);
      // Since the API returns a simple array, we'll calculate pagination based on returned length
      setTotalPages(data.length === 20 ? currentPage + 1 : currentPage);
    } catch (err) {
      console.warn('API not available, using mock data:', err);
      // Use mock data as fallback
      let filteredMovies = [...mockMovies];
      
      // Apply search filter
      if (searchQuery) {
        filteredMovies = filteredMovies.filter(movie => 
          movie.title.toLowerCase().includes(searchQuery.toLowerCase())
        );
      }
      
      // Apply genre filter
      if (selectedGenre) {
        filteredMovies = filteredMovies.filter(movie => 
          movie.genre.toLowerCase().includes(selectedGenre.toLowerCase())
        );
      }
      
      // Apply sorting
      filteredMovies.sort((a, b) => {
        let aValue: any = a[sortBy as keyof Movie];
        let bValue: any = b[sortBy as keyof Movie];
        
        // Handle undefined values
        if (aValue === undefined) aValue = '';
        if (bValue === undefined) bValue = '';
        
        if (typeof aValue === 'string') aValue = aValue.toLowerCase();
        if (typeof bValue === 'string') bValue = bValue.toLowerCase();
        
        if (sortOrder === 'asc') {
          return aValue > bValue ? 1 : -1;
        } else {
          return aValue < bValue ? 1 : -1;
        }
      });
      
      setMovies(filteredMovies);
      setTotalPages(1);
      setError('Using demo data - API not available');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMovies();
  }, [currentPage, sortBy, sortOrder, searchQuery, selectedGenre]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setCurrentPage(1);
    fetchMovies();
  };

  const handleGenreChange = (genre: string) => {
    setSelectedGenre(genre === selectedGenre ? '' : genre);
    setCurrentPage(1);
  };

  const handleSortChange = (newSortBy: string) => {
    if (newSortBy === sortBy) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(newSortBy);
      setSortOrder('asc');
    }
    setCurrentPage(1);
  };

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <Film className="h-8 w-8 text-blue-600 mr-3" />
              <h1 className="text-2xl font-bold text-gray-900">Browse Movies</h1>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setViewMode(viewMode === 'grid' ? 'list' : 'grid')}
                className="flex items-center space-x-1 px-3 py-2 border border-gray-300 rounded-md text-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {viewMode === 'grid' ? <List className="h-4 w-4" /> : <Grid className="h-4 w-4" />}
                <span>{viewMode === 'grid' ? 'List' : 'Grid'}</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Filters and Search */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
            {/* Search */}
            <form onSubmit={handleSearch} className="flex-1 max-w-md">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="text"
                  placeholder="Search movies..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg text-gray-900 bg-white placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
            </form>

            {/* Sort Options */}
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <Filter className="h-5 w-5 text-gray-500" />
                <span className="text-sm font-medium text-gray-700">Sort by:</span>
                <select
                  value={sortBy}
                  onChange={(e) => handleSortChange(e.target.value)}
                  aria-label="Sort movies by"
                  className="px-3 py-1 border border-gray-300 rounded-md text-sm text-gray-900 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="title">Title</option>
                  <option value="release_date">Release Date</option>
                  <option value="vote_average">Rating</option>
                  <option value="vote_count">Popularity</option>
                </select>
                <button
                  onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
                  className="px-2 py-1 text-sm text-gray-600 hover:text-gray-900"
                >
                  {sortOrder === 'asc' ? '↑' : '↓'}
                </button>
              </div>
            </div>
          </div>

          {/* Genre Filter */}
          <div className="mt-4">
            <div className="flex flex-wrap gap-2">
              <button
                onClick={() => handleGenreChange('')}
                className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                  selectedGenre === '' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                All Genres
              </button>
              {genres.map((genre) => (
                <button
                  key={genre}
                  onClick={() => handleGenreChange(genre)}
                  className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                    selectedGenre === genre 
                      ? 'bg-blue-600 text-white' 
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  {genre}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Loading State */}
        {loading && (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Error Loading Movies</h3>
                <p className="text-sm text-red-700 mt-1">{error}</p>
                <button
                  onClick={fetchMovies}
                  className="mt-2 text-sm font-medium text-red-800 hover:text-red-600"
                >
                  Try Again
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Movies Grid/List */}
        {!loading && !error && movies.length > 0 && (
          <>
            <div className={viewMode === 'grid' 
              ? 'grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6' 
              : 'space-y-4'
            }>
              {movies.map((movie) => (
                <MovieCard key={movie.id} movie={movie} />
              ))}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="mt-8 flex justify-center">
                <nav className="flex items-center space-x-2">
                  <button
                    onClick={() => handlePageChange(currentPage - 1)}
                    disabled={currentPage === 1}
                    className="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Previous
                  </button>
                  
                  {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                    const page = Math.max(1, Math.min(totalPages - 4, currentPage - 2)) + i;
                    return (
                      <button
                        key={page}
                        onClick={() => handlePageChange(page)}
                        className={`px-3 py-2 text-sm font-medium rounded-md ${
                          currentPage === page
                            ? 'bg-blue-600 text-white'
                            : 'text-gray-700 bg-white border border-gray-300 hover:bg-gray-50'
                        }`}
                      >
                        {page}
                      </button>
                    );
                  })}
                  
                  <button
                    onClick={() => handlePageChange(currentPage + 1)}
                    disabled={currentPage === totalPages}
                    className="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Next
                  </button>
                </nav>
              </div>
            )}
          </>
        )}

        {/* Empty State */}
        {!loading && !error && movies.length === 0 && (
          <div className="text-center py-12">
            <Film className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">No movies found</h3>
            <p className="mt-1 text-sm text-gray-500">
              Try adjusting your search or filter criteria.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
