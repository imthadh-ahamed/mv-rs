// Initialize MongoDB with sample data
db = db.getSiblingDB('movie_recommendation_db');

// Create collections
db.createCollection('movies');
db.createCollection('users');
db.createCollection('ratings');
db.createCollection('recommendations');

// Insert sample movies
db.movies.insertMany([
  {
    movie_id: 1,
    title: "The Shawshank Redemption",
    genre: "Drama",
    release_date: "1994-09-23",
    overview: "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
    vote_average: 9.3,
    vote_count: 2500000,
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    movie_id: 2,
    title: "The Dark Knight",
    genre: "Action",
    release_date: "2008-07-18",
    overview: "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
    vote_average: 9.0,
    vote_count: 2300000,
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    movie_id: 3,
    title: "Pulp Fiction",
    genre: "Crime",
    release_date: "1994-10-14",
    overview: "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
    vote_average: 8.9,
    vote_count: 2100000,
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    movie_id: 4,
    title: "Forrest Gump",
    genre: "Drama",
    release_date: "1994-07-06",
    overview: "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an IQ of 75.",
    vote_average: 8.8,
    vote_count: 2000000,
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    movie_id: 5,
    title: "The Matrix",
    genre: "Science Fiction",
    release_date: "1999-03-31",
    overview: "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
    vote_average: 8.7,
    vote_count: 1800000,
    created_at: new Date(),
    updated_at: new Date()
  }
]);

// Insert sample users
db.users.insertMany([
  {
    user_id: 1,
    age: 24,
    gender: "M",
    occupation: "technician",
    zip_code: "85711",
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    user_id: 2,
    age: 53,
    gender: "F",
    occupation: "other",
    zip_code: "94043",
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    user_id: 3,
    age: 23,
    gender: "M",
    occupation: "writer",
    zip_code: "32067",
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    user_id: 4,
    gender: "M",
    occupation: "technician",
    zip_code: "43537",
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    user_id: 5,
    age: 33,
    gender: "F",
    occupation: "other",
    zip_code: "15213",
    created_at: new Date(),
    updated_at: new Date()
  }
]);

// Insert sample ratings
db.ratings.insertMany([
  {
    user_id: 1,
    movie_id: 1,
    rating: 5.0,
    timestamp: 874965758,
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    user_id: 1,
    movie_id: 2,
    rating: 4.0,
    timestamp: 874965759,
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    user_id: 2,
    movie_id: 1,
    rating: 4.0,
    timestamp: 874965760,
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    user_id: 2,
    movie_id: 3,
    rating: 5.0,
    timestamp: 874965761,
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    user_id: 3,
    movie_id: 1,
    rating: 5.0,
    timestamp: 874965762,
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    user_id: 3,
    movie_id: 4,
    rating: 3.0,
    timestamp: 874965763,
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    user_id: 4,
    movie_id: 2,
    rating: 4.0,
    timestamp: 874965764,
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    user_id: 5,
    movie_id: 5,
    rating: 5.0,
    timestamp: 874965765,
    created_at: new Date(),
    updated_at: new Date()
  }
]);

// Create indexes
db.movies.createIndex({ movie_id: 1 }, { unique: true });
db.movies.createIndex({ title: 1 });
db.movies.createIndex({ genre: 1 });

db.users.createIndex({ user_id: 1 }, { unique: true });

db.ratings.createIndex({ user_id: 1, movie_id: 1 }, { unique: true });
db.ratings.createIndex({ user_id: 1 });
db.ratings.createIndex({ movie_id: 1 });

db.recommendations.createIndex({ user_id: 1, model_type: 1 });
db.recommendations.createIndex({ user_id: 1 });
db.recommendations.createIndex({ created_at: 1 });

print("Database initialized with sample data and indexes!");
