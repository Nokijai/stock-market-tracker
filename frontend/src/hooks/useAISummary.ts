import { useQuery } from '@tanstack/react-query'
import api from '../lib/api'

interface AISummary {
  ticker: string
  bullets: string[]
  sentiment: 'Bullish' | 'Neutral' | 'Bearish'
  reason: string
}

export function useAISummary(ticker: string | undefined) {
  return useQuery<AISummary>({
    queryKey: ['ai-summary', ticker],
    queryFn: () => api.get(`/news/${ticker}/summary`).then(r => r.data),
    enabled: !!ticker,
    staleTime: 1000 * 60 * 30,  // 30 min — matches backend Redis TTL
    retry: false,                // don't retry 503 (AI unavailable)
  })
}
