import type { NewsArticle } from '../types'
import { getSentimentLabel, timeAgo } from '../lib/utils'
import { ExternalLink } from 'lucide-react'

export function NewsCard({ article }: { article: NewsArticle }) {
  const { label, color } = getSentimentLabel(article.sentiment)
  return (
    <div className="bg-gray-800 border border-gray-700 rounded-xl p-4 hover:border-gray-600 transition-colors">
      <div className="flex justify-between items-start gap-3 mb-2">
        <a href={article.url || '#'} target="_blank" rel="noopener noreferrer" className="text-gray-100 font-medium text-sm leading-snug hover:text-blue-400 transition-colors line-clamp-2">
          {article.headline}
          {article.url && <ExternalLink size={12} className="inline ml-1 mb-0.5 text-gray-500"/>}
        </a>
        {article.sentiment !== null && article.sentiment !== undefined && (
          <span className={`text-xs font-medium shrink-0 ${color}`}>{label}</span>
        )}
      </div>
      <div className="flex items-center gap-2 text-xs text-gray-500">
        <span className="bg-gray-700 px-2 py-0.5 rounded text-xs">{article.ticker}</span>
        {article.source && <span>{article.source}</span>}
        <span>·</span>
        <span>{timeAgo(article.published_at)}</span>
      </div>
    </div>
  )
}
