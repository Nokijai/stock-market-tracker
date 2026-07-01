import { useMarketStatus } from '../hooks/useMarket'
export function MarketStatusBadge() {
  const { data: status } = useMarketStatus()
  if (!status) return null
  return (
    <div className="flex items-center gap-2 bg-gray-800 border border-gray-700 rounded-lg px-3 py-1.5">
      <span className={`w-2.5 h-2.5 rounded-full ${status.is_open ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`} />
      <span className={`text-sm font-medium ${status.is_open ? 'text-green-400' : 'text-red-400'}`}>
        {status.is_open ? 'Market Open' : status.session === 'pre' ? 'Pre-Market' : status.session === 'after' ? 'After-Hours' : 'Market Closed'}
      </span>
    </div>
  )
}
