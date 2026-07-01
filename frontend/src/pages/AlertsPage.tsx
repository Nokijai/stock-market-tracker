import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { usePortfolio } from '../hooks/usePortfolio'
import api from '../lib/api'
import type { Alert } from '../types'
import { Layout } from '../components/layout/Layout'
import { Card } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { Input } from '../components/ui/Input'
import { Badge } from '../components/ui/Badge'
import { formatCurrency, formatDate } from '../lib/utils'
import { Bell, Trash2, Plus } from 'lucide-react'

export function AlertsPage() {
  const { data: alerts = [] } = useQuery<Alert[]>({ queryKey: ['alerts'], queryFn: () => api.get('/alerts/').then(r => r.data) })
  const { data: holdings = [] } = usePortfolio()
  const qc = useQueryClient()
  const deleteAlert = useMutation({ mutationFn: (id: number) => api.delete(`/alerts/${id}`), onSuccess: () => qc.invalidateQueries({ queryKey: ['alerts'] }) })
  const createAlert = useMutation({ mutationFn: (data: any) => api.post('/alerts/', data).then(r => r.data), onSuccess: () => { qc.invalidateQueries({ queryKey: ['alerts'] }); setForm({ ticker: '', alert_type: 'price_above', threshold: '' }) } })

  const [form, setForm] = useState({ ticker: '', alert_type: 'price_above', threshold: '' })
  const [formError, setFormError] = useState('')

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!form.ticker || !form.threshold) { setFormError('All fields required'); return }
    try { await createAlert.mutateAsync({ ...form, threshold: parseFloat(form.threshold) }); setFormError('') }
    catch (e: any) { setFormError(e.response?.data?.detail || 'Failed to create alert') }
  }

  return (
    <Layout>
      <h1 className="text-2xl font-bold text-gray-100 mb-6">Alerts</h1>
      <div className="grid md:grid-cols-2 gap-6">
        <Card>
          <h2 className="font-semibold text-gray-100 mb-4 flex items-center gap-2"><Plus size={16}/>Create Alert</h2>
          <form onSubmit={handleCreate} className="flex flex-col gap-4">
            <div>
              <label className="text-sm text-gray-400 mb-1 block">Ticker</label>
              <select className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={form.ticker} onChange={e => setForm(f => ({ ...f, ticker: e.target.value }))}>
                <option value="">Select ticker</option>
                {holdings.map(h => <option key={h.ticker} value={h.ticker}>{h.ticker}</option>)}
              </select>
            </div>
            <div>
              <label className="text-sm text-gray-400 mb-1 block">Alert Type</label>
              <select className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={form.alert_type} onChange={e => setForm(f => ({ ...f, alert_type: e.target.value }))}>
                <option value="price_above">Price rises above</option>
                <option value="price_below">Price drops below</option>
                <option value="pct_change">Day change exceeds ±%</option>
              </select>
            </div>
            <Input label={form.alert_type === 'pct_change' ? 'Percentage (e.g. 5 for ±5%)' : 'Price (USD)'} type="number" step="0.01" placeholder={form.alert_type === 'pct_change' ? '5' : '150.00'} value={form.threshold} onChange={e => setForm(f => ({ ...f, threshold: e.target.value }))} />
            {formError && <p className="text-red-400 text-sm">{formError}</p>}
            <Button type="submit" disabled={createAlert.isPending}>{createAlert.isPending ? 'Creating...' : 'Create Alert'}</Button>
          </form>
        </Card>
        <Card>
          <h2 className="font-semibold text-gray-100 mb-4 flex items-center gap-2"><Bell size={16}/>Active Alerts ({alerts.filter(a => a.is_active).length})</h2>
          {alerts.length === 0 ? <p className="text-gray-500 text-sm text-center py-8">No alerts yet.</p> : (
            <div className="flex flex-col gap-3">
              {alerts.map(alert => (
                <div key={alert.id} className="flex items-center justify-between p-3 bg-gray-700/50 rounded-lg">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-gray-100">{alert.ticker}</span>
                      <Badge variant={alert.is_active ? 'success' : 'default'}>{alert.is_active ? 'Active' : 'Triggered'}</Badge>
                    </div>
                    <p className="text-xs text-gray-400 mt-0.5">
                      {alert.alert_type === 'price_above' ? `Price ≥ ${formatCurrency(alert.threshold)}`
                        : alert.alert_type === 'price_below' ? `Price ≤ ${formatCurrency(alert.threshold)}`
                        : `Day change ≥ ±${alert.threshold}%`}
                      {alert.triggered_at && <span className="ml-2 text-gray-500">· Triggered {formatDate(alert.triggered_at)}</span>}
                    </p>
                  </div>
                  <button onClick={() => deleteAlert.mutate(alert.id)} className="text-gray-500 hover:text-red-400 transition-colors p-1"><Trash2 size={15}/></button>
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>
    </Layout>
  )
}
