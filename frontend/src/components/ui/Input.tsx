import { cn } from '../../lib/utils'
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> { label?: string; error?: string }
export function Input({ label, error, className, ...props }: InputProps) {
  return (
    <div className="flex flex-col gap-1">
      {label && <label className="text-sm text-gray-400">{label}</label>}
      <input className={cn('bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500', error && 'border-red-500', className)} {...props} />
      {error && <p className="text-xs text-red-400">{error}</p>}
    </div>
  )
}
