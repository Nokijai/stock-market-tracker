import { usePortfolio, usePortfolioSummary } from '../hooks/usePortfolio'
import { useNewsFeed } from '../hooks/useNews'
import { Layout } from '../components/layout/Layout'
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card'
import { PortfolioPieChart } from '../components/PortfolioPieChart'
import { NewsCard } from '../components/NewsCard'
import { MarketStatusBadge } from '../components/MarketStatusBadge'
import { formatCurrency, formatPercent, getChangeColor } from '../lib/utils'
import { TrendingUp, TrendingDown, Plus } from 'lucide-react'
import { Link } from 'react-router-dom'
import { Button } from '../components/ui/Button'

export function DashboardPage() {
  const { data: holdings = [] } = usePortfolio()
  const { data: summary } = usePortfolioSummary()
  const { data: news = [] } = useNewsFeed(5)

  const sortedByDay = [...holdings].sort((a, b) => (b.day_change_pct || 0) - (a.day_change_pct || 0))
  const topGainers = sortedByDay.slice(0, 3).filter(h => (h.day_change_pct || 0) > 0)
  const topLosers = sortedByDay.slice(-3).reverse().filter(h => (h.day_change_pct || 0) < 0)

  return (
    <Layout>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-100">Dashboard</h1>
        <MarketStatusBadge />
      </div>

      {/* Summary Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <Card className="col-span-2">
          <CardContent>
            <p className="text-sm text-gray-500 mb-1">Total Portfolio Value</p>
            <p className="text-3xl font-bold text-gray-100">{summary ? formatCurrency(summary.total_market_value) : '—'}</p>
            {summary && (
              <p className={`text-sm font-medium mt-1 ${getChangeColor(summary.total_return_pct)}`}>
                {formatCurrency(summary.total_unrealized_pnl)} ({formatPercent(summary.total_return_pct)}) all time
              </p>
            )}
          </CardContent>
        </Card>
        <Card>
          <CardContent>
            <p className="text-sm text-gray-500 mb-1">Holdings</p>
            <p className="text-2xl font-bold text-gray-100">{summary?.holdings_count ?? '—'}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent>
            <p className="text-sm text-gray-500 mb-1">Cost Basis</p>
            <p className="text-2xl font-bold text-gray-100">{summary ? formatCurrency(summary.total_cost_basis) : '—'}</p>
          </CardContent>
        </Card>
      </div>

      {holdings.length === 0 ? (
        <Card className="text-center py-16">
          <p className="text-gray-500 mb-4">You haven't added any holdings yet.</p>
          <Link to="/portfolio"><Button><Plus size={16} className="mr-2"/>Add Your First Holding</Button></Link>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <Card>
            <CardHeader><CardTitle>Allocation</CardTitle></CardHeader>
            <CardContent><PortfolioPieChart holdings={holdings} /></CardContent>
          </Card>
          <Card>
            <CardHeader><CardTitle>Today's Movers</CardTitle></CardHeader>
            <CardContent>
              {topGainers.length > 0 && (
                <div className="mb-4">
                  <p className="text-xs text-gray-500 uppercase tracking-wide mb-2">Top Gainers</p>
                  {topGainers.map(h => (
                    <div key={h.id} className="flex justify-between items-center py-2 border-b border-gray-700/50">
                      <div><Link to={`/stock/${h.ticker}`} className="font-medium text-gray-100 hover:text-blue-400">{h.ticker}</Link><p className="text-xs text-gray-500">{h.company_name}</p></div>
                      <div className="text-right"><p className="font-medium text-gray-100">{formatCurrency(h.current_price)}</p><p className="text-sm text-green-400 flex items-center justify-end gap-1"><TrendingUp size={12}/>{formatPercent(h.day_change_pct)}</p></div>
                    </div>
                  ))}
                </div>
              )}
              {topLosers.length > 0 && (
                <div>
                  <p className="text-xs text-gray-500 uppercase tracking-wide mb-2">Top Losers</p>
                  {topLosers.map(h => (
                    <div key={h.id} className="flex justify-between items-center py-2 border-b border-gray-700/50">
                      <div><Link to={`/stock/${h.ticker}`} className="font-medium text-gray-100 hover:text-blue-400">{h.ticker}</Link><p className="text-xs text-gray-500">{h.company_name}</p></div>
                      <div className="text-right"><p className="font-medium text-gray-100">{formatCurrency(h.current_price)}</p><p className="text-sm text-red-400 flex items-center justify-end gap-1"><TrendingDown size={12}/>{formatPercent(h.day_change_pct)}</p></div>
                    </div>
                  ))}
                </div>
              )}
              {topGainers.length === 0 && topLosers.length === 0 && <p className="text-gray-500 text-sm text-center py-4">No price data yet</p>}
            </CardContent>
          </Card>
        </div>
      )}

      {news.length > 0 && (
        <Card>
          <CardHeader><CardTitle>Latest News</CardTitle></CardHeader>
          <CardContent>
            <div className="flex flex-col gap-3">{news.slice(0, 5).map(a => <NewsCard key={a.id} article={a}/>)}</div>
          </CardContent>
        </Card>
      )}
    </Layout>
  )
}
