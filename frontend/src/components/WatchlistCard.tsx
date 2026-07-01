import type { WatchlistItem } from '../types'
import { formatCurrency, formatPercent, getChangeColor } from '../lib/utils'
import { Button } from './ui/Button'
import { Plus, Minus } from 'lucide-react'
import { Link } from 'react-router-dom'

interface Props { item: WatchlistItem; onRemove: (ticker: string) => void; onAddToPortfolio?: () => void }
export function WatchlistCard({ item, onRemove, onAddToPortfolio }: Props) {
  const dayColor = getChangeColor(item.day_change_pct)
  return (
    <div className="bg-gray-800 border border-gray-700 rounded-xl p-4 flex flex-col gap-2">
      <div className="flex items-start justify-between">
        <Link to={`/stock/${item.ticker}`} className="hover:text-blue-400 transition-colors">
          <div className="font-bold text-lg text-gray-100">{item.ticker}</div>
          <div className="text-xs text-gray-500 truncate">{item.company_name || '—'}</div>
        </Link>
        <button onClick={() => onRemove(item.ticker)} className="text-gray-600 hover:text-red-400 transition-colors"><Minus size={16}/></button>
      </div>
      <div>
        <div className="font-medium text-xl text-gray-100">{item.current_price ? formatCurrency(item.current_price) : '—'}</div>
        <div className={`text-sm font-medium ${dayColor}`}>{item.day_change_pct ? formatPercent(item.day_change_pct) + ' today' : ''}</div>
      </div>
      {onAddToPortfolio && (
        <Button variant="outline" size="sm" onClick={onAddToPortfolio} className="mt-1"><Plus size={14} className="mr-1"/>Add to Portfolio</Button>
      )}
    </div>
  )
}
