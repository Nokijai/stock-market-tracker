import { useQuery } from '@tanstack/react-query'
import api from '../lib/api'
import type { NewsArticle } from '../types'

export function useTickerNews(ticker?: string, limit = 10) {
  return useQuery<NewsArticle[]>({ queryKey: ['news', ticker], queryFn: () => api.get(`/news/${ticker}`, { params: { limit } }).then(r => r.data), enabled: !!ticker, staleTime: 1_800_000 })
}
export function useNewsFeed(limit = 20) {
  return useQuery<NewsArticle[]>({ queryKey: ['news-feed'], queryFn: () => api.get('/news/feed', { params: { limit } }).then(r => r.data), staleTime: 1_800_000 })
}
