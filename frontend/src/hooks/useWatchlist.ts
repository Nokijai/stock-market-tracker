import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from '../lib/api'
import type { WatchlistItem } from '../types'

export function useWatchlist() {
  return useQuery<WatchlistItem[]>({ queryKey: ['watchlist'], queryFn: () => api.get('/watchlist/').then(r => r.data) })
}
export function useAddToWatchlist() {
  const qc = useQueryClient()
  return useMutation({ mutationFn: (ticker: string) => api.post('/watchlist/', { ticker }).then(r => r.data), onSuccess: () => qc.invalidateQueries({ queryKey: ['watchlist'] }) })
}
export function useRemoveFromWatchlist() {
  const qc = useQueryClient()
  return useMutation({ mutationFn: (ticker: string) => api.delete(`/watchlist/${ticker}`), onSuccess: () => qc.invalidateQueries({ queryKey: ['watchlist'] }) })
}
