import { useState } from 'react'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts'
import { useHistory } from '../hooks/useMarket'
import { formatCurrency } from '../lib/utils'
import type { HistoryPoint } from '../types'

const PERIODS = [{ label: '1W', value: '1wk' }, { label: '1M', value: '1mo' }, { label: '3M', value: '3mo' }, { label: '1Y', value: '1y' }]

interface PriceChartProps {
  ticker: string
  period?: string
  onPeriodChange?: (period: string) => void
  benchmarkData?: HistoryPoint[]
}

export function PriceChart({ ticker, period: externalPeriod, onPeriodChange, benchmarkData }: PriceChartProps) {
  const [internalPeriod, setInternalPeriod] = useState('1mo')
  const activePeriod = externalPeriod ?? internalPeriod
  const { data, isLoading } = useHistory(ticker, activePeriod)

  const setPeriod = (p: string) => {
    if (onPeriodChange) {
      onPeriodChange(p)
    } else {
      setInternalPeriod(p)
    }
  }

  const color = data && data.length >= 2
    ? data[data.length - 1].close >= data[0].close ? '#22c55e' : '#ef4444'
    : '#3b82f6'

  return (
    <div>
      <div className="flex gap-2 mb-3">
        {PERIODS.map(p => (
          <button key={p.value} onClick={() => setPeriod(p.value)}
            className={`px-3 py-1 rounded-lg text-xs font-medium transition-colors ${activePeriod === p.value ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-400 hover:text-gray-200'}`}>{p.label}</button>
        ))}
      </div>
      {isLoading ? (
        <div className="h-48 bg-gray-700/30 rounded-lg animate-pulse" />
      ) : (
        <ResponsiveContainer width="100%" height={200}>
          <LineChart data={data}>
            <XAxis dataKey="date" tick={{ fill: '#9ca3af', fontSize: 11 }} tickLine={false} axisLine={false} tickFormatter={d => new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })} />
            <YAxis domain={['auto', 'auto']} tick={{ fill: '#9ca3af', fontSize: 11 }} tickLine={false} axisLine={false} tickFormatter={v => `$${v.toFixed(0)}`} width={55} />
            <Tooltip formatter={(v: any) => [formatCurrency(v as number), 'Price']} contentStyle={{ background: '#1f2937', border: '1px solid #374151', borderRadius: 8 }} labelStyle={{ color: '#9ca3af' }} />
            <Legend
              wrapperStyle={{ paddingTop: 8 }}
              formatter={(value: string) => <span style={{ color: '#d1d5db', fontSize: 12 }}>{value}</span>}
            />
            <Line type="monotone" dataKey="close" stroke={color} dot={false} strokeWidth={2} name={`${ticker}`} />
            {benchmarkData && (
              <Line type="monotone" dataKey="close" data={benchmarkData} stroke="#f59e0b" dot={false} strokeWidth={2} strokeDasharray="4 3" name="S&P 500 (SPY)" />
            )}
          </LineChart>
        </ResponsiveContainer>
      )}
    </div>
  )
}