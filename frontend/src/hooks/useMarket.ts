import { useQuery } from '@tanstack/react-query'
import api from '../lib/api'
import type { Quote, HistoryPoint, MarketStatus, Fundamentals } from '../types'

export function useQuote(ticker?: string) {
  return useQuery<Quote>({ queryKey: ['quote', ticker], queryFn: () => api.get(`/market/quote/${ticker}`).then(r => r.data), enabled: !!ticker, refetchInterval: 60_000 })
}
export function useHistory(ticker?: string, period = '1mo') {
  return useQuery<HistoryPoint[]>({ queryKey: ['history', ticker, period], queryFn: () => api.get(`/market/history/${ticker}`, { params: { period } }).then(r => r.data), enabled: !!ticker })
}
export function useMarketStatus() {
  return useQuery<MarketStatus>({ queryKey: ['market-status'], queryFn: () => api.get('/market/status').then(r => r.data), refetchInterval: 60_000 })
}
export function useFundamentals(ticker?: string) {
  return useQuery<Fundamentals>({ queryKey: ['fundamentals', ticker], queryFn: () => api.get(`/market/fundamentals/${ticker}`).then(r => r.data), enabled: !!ticker, staleTime: 86_400_000 })
}
