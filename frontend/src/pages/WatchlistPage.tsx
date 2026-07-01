import { useState } from 'react'
import { useWatchlist, useAddToWatchlist, useRemoveFromWatchlist } from '../hooks/useWatchlist'
import { Layout } from '../components/layout/Layout'
import { WatchlistCard } from '../components/WatchlistCard'
import { Button } from '../components/ui/Button'
import { Modal } from '../components/ui/Modal'
import { Input } from '../components/ui/Input'
import { Plus } from 'lucide-react'

export function WatchlistPage() {
  const { data: items = [], isLoading } = useWatchlist()
  const addToWatchlist = useAddToWatchlist()
  const remove = useRemoveFromWatchlist()
  const [showAdd, setShowAdd] = useState(false)
  const [ticker, setTicker] = useState('')
  const [error, setError] = useState('')

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!ticker) return
    try { await addToWatchlist.mutateAsync(ticker.toUpperCase()); setShowAdd(false); setTicker('') }
    catch (e: any) { setError(e.response?.data?.detail || 'Failed to add') }
  }

  return (
    <Layout>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-100">Watchlist</h1>
        <Button onClick={() => setShowAdd(true)}><Plus size={16} className="mr-1"/>Watch Ticker</Button>
      </div>
      {isLoading ? <div className="animate-pulse grid grid-cols-2 md:grid-cols-4 gap-4">{[1,2,3,4].map(i => <div key={i} className="h-32 bg-gray-800 rounded-xl"/>)}</div>
        : items.length === 0 ? <div className="text-center py-16 text-gray-500">No tickers watched yet.</div>
        : <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">{items.map(item => <WatchlistCard key={item.id} item={item} onRemove={t => remove.mutate(t)}/>)}</div>
      }
      <Modal open={showAdd} onClose={() => setShowAdd(false)} title="Add to Watchlist">
        <form onSubmit={handleAdd} className="flex flex-col gap-4">
          <Input label="Ticker Symbol" placeholder="e.g. TSLA" value={ticker} onChange={e => setTicker(e.target.value.toUpperCase())} autoFocus />
          {error && <p className="text-red-400 text-sm">{error}</p>}
          <Button type="submit" disabled={addToWatchlist.isPending}>{addToWatchlist.isPending ? 'Adding...' : 'Add to Watchlist'}</Button>
        </form>
      </Modal>
    </Layout>
  )
}
