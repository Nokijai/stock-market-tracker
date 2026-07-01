import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts'
import type { Holding } from '../types'
import { formatCurrency } from '../lib/utils'

const COLORS = ['#3b82f6','#8b5cf6','#06b6d4','#10b981','#f59e0b','#ef4444','#ec4899','#84cc16']

export function PortfolioPieChart({ holdings }: { holdings: Holding[] }) {
  const data = holdings.filter(h => h.current_value).map(h => ({ name: h.ticker, value: h.current_value! }))
  if (!data.length) return <div className="flex items-center justify-center h-48 text-gray-500 text-sm">No data</div>
  return (
    <ResponsiveContainer width="100%" height={240}>
      <PieChart>
        <Pie data={data} cx="50%" cy="50%" innerRadius={60} outerRadius={90} dataKey="value" paddingAngle={2}>
          {data.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
        </Pie>
        <Tooltip formatter={(v: any) => formatCurrency(v as number)} contentStyle={{ background: '#1f2937', border: '1px solid #374151', borderRadius: 8 }} />
        <Legend wrapperStyle={{ fontSize: 12 }} />
      </PieChart>
    </ResponsiveContainer>
  )
}
