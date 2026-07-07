import { useNavigate } from 'react-router-dom'
import { useState } from 'react'
import { usePortfolio, usePortfolioSummary, useDeleteHolding } from '../hooks/usePortfolio'
import { Layout } from '../components/layout/Layout'
import { Card } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { HoldingRow } from '../components/HoldingRow'
import { AddHoldingModal } from '../components/AddHoldingModal'
import { formatCurrency, formatPercent, getChangeColor } from '../lib/utils'
import { Plus, Upload } from 'lucide-react'
import type { Holding } from '../types'

export function PortfolioPage() {
  const navigate = useNavigate()
  const { data: holdings = [], isLoading } = usePortfolio()
  const { data: summary } = usePortfolioSummary()
  const deleteHolding = useDeleteHolding()
  const [showAdd, setShowAdd] = useState(false)
  const [editing, setEditing] = useState<Holding | null>(null)

  return (
    <Layout>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-100">Portfolio</h1>
          {summary && <p className={`text-sm mt-1 ${getChangeColor(summary.total_return_pct)}`}>{formatCurrency(summary.total_market_value)} · {formatPercent(summary.total_return_pct)} all time</p>}
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" onClick={() => navigate('/import')}><Upload size={16} className="mr-1"/>Import CSV</Button>
          <Button onClick={() => setShowAdd(true)}><Plus size={16} className="mr-1"/>Add Holding</Button>
        </div>
      </div>

      {summary && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          {[
            { label: 'Market Value', value: formatCurrency(summary.total_market_value) },
            { label: 'Cost Basis', value: formatCurrency(summary.total_cost_basis) },
            { label: 'Unrealized P&L', value: formatCurrency(summary.total_unrealized_pnl), colorPct: summary.total_return_pct },
            { label: 'Total Return', value: formatPercent(summary.total_return_pct), colorPct: summary.total_return_pct },
          ].map(({ label, value, colorPct }) => (
            <Card key={label}>
              <p className="text-xs text-gray-500 mb-1">{label}</p>
              <p className={`text-xl font-bold ${colorPct !== undefined ? getChangeColor(colorPct) : 'text-gray-100'}`}>{value}</p>
            </Card>
          ))}
        </div>
      )}

      <Card>
        {isLoading ? (
          <div className="animate-pulse space-y-3 p-4">{[1,2,3].map(i => <div key={i} className="h-12 bg-gray-700 rounded"/>)}</div>
        ) : holdings.length === 0 ? (
          <div className="text-center py-16">
            <p className="text-gray-500 mb-4">No holdings yet. Add your first stock!</p>
            <Button onClick={() => setShowAdd(true)}><Plus size={16} className="mr-1"/>Add Holding</Button>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-700 text-xs text-gray-500 uppercase tracking-wide">
                  {['Ticker', 'Position', 'Price', 'Value', 'P&L', 'Weight', ''].map(h => <th key={h} className="py-3 px-4 text-left font-medium">{h}</th>)}
                </tr>
              </thead>
              <tbody>
                {holdings.map(h => <HoldingRow key={h.id} holding={h} onDelete={id => deleteHolding.mutate(id)} onEdit={setEditing}/>)}
              </tbody>
            </table>
          </div>
        )}
      </Card>

      <AddHoldingModal open={showAdd || !!editing} onClose={() => { setShowAdd(false); setEditing(null) }} editing={editing} />
    </Layout>
  )
}