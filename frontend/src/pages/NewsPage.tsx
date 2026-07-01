import { useState } from 'react'
import { usePortfolio } from '../hooks/usePortfolio'
import { useTickerNews, useNewsFeed } from '../hooks/useNews'
import { Layout } from '../components/layout/Layout'
import { NewsCard } from '../components/NewsCard'
import { Card } from '../components/ui/Card'

function TickerFeed({ ticker }: { ticker: string }) {
  const { data: articles = [], isLoading } = useTickerNews(ticker, 15)
  if (isLoading) return <div className="animate-pulse space-y-3">{[1,2,3].map(i => <div key={i} className="h-20 bg-gray-800 rounded-xl"/>)}</div>
  if (!articles.length) return <p className="text-gray-500 text-sm text-center py-8">No news found for {ticker}</p>
  return <div className="flex flex-col gap-3">{articles.map(a => <NewsCard key={a.id} article={a}/>)}</div>
}

function AllFeed() {
  const { data: articles = [], isLoading } = useNewsFeed(30)
  if (isLoading) return <div className="animate-pulse space-y-3">{[1,2,3].map(i => <div key={i} className="h-20 bg-gray-800 rounded-xl"/>)}</div>
  if (!articles.length) return <p className="text-gray-500 text-sm text-center py-8">No news yet. Add holdings to see their news.</p>
  return <div className="flex flex-col gap-3">{articles.map(a => <NewsCard key={a.id} article={a}/>)}</div>
}

export function NewsPage() {
  const { data: holdings = [] } = usePortfolio()
  const [active, setActive] = useState('all')
  const tickers = holdings.map(h => h.ticker)

  return (
    <Layout>
      <h1 className="text-2xl font-bold text-gray-100 mb-6">News</h1>
      <div className="flex gap-2 mb-6 overflow-x-auto pb-1">
        {['all', ...tickers].map(t => (
          <button key={t} onClick={() => setActive(t)}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium whitespace-nowrap transition-colors ${active === t ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-400 hover:text-gray-200'}`}>
            {t === 'all' ? 'All Holdings' : t}
          </button>
        ))}
      </div>
      <Card>{active === 'all' ? <AllFeed/> : <TickerFeed ticker={active}/>}</Card>
    </Layout>
  )
}
