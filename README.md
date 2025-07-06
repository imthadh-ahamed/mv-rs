# Movie Recommendation System

A full-stack movie recommendation system built with Next.js frontend and Python FastAPI backend, featuring collaborative filtering, content-based filtering, and hybrid recommendation algorithms.

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