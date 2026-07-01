import * as TooltipPrimitive from '@radix-ui/react-tooltip'
interface TooltipProps { content: string; children: React.ReactNode }
export function Tooltip({ content, children }: TooltipProps) {
  return (
    <TooltipPrimitive.Provider>
      <TooltipPrimitive.Root>
        <TooltipPrimitive.Trigger asChild>{children}</TooltipPrimitive.Trigger>
        <TooltipPrimitive.Portal>
          <TooltipPrimitive.Content className="bg-gray-900 border border-gray-600 text-gray-200 text-xs px-3 py-2 rounded-lg max-w-xs shadow-xl z-50" sideOffset={5}>
            {content}
            <TooltipPrimitive.Arrow className="fill-gray-900" />
          </TooltipPrimitive.Content>
        </TooltipPrimitive.Portal>
      </TooltipPrimitive.Root>
    </TooltipPrimitive.Provider>
  )
}
