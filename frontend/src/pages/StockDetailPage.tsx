import { useParams } from 'react-router-dom'
import { Layout } from '../components/layout/Layout'
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card'
import { PriceChart } from '../components/PriceChart'
import { NewsCard } from '../components/NewsCard'
import { Tooltip } from '../components/ui/Tooltip'
import AISummaryCard from '../components/AISummaryCard'
import { useQuote } from '../hooks/useMarket'
import { useFundamentals } from '../hooks/useMarket'
import { useTickerNews } from '../hooks/useNews'
import { useAISummary } from '../hooks/useAISummary'
import { formatCurrency, formatPercent, formatLargeNumber, getChangeColor } from '../lib/utils'
import { Info } from 'lucide-react'

const METRIC_TOOLTIPS: Record<string, string> = {
  pe_ratio: 'Price-to-Earnings ratio. How much investors pay per $1 of earnings. Lower generally means cheaper. The average S&P 500 P/E is ~22.',
  eps: 'Earnings Per Share — profit the company made per share last year. Higher is better.',
  dividend_yield: 'Annual dividend as % of stock price. Free income just for holding the stock. 0% means the company reinvests profits instead.',
  beta: 'Volatility vs. the market. Beta > 1 = moves more than the market. Beta < 1 = more stable. Negative = moves opposite the market.',
  market_cap: 'Total market value of all shares. Large-cap (>$10B) = established; Small-cap (<$2B) = higher risk/reward.',
  week_52_high: 'Highest price over the last 52 weeks. Useful to see if the stock is near its peak.',
  week_52_low: 'Lowest price over the last 52 weeks. Useful to see if the stock is near a bottom.',
}

export function StockDetailPage() {
  const { ticker } = useParams<{ ticker: string }>()
  const { data: quote } = useQuote(ticker)
  const { data: fundamentals } = useFundamentals(ticker)
  const { data: news = [] } = useTickerNews(ticker, 15)
  const { data: aiSummary, isLoading: aiLoading, error: aiError } = useAISummary(ticker)
  const dayColor = getChangeColor(quote?.day_change_pct)

  return (
    <Layout>
      <div className="mb-6">
        <div className="flex items-baseline gap-4">
          <h1 className="text-3xl font-bold text-gray-100">{ticker}</h1>
          {quote?.company_name && <span className="text-gray-400">{quote.company_name}</span>}
        </div>
        {quote?.price && (
          <div className="flex items-baseline gap-3 mt-2">
            <span className="text-4xl font-bold text-gray-100">{formatCurrency(quote.price)}</span>
            <span className={`text-lg font-medium ${dayColor}`}>{formatPercent(quote.day_change_pct)} today</span>
          </div>
        )}
      </div>

      <div className="grid md:grid-cols-2 gap-6 mb-6">
        <Card>
          <CardHeader><CardTitle>Price History</CardTitle></CardHeader>
          <CardContent><PriceChart ticker={ticker!} /></CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle>Fundamentals</CardTitle></CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 gap-4">
              {fundamentals && Object.entries({
                'P/E Ratio': { value: fundamentals.pe_ratio?.toFixed(2) || '—', key: 'pe_ratio' },
                'EPS': { value: fundamentals.eps ? formatCurrency(fundamentals.eps) : '—', key: 'eps' },
                'Dividend Yield': { value: fundamentals.dividend_yield ? `${(fundamentals.dividend_yield * 100).toFixed(2)}%` : '—', key: 'dividend_yield' },
                'Beta': { value: fundamentals.beta?.toFixed(2) || '—', key: 'beta' },
                '52W High': { value: formatCurrency(fundamentals.week_52_high), key: 'week_52_high' },
                '52W Low': { value: formatCurrency(fundamentals.week_52_low), key: 'week_52_low' },
                'Market Cap': { value: formatLargeNumber(fundamentals.market_cap), key: 'market_cap' },
                'Sector': { value: fundamentals.sector || '—', key: '' },
              }).map(([label, { value, key }]) => (
                <div key={label} className="bg-gray-700/50 rounded-lg p-3">
                  <div className="flex items-center gap-1 text-xs text-gray-500 mb-1">
                    {label}
                    {key && METRIC_TOOLTIPS[key] && (
                      <Tooltip content={METRIC_TOOLTIPS[key]}><Info size={12} className="text-gray-600 hover:text-gray-400 cursor-help"/></Tooltip>
                    )}
                  </div>
                  <div className="font-semibold text-gray-100">{value}</div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader><CardTitle>News</CardTitle></CardHeader>
        <CardContent className="space-y-4">
          <AISummaryCard
            summary={aiSummary ?? null}
            loading={aiLoading}
            error={aiError ? String(aiError) : null}
          />
          {news.length === 0 ? <p className="text-gray-500 text-sm text-center py-8">No news found.</p>
            : <div className="flex flex-col gap-3">{news.map(a => <NewsCard key={a.id} article={a}/>)}</div>
          }
        </CardContent>
      </Card>
    </Layout>
  )
}
