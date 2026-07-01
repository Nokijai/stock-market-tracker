import { cn } from '../../lib/utils'
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'destructive' | 'outline' | 'ghost' | 'success'
  size?: 'sm' | 'md' | 'lg'
}
export function Button({ variant = 'default', size = 'md', className, children, ...props }: ButtonProps) {
  return (
    <button className={cn(
      'inline-flex items-center justify-center rounded-lg font-medium transition-colors disabled:opacity-50',
      {
        'default': 'bg-blue-600 hover:bg-blue-700 text-white',
        'destructive': 'bg-red-600 hover:bg-red-700 text-white',
        'outline': 'border border-gray-600 hover:bg-gray-700 text-gray-100',
        'ghost': 'hover:bg-gray-700 text-gray-300',
        'success': 'bg-green-600 hover:bg-green-700 text-white',
      }[variant],
      { 'sm': 'px-3 py-1.5 text-sm', 'md': 'px-4 py-2 text-sm', 'lg': 'px-6 py-3 text-base' }[size],
      className
    )} {...props}>{children}</button>
  )
}
