import { Bell, Trash2, CheckCircle, AlertTriangle } from 'lucide-react'
import type { Alert } from '../types'
import { formatCurrency } from '../lib/utils'
import { Card, CardContent } from './ui/Card'
import { Badge } from './ui/Badge'
import { Button } from './ui/Button'
import api from '../lib/api'
import { useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'

interface AlertCardProps {
  alert: Alert
}

const alertTypeLabel: Record<Alert['alert_type'], string> = {
  price_above: 'Price Above',
  price_below: 'Price Below',
  pct_change: '% Change',
}

export function AlertCard({ alert }: AlertCardProps) {
  const queryClient = useQueryClient()
  const [_del, setDeleting] = useState(false)
  const [_tog, setToggling] = useState(false)

  const handleDelete = async () => {
    setDeleting(true)
    try {
      await api.delete(`/alerts/${alert.id}`)
      queryClient.invalidateQueries({ queryKey: ['alerts'] })
    } finally {
      setDeleting(false)
    }
  }

  const handleToggle = async () => {
    setToggling(true)
    try {
      await api.patch(`/alerts/${alert.id}`, { is_active: !alert.is_active })
      queryClient.invalidateQueries({ queryKey: ['alerts'] })
    } finally {
      setToggling(false)
    }
  }

  const isTriggered = !!alert.triggered_at

  return (
    <Card className={`${isTriggered ? 'border-yellow-700' : ''}`}>
      <CardContent className="p-4">
        <div className="flex items-start justify-between gap-3">
          <div className="flex items-start gap-3">
            <div className={`mt-0.5 p-2 rounded-lg ${
              isTriggered ? 'bg-yellow-900/30' : alert.is_active ? 'bg-blue-900/30' : 'bg-gray-700'
            }`}>
              {isTriggered ? (
                <AlertTriangle size={16} className="text-yellow-400" />
              ) : alert.is_active ? (
                <Bell size={16} className="text-blue-400" />
              ) : (
                <Bell size={16} className="text-gray-500" />
              )}
            </div>
            <div>
              <div className="flex items-center gap-2 flex-wrap">
                <span className="font-bold text-gray-100">{alert.ticker}</span>
                <Badge variant={isTriggered ? 'warning' : alert.is_active ? 'info' : 'default'}>
                  {isTriggered ? 'Triggered' : alert.is_active ? 'Active' : 'Paused'}
                </Badge>
              </div>
              <p className="text-sm text-gray-400 mt-0.5">
                {alertTypeLabel[alert.alert_type]}{' '}
                <span className="text-gray-200 font-medium">
                  {alert.alert_type === 'pct_change'
                    ? `${alert.threshold}%`
                    : formatCurrency(alert.threshold)}
                </span>
              </p>
              {isTriggered && alert.triggered_at && (
                <div className="flex items-center gap-1 mt-1 text-xs text-yellow-400">
                  <CheckCircle size={12} />
                  Triggered {new Date(alert.triggered_at).toLocaleDateString()}
                </div>
              )}
            </div>
          </div>

          <div className="flex items-center gap-1 flex-shrink-0">
            <Button
              variant="ghost"
              size="sm"
              onClick={handleToggle}
             
              className="text-xs"
            >
              {alert.is_active ? 'Pause' : 'Activate'}
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={handleDelete}
             
              className="p-1.5 text-gray-500 hover:text-red-400"
            >
              <Trash2 size={14} />
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
