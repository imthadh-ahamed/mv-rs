import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatRating(rating: number): string {
  return rating.toFixed(1);
}

export function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

export function getGenreColor(genre: string): string {
  const colors: Record<string, string> = {
    Action: 'bg-red-500',
    Adventure: 'bg-orange-500',
    Animation: 'bg-purple-500',
    Comedy: 'bg-yellow-500',
    Crime: 'bg-gray-700',
    Documentary: 'bg-blue-500',
    Drama: 'bg-green-600',
    Family: 'bg-pink-500',
    Fantasy: 'bg-violet-500',
    Horror: 'bg-red-700',
    Musical: 'bg-indigo-500',
    Mystery: 'bg-gray-600',
    Romance: 'bg-rose-500',
    'Science Fiction': 'bg-cyan-500',
    Thriller: 'bg-slate-600',
    War: 'bg-amber-700',
    Western: 'bg-orange-700',
  };
  
  return colors[genre] || 'bg-gray-500';
}

export function debounce<T extends (...args: any[]) => void>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}

export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
}

export function getInitials(name: string): string {
  return name
    .split(' ')
    .map((word) => word.charAt(0))
    .join('')
    .toUpperCase()
    .slice(0, 2);
}

export function generatePlaceholderImage(width: number, height: number, text?: string): string {
  const placeholderText = text || `${width}x${height}`;
  return `https://via.placeholder.com/${width}x${height}/374151/ffffff?text=${encodeURIComponent(placeholderText)}`;
}
