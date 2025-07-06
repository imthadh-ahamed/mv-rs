# Movie Recommendation System

A full-stack movie recommendation system built with Next.js frontend and Python FastAPI backend, featuring collaborative filtering, content-based filtering, and hybrid recommendation algorithms.

## 🏗️ Project Structure

```
mv-rs/
├── backend/                    # Python FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI application entry point
│   │   ├── config.py          # Configuration and environment variables
│   │   ├── database.py        # MongoDB connection and operations
│   │   ├── models/            # Pydantic models and ML models
│   │   ├── routers/           # API route handlers
│   │   ├── services/          # Business logic and ML services
│   │   └── utils/             # Utility functions
│   ├── ml_models/             # Saved ML models
│   ├── requirements.txt
│   └── .env                   # Backend environment variables
├── frontend/                  # Next.js frontend
│   ├── src/
│   │   ├── app/               # App router (Next.js 13+)
│   │   ├── components/        # Reusable UI components
│   │   ├── lib/               # Utilities and configurations
│   │   ├── hooks/             # Custom React hooks
│   │   └── types/             # TypeScript type definitions
│   ├── public/                # Static assets
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   └── .env.local             # Frontend environment variables
├── ml/                        # Machine learning development
│   └── mv-rs.ipynb           # Jupyter notebook for model development
└── docker-compose.yml        # Docker setup for full stack
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose (recommended)
- OR Python 3.11+, Node.js 18+, and MongoDB

### Option 1: Docker Setup (Recommended)
1. Clone the repository
2. Navigate to the project directory: `cd mv-rs`
3. Copy environment files:
   ```bash
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env.local
   ```
4. Start all services: `docker-compose up --build`
5. Access the application:
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`

### Option 2: Manual Setup

#### Backend Setup
1. Navigate to backend directory: `cd backend`
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment: 
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and configure your environment variables
6. Start MongoDB (locally or use MongoDB Atlas)
7. Run the server: `uvicorn app.main:app --reload`

#### Frontend Setup
1. Navigate to frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Copy `.env.example` to `.env.local` and configure your environment variables
4. Run the development server: `npm run dev`

### Loading Sample Data
The Docker setup automatically loads sample data. For manual setup:
1. Start MongoDB
2. Run the initialization script: `mongosh < init-mongo.js`

## 🔧 Environment Variables

### Backend (.env)
```bash
# Database
MONGODB_URL=mongodb://admin:password123@localhost:27017/movie_recommendation_db?authSource=admin
DATABASE_NAME=movie_recommendation_db

# Security
SECRET_KEY=your-very-secure-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:3001"]

# Environment
ENVIRONMENT=development
DEBUG=true

# ML Models
MODELS_PATH=ml_models
```

### Frontend (.env.local)
```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# NextAuth.js configuration (for future authentication)
NEXTAUTH_SECRET=your-nextauth-secret-key-here
NEXTAUTH_URL=http://localhost:3000

# Optional: External APIs
TMDB_API_KEY=your-tmdb-api-key-here
```

## 🗄️ Database Setup

The application uses MongoDB to store:
- **Movies**: Movie information with genres, ratings, and metadata
- **Users**: User profiles and demographics
- **Ratings**: User ratings for movies
- **Recommendations**: Cached recommendation results

Sample data is automatically loaded when using Docker. The database includes:
- 5 sample movies (Shawshank Redemption, Dark Knight, etc.)
- 5 sample users with different demographics
- Sample ratings to demonstrate the recommendation system

## 🤖 ML Models

The system includes multiple recommendation algorithms:

### 1. **Popularity-based Recommender**
- Baseline recommender using movie popularity
- Great for new users (cold start problem)
- Based on average ratings and rating counts

### 2. **Collaborative Filtering**
- **User-based**: Find similar users and recommend movies they liked
- **Item-based**: Find similar movies based on user rating patterns
- Uses cosine similarity and Pearson correlation

### 3. **Matrix Factorization (SVD)**
- Advanced collaborative filtering using Singular Value Decomposition
- Handles sparse data better than traditional CF
- Predicts ratings for user-movie pairs

### 4. **Content-based Filtering**
- Recommends movies based on genre preferences
- Analyzes user's rating history to learn preferences
- Good for users with consistent genre preferences

### 5. **Hybrid Model**
- Combines multiple algorithms for better accuracy
- Weighted combination of collaborative and content-based filtering
- Provides the most accurate recommendations

### Model Training
All models are trained on the MovieLens 100K dataset and can be retrained with new data. The Jupyter notebook (`ml/mv-rs.ipynb`) contains the complete ML pipeline for data processing, model training, and evaluation.

## 🎯 API Endpoints

### Movies
- `GET /movies/` - Get movies with filtering and pagination
- `GET /movies/{movie_id}` - Get specific movie
- `GET /movies/popular/` - Get popular movies
- `GET /movies/genre/{genre}` - Get movies by genre
- `GET /movies/search/?q={query}` - Search movies

### Recommendations
- `GET /recommendations/?user_id={id}&model={type}` - Get recommendations
- `POST /recommendations/predict-rating` - Predict user rating for movie
- `GET /recommendations/similar/{movie_id}` - Get similar movies

### Ratings
- `POST /ratings/` - Create/update rating
- `GET /ratings/user/{user_id}` - Get user ratings
- `GET /ratings/movie/{movie_id}` - Get movie ratings

### Users
- `GET /users/` - Get users with pagination
- `GET /users/{user_id}` - Get specific user
- `GET /users/{user_id}/stats` - Get user statistics

## 🚀 Features

### Frontend Features
- **Modern UI**: Clean, responsive design with Tailwind CSS
- **Movie Discovery**: Browse, search, and filter movies
- **Personalized Recommendations**: Get recommendations based on your ratings
- **Rating System**: Rate movies from 1-5 stars
- **User Profiles**: Switch between different user profiles
- **Real-time Updates**: Instant feedback when rating movies

### Backend Features
- **RESTful API**: Well-documented FastAPI with automatic OpenAPI docs
- **Multiple ML Models**: Choose from different recommendation algorithms
- **Database Integration**: MongoDB for scalable data storage
- **Error Handling**: Comprehensive error handling and logging
- **CORS Support**: Cross-origin requests enabled for frontend
- **Health Checks**: Built-in health monitoring endpoints

### Infrastructure Features
- **Docker Support**: Complete Docker setup with docker-compose
- **Environment Management**: Secure environment variable handling
- **Database Initialization**: Automatic sample data loading
- **Logging**: Comprehensive logging for debugging and monitoring