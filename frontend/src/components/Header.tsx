"use client";

import React from 'react';
import Link from 'next/link';
import { Search, User, Film, Heart } from 'lucide-react';

export default function Header() {
  const [searchQuery, setSearchQuery] = React.useState('');

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle search functionality
    console.log('Search query:', searchQuery);
  };

  return (
    <header className="bg-white shadow-sm border-b">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center space-x-2">
            <Film className="w-8 h-8 text-blue-600" />
            <h1 className="text-2xl font-bold text-gray-800">MovieRec</h1>
          </div>

          {/* Search Bar */}
          <form onSubmit={handleSearch} className="flex-1 max-w-md mx-8">
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

          {/* Navigation */}
          <nav className="flex items-center space-x-4">
            <Link
              href="/"
              className="text-gray-600 hover:text-blue-600 transition-colors font-medium"
            >
              Home
            </Link>
            <Link
              href="/movies"
              className="text-gray-600 hover:text-blue-600 transition-colors font-medium"
            >
              Movies
            </Link>
            <Link
              href="/recommendations"
              className="text-gray-600 hover:text-blue-600 transition-colors font-medium"
            >
              For You
            </Link>
            <Link
              href="/favorites"
              className="text-gray-600 hover:text-blue-600 transition-colors font-medium flex items-center space-x-1"
            >
              <Heart className="w-4 h-4" />
              <span>Favorites</span>
            </Link>
            <div className="flex items-center space-x-2 ml-4 pl-4 border-l border-gray-300">
              <User className="w-8 h-8 text-gray-600 p-1 rounded-full border border-gray-300" />
              <span className="text-sm text-gray-600">User #1</span>
            </div>
          </nav>
        </div>
      </div>
    </header>
  );
}
