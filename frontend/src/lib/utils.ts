import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) { return twMerge(clsx(inputs)) }

export function formatCurrency(value?: number, currency = 'USD'): string {
  if (value === undefined || value === null) return '—'
  return new Intl.NumberFormat('en-US', { style: 'currency', currency }).format(value)
}

export function formatPercent(value?: number): string {
  if (value === undefined || value === null) return '—'
  const sign = value >= 0 ? '+' : ''
  return `${sign}${value.toFixed(2)}%`
}

export function formatLargeNumber(value?: number): string {
  if (value === undefined || value === null) return '—'
  if (value >= 1e12) return `$${(value / 1e12).toFixed(2)}T`
  if (value >= 1e9) return `$${(value / 1e9).toFixed(2)}B`
  if (value >= 1e6) return `$${(value / 1e6).toFixed(2)}M`
  return formatCurrency(value)
}

export function getChangeColor(pct?: number): string {
  if (pct === undefined || pct === null) return 'text-gray-400'
  return pct >= 0 ? 'text-green-400' : 'text-red-400'
}

export function formatDate(dateStr?: string): string {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

export function timeAgo(dateStr?: string): string {
  if (!dateStr) return '—'
  const diff = (Date.now() - new Date(dateStr).getTime()) / 1000
  if (diff < 60) return `${Math.floor(diff)}s ago`
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`
  return `${Math.floor(diff / 86400)}d ago`
}

export function getSentimentLabel(score?: number): { label: string; color: string } {
  if (score === undefined || score === null) return { label: 'Neutral', color: 'text-gray-400' }
  if (score > 0.1) return { label: 'Bullish', color: 'text-green-400' }
  if (score < -0.1) return { label: 'Bearish', color: 'text-red-400' }
  return { label: 'Neutral', color: 'text-gray-400' }
}
