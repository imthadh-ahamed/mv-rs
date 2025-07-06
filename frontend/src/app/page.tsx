"use client";

import React from 'react';
import Link from 'next/link';
import MovieCard from '@/components/MovieCard';
import { Film, TrendingUp, Star, Users } from 'lucide-react';

// Mock data for demonstration
const mockMovies = [
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
    overview: "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
    vote_average: 9.0,
    vote_count: 2300000,
    poster_path: "/path-to-poster.jpg"
  },
  {
    id: 3,
    title: "Pulp Fiction",
    genre: "Crime",
    release_date: "1994-10-14",
    overview: "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
    vote_average: 8.9,
    vote_count: 2100000,
    poster_path: "/path-to-poster.jpg"
  },
  {
    id: 4,
    title: "Forrest Gump",
    genre: "Drama",
    release_date: "1994-07-06",
    overview: "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an IQ of 75.",
    vote_average: 8.8,
    vote_count: 2000000,
    poster_path: "/path-to-poster.jpg"
  }
];

export default function HomePage() {
  const [selectedUser, setSelectedUser] = React.useState(1);

  const handleRateMovie = (movieId: number, rating: number) => {
    console.log(`Movie ${movieId} rated ${rating} stars`);
    // Here you would typically send the rating to your API
  };

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg p-8">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-4xl font-bold mb-4">
            Discover Your Next Favorite Movie
          </h1>
          <p className="text-xl mb-6">
            Get personalized recommendations powered by advanced machine learning algorithms
          </p>
          <div className="flex justify-center space-x-4">
            <Link href="/recommendations" className="bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
              Get Recommendations
            </Link>
            <Link href="/movies" className="border border-white text-white px-6 py-3 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors">
              Browse Movies
            </Link>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-md text-center">
          <Film className="w-12 h-12 text-blue-600 mx-auto mb-2" />
          <h3 className="text-2xl font-bold text-gray-800">1,682</h3>
          <p className="text-gray-600">Movies Available</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md text-center">
          <Users className="w-12 h-12 text-green-600 mx-auto mb-2" />
          <h3 className="text-2xl font-bold text-gray-800">943</h3>
          <p className="text-gray-600">Active Users</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md text-center">
          <Star className="w-12 h-12 text-yellow-600 mx-auto mb-2" />
          <h3 className="text-2xl font-bold text-gray-800">100K+</h3>
          <p className="text-gray-600">Ratings Given</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md text-center">
          <TrendingUp className="w-12 h-12 text-purple-600 mx-auto mb-2" />
          <h3 className="text-2xl font-bold text-gray-800">95%</h3>
          <p className="text-gray-600">Accuracy Rate</p>
        </div>
      </section>

      {/* User Selection */}
      <section className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Select User Profile</h2>
        <div className="flex flex-wrap gap-2">
          {[1, 2, 3, 4, 5].map((userId) => (
            <button
              key={userId}
              onClick={() => setSelectedUser(userId)}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                selectedUser === userId
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              User #{userId}
            </button>
          ))}
        </div>
        <p className="text-sm text-gray-600 mt-2">
          Selected: User #{selectedUser} - This will be used for generating personalized recommendations
        </p>
      </section>

      {/* Popular Movies */}
      <section>
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Popular Movies</h2>
        <div className="movie-grid">
          {mockMovies.map((movie) => (
            <MovieCard
              key={movie.id}
              movie={movie}
              onRate={(rating) => handleRateMovie(movie.id, rating)}
              showRating={true}
            />
          ))}
        </div>
      </section>

      {/* How It Works */}
      <section className="bg-white p-8 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">How It Works</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl font-bold text-blue-600">1</span>
            </div>
            <h3 className="text-lg font-semibold mb-2">Rate Movies</h3>
            <p className="text-gray-600">Rate movies you've watched to help us understand your preferences</p>
          </div>
          <div className="text-center">
            <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl font-bold text-green-600">2</span>
            </div>
            <h3 className="text-lg font-semibold mb-2">Get Recommendations</h3>
            <p className="text-gray-600">Our AI analyzes your ratings and finds movies you'll love</p>
          </div>
          <div className="text-center">
            <div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl font-bold text-purple-600">3</span>
            </div>
            <h3 className="text-lg font-semibold mb-2">Discover & Enjoy</h3>
            <p className="text-gray-600">Watch recommended movies and discover new favorites</p>
          </div>
        </div>
      </section>
    </div>
  );
}
