import { cn } from '../../lib/utils'
interface BadgeProps { variant?: 'default' | 'success' | 'danger' | 'warning' | 'info'; children: React.ReactNode; className?: string }
export function Badge({ variant = 'default', className, children }: BadgeProps) {
  return (
    <span className={cn('inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium', {
      default: 'bg-gray-700 text-gray-300',
      success: 'bg-green-900/50 text-green-400',
      danger: 'bg-red-900/50 text-red-400',
      warning: 'bg-yellow-900/50 text-yellow-400',
      info: 'bg-blue-900/50 text-blue-400',
    }[variant], className)}>{children}</span>
  )
}
