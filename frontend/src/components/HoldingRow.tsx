import type { Holding } from '../types'
import { formatCurrency, formatPercent, getChangeColor } from '../lib/utils'
import { Button } from './ui/Button'
import { Pencil, Trash2, TrendingUp, TrendingDown } from 'lucide-react'

interface Props { holding: Holding; onDelete: (id: number) => void; onEdit: (h: Holding) => void }
export function HoldingRow({ holding: h, onDelete, onEdit }: Props) {
  const gainColor = getChangeColor(h.unrealized_gain_pct)
  const dayColor = getChangeColor(h.day_change_pct)
  return (
    <tr className="border-b border-gray-700/50 hover:bg-gray-800/50 transition-colors">
      <td className="py-3 px-4">
        <div className="font-bold text-gray-100">{h.ticker}</div>
        <div className="text-xs text-gray-500 truncate max-w-[150px]">{h.company_name || '—'}</div>
      </td>
      <td className="py-3 px-4 text-sm text-gray-300">{h.shares} @ {formatCurrency(h.avg_cost)}</td>
      <td className="py-3 px-4">
        <div className="font-medium text-gray-100">{h.current_price ? formatCurrency(h.current_price) : '—'}</div>
        <div className={`text-xs ${dayColor}`}>{h.day_change_pct ? formatPercent(h.day_change_pct) + ' today' : ''}</div>
      </td>
      <td className="py-3 px-4 font-medium text-gray-100">{h.current_value ? formatCurrency(h.current_value) : '—'}</td>
      <td className="py-3 px-4">
        <div className={`font-medium ${gainColor}`}>{h.unrealized_gain ? formatCurrency(h.unrealized_gain) : '—'}</div>
        <div className={`text-xs flex items-center gap-1 ${gainColor}`}>
          {h.unrealized_gain_pct !== undefined && (h.unrealized_gain_pct >= 0 ? <TrendingUp size={12}/> : <TrendingDown size={12}/>)}
          {h.unrealized_gain_pct ? formatPercent(h.unrealized_gain_pct) : ''}
        </div>
      </td>
      <td className="py-3 px-4 text-sm text-gray-400">{h.weight ? `${h.weight.toFixed(1)}%` : '—'}</td>
      <td className="py-3 px-4">
        <div className="flex gap-2">
          <Button variant="ghost" size="sm" onClick={() => onEdit(h)}><Pencil size={14}/></Button>
          <Button variant="ghost" size="sm" onClick={() => onDelete(h.id)} className="text-red-400 hover:text-red-300"><Trash2 size={14}/></Button>
        </div>
      </td>
    </tr>
  )
}
