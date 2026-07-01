import { useState } from 'react'
import { Modal } from './ui/Modal'
import { Input } from './ui/Input'
import { Button } from './ui/Button'
import { useAddToWatchlist } from '../hooks/useWatchlist'

interface AddWatchlistModalProps {
  open: boolean
  onClose: () => void
  defaultTicker?: string
}

export function AddWatchlistModal({ open, onClose, defaultTicker = '' }: AddWatchlistModalProps) {
  const [ticker, setTicker] = useState(defaultTicker)
  const [error, setError] = useState('')

  const mutation = useAddToWatchlist()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!ticker.trim()) {
      setError('Ticker symbol is required')
      return
    }
    setError('')
    try {
      await mutation.mutateAsync(ticker.trim().toUpperCase())
      setTicker('')
      onClose()
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail
      setError(msg || 'Failed to add to watchlist.')
    }
  }

  return (
    <Modal open={open} onClose={onClose} title="Add to Watchlist">
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          label="Ticker Symbol"
          placeholder="e.g. TSLA"
          value={ticker}
          onChange={(e) => setTicker(e.target.value.toUpperCase())}
          error={error}
          autoFocus
        />
        <p className="text-xs text-gray-500">
          We'll track real-time prices and notify you of movements.
        </p>
        {error && (
          <div className="bg-red-900/30 border border-red-700 rounded-lg p-3 text-sm text-red-400">
            {error}
          </div>
        )}
        <div className="flex gap-3 pt-2">
          <Button type="button" variant="outline" className="flex-1" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" className="flex-1">
            Add to Watchlist
          </Button>
        </div>
      </form>
    </Modal>
  )
}
