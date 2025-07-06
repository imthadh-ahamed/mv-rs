import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { UserState, Rating } from '@/types';

export const useUserStore = create<UserState>()(
  persist(
    (set, get) => ({
      userId: null,
      ratings: [],
      preferences: {
        favoriteGenres: [],
        dislikedGenres: [],
      },
      setUserId: (id: number) => set({ userId: id }),
      addRating: (rating: Rating) => {
        const { ratings } = get();
        const existingIndex = ratings.findIndex(
          (r) => r.user_id === rating.user_id && r.movie_id === rating.movie_id
        );
        
        if (existingIndex >= 0) {
          // Update existing rating
          const newRatings = [...ratings];
          newRatings[existingIndex] = rating;
          set({ ratings: newRatings });
        } else {
          // Add new rating
          set({ ratings: [...ratings, rating] });
        }
      },
      updateRating: (rating: Rating) => {
        const { ratings } = get();
        const updatedRatings = ratings.map((r) =>
          r.user_id === rating.user_id && r.movie_id === rating.movie_id ? rating : r
        );
        set({ ratings: updatedRatings });
      },
      setPreferences: (preferences) => set({ preferences }),
    }),
    {
      name: 'user-storage',
    }
  )
);

export const useRecommendationStore = create<any>()((set) => ({
  recommendations: [],
  loading: false,
  error: null,
  lastUpdated: null,
  modelUsed: null,
  fetchRecommendations: async (userId: number, model?: string) => {
    set({ loading: true, error: null });
    try {
      // This would call the API
      const response = await fetch(`/api/recommendations?user_id=${userId}&model=${model || 'hybrid'}`);
      const data = await response.json();
      
      set({
        recommendations: data.recommendations,
        loading: false,
        lastUpdated: new Date(),
        modelUsed: data.model_used,
      });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to fetch recommendations',
        loading: false,
      });
    }
  },
  clearRecommendations: () => set({ recommendations: [], lastUpdated: null, modelUsed: null }),
}));
