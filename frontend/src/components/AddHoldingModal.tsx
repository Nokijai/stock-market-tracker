import { useState } from 'react'
import { Modal } from './ui/Modal'
import { Input } from './ui/Input'
import { Button } from './ui/Button'
import { useAddHolding, useUpdateHolding } from '../hooks/usePortfolio'
import type { Holding } from '../types'

interface Props { open: boolean; onClose: () => void; editing?: Holding | null }
export function AddHoldingModal({ open, onClose, editing }: Props) {
  const [ticker, setTicker] = useState(editing?.ticker || '')
  const [shares, setShares] = useState(editing?.shares?.toString() || '')
  const [avgCost, setAvgCost] = useState(editing?.avg_cost?.toString() || '')
  const [error, setError] = useState('')
  const addHolding = useAddHolding()
  const updateHolding = useUpdateHolding()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    if (!ticker || !shares || !avgCost) { setError('All fields required'); return }
    try {
      if (editing) {
        await updateHolding.mutateAsync({ id: editing.id, shares: parseFloat(shares), avg_cost: parseFloat(avgCost) })
      } else {
        await addHolding.mutateAsync({ ticker: ticker.toUpperCase(), shares: parseFloat(shares), avg_cost: parseFloat(avgCost) })
      }
      onClose()
    } catch (e: any) {
      setError(e.response?.data?.detail || 'Failed to save holding')
    }
  }

  return (
    <Modal open={open} onClose={onClose} title={editing ? `Edit ${editing.ticker}` : 'Add Holding'}>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <Input label="Ticker Symbol" placeholder="e.g. AAPL" value={ticker} onChange={e => setTicker(e.target.value.toUpperCase())} disabled={!!editing} />
        <Input label="Shares" type="number" step="0.001" min="0" placeholder="e.g. 10" value={shares} onChange={e => setShares(e.target.value)} />
        <Input label="Avg Cost per Share (USD)" type="number" step="0.01" min="0" placeholder="e.g. 150.00" value={avgCost} onChange={e => setAvgCost(e.target.value)} />
        {error && <p className="text-red-400 text-sm">{error}</p>}
        <Button type="submit" disabled={addHolding.isPending || updateHolding.isPending}>
          {addHolding.isPending || updateHolding.isPending ? 'Saving...' : editing ? 'Update' : 'Add Holding'}
        </Button>
      </form>
    </Modal>
  )
}
