import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from '../lib/api'
import type { Holding, PortfolioSummary } from '../types'

export function usePortfolio() {
  return useQuery<Holding[]>({ queryKey: ['portfolio'], queryFn: () => api.get('/portfolio/').then(r => r.data), refetchInterval: 60_000 })
}
export function usePortfolioSummary() {
  return useQuery<PortfolioSummary>({ queryKey: ['portfolio-summary'], queryFn: () => api.get('/portfolio/summary').then(r => r.data), refetchInterval: 60_000 })
}
export function useAddHolding() {
  const qc = useQueryClient()
  return useMutation({ mutationFn: (data: { ticker: string; shares: number; avg_cost: number }) => api.post('/portfolio/', data).then(r => r.data), onSuccess: () => qc.invalidateQueries({ queryKey: ['portfolio'] }) })
}
export function useDeleteHolding() {
  const qc = useQueryClient()
  return useMutation({ mutationFn: (id: number) => api.delete(`/portfolio/${id}`), onSuccess: () => qc.invalidateQueries({ queryKey: ['portfolio'] }) })
}
export function useUpdateHolding() {
  const qc = useQueryClient()
  return useMutation({ mutationFn: ({ id, ...data }: { id: number; shares?: number; avg_cost?: number }) => api.put(`/portfolio/${id}`, data).then(r => r.data), onSuccess: () => qc.invalidateQueries({ queryKey: ['portfolio'] }) })
}
