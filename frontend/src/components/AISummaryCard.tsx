import { Sparkles, TrendingUp, TrendingDown, Minus, Loader2 } from 'lucide-react'

interface AISummary {
  ticker: string
  bullets: string[]
  sentiment: 'Bullish' | 'Neutral' | 'Bearish'
  reason: string
}

interface Props {
  summary: AISummary | null
  loading: boolean
  error: string | null
}

const SENTIMENT_CONFIG = {
  Bullish:  { icon: TrendingUp,   bg: 'bg-green-900/40',  border: 'border-green-700', text: 'text-green-400',  badge: 'bg-green-800 text-green-300' },
  Neutral:  { icon: Minus,        bg: 'bg-gray-800/60',   border: 'border-gray-600',  text: 'text-gray-400',  badge: 'bg-gray-700  text-gray-300'  },
  Bearish:  { icon: TrendingDown, bg: 'bg-red-900/40',    border: 'border-red-700',   text: 'text-red-400',   badge: 'bg-red-800   text-red-300'   },
}

export default function AISummaryCard({ summary, loading, error }: Props) {
  if (loading) {
    return (
      <div className="rounded-xl border border-gray-700 bg-gray-800/50 p-5 flex items-center gap-3 text-gray-400">
        <Loader2 className="h-5 w-5 animate-spin" />
        <span className="text-sm">Generating AI summary…</span>
      </div>
    )
  }

  if (error || !summary) {
    return (
      <div className="rounded-xl border border-gray-700 bg-gray-800/40 p-5 text-gray-500 text-sm">
        <Sparkles className="h-4 w-4 inline mr-2 opacity-50" />
        AI summary unavailable
      </div>
    )
  }

  const cfg = SENTIMENT_CONFIG[summary.sentiment] ?? SENTIMENT_CONFIG.Neutral
  const Icon = cfg.icon

  return (
    <div className={`rounded-xl border ${cfg.border} ${cfg.bg} p-5 space-y-3`}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 text-sm font-semibold text-white">
          <Sparkles className="h-4 w-4 text-violet-400" />
          AI Summary
        </div>
        <span className={`flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold ${cfg.badge}`}>
          <Icon className="h-3.5 w-3.5" />
          {summary.sentiment}
        </span>
      </div>

      {/* Bullets */}
      <ul className="space-y-1.5">
        {summary.bullets.map((b, i) => (
          <li key={i} className="flex items-start gap-2 text-sm text-gray-200">
            <span className={`mt-1.5 h-1.5 w-1.5 rounded-full flex-shrink-0 ${cfg.text} bg-current`} />
            {b}
          </li>
        ))}
      </ul>

      {/* Reason */}
      <p className={`text-xs ${cfg.text} italic border-t border-gray-700 pt-2`}>
        {summary.reason}
      </p>
    </div>
  )
}
