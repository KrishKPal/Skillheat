// API client using SWR for polling.
import useSWR from 'swr';
import type { GlobeState, NewsArticle, Health } from '@/types/api';

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';

const NEWS_REFRESH_MS = 60_000;
const GLOBE_REFRESH_MS = 90_000;

async function fetcher<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json() as Promise<T>;
}

export function useGlobeState() {
  return useSWR<GlobeState>(`${API_BASE}/globe`, fetcher, {
    refreshInterval: GLOBE_REFRESH_MS,
    revalidateOnFocus: true,
  });
}

export function useNews(countryCode: string | null, limit = 30) {
  const url = countryCode
    ? `${API_BASE}/news?country=${countryCode}&limit=${limit}`
    : `${API_BASE}/news?limit=${limit}`;
  return useSWR<NewsArticle[]>(url, fetcher, {
    refreshInterval: NEWS_REFRESH_MS,
    revalidateOnFocus: true,
    keepPreviousData: true,
  });
}

export function useHealth() {
  return useSWR<Health>(`${API_BASE}/health`, fetcher, {
    refreshInterval: 30_000,
  });
}

export function timeAgo(iso: string): string {
  const seconds = Math.floor((Date.now() - new Date(iso).getTime()) / 1000);
  if (seconds < 60) return `${seconds}s ago`;
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  return `${Math.floor(hours / 24)}d ago`;
}
