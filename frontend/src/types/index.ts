export interface User { id: number; email: string }
export interface Token { access_token: string; token_type: string }
export interface Holding {
  id: number; ticker: string; shares: number; avg_cost: number; currency: string; added_at: string
  current_price?: number; day_change_pct?: number; current_value?: number
  unrealized_gain?: number; unrealized_gain_pct?: number; weight?: number
  company_name?: string; sector?: string
}
export interface WatchlistItem {
  id: number; ticker: string; added_at: string
  current_price?: number; day_change_pct?: number; company_name?: string
}
export interface Quote {
  ticker: string; price?: number; day_change?: number; day_change_pct?: number
  volume?: number; market_cap?: number; company_name?: string; updated_at?: string
}
export interface HistoryPoint { date: string; open: number; high: number; low: number; close: number; volume: number }
export interface Fundamentals {
  ticker: string; company_name?: string; pe_ratio?: number; eps?: number
  dividend_yield?: number; week_52_high?: number; week_52_low?: number
  beta?: number; market_cap?: number; sector?: string; industry?: string
}
export interface MarketStatus { is_open: boolean; session: string; timezone: string }
export interface NewsArticle {
  id: number; ticker: string; headline: string; url?: string; source?: string
  sentiment?: number; image?: string; published_at?: string
}
export interface Alert {
  id: number; ticker: string; alert_type: string; threshold: number
  is_active: boolean; triggered_at?: string; created_at: string
}
export interface PortfolioSummary {
  total_cost_basis: number; total_market_value: number
  total_unrealized_pnl: number; total_return_pct: number; holdings_count: number
}
