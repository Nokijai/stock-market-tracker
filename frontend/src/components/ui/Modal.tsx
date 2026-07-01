import * as Dialog from '@radix-ui/react-dialog'
import { X } from 'lucide-react'
interface ModalProps { open: boolean; onClose: () => void; title: string; children: React.ReactNode }
export function Modal({ open, onClose, title, children }: ModalProps) {
  return (
    <Dialog.Root open={open} onOpenChange={(o) => !o && onClose()}>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/70 z-40" />
        <Dialog.Content className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-gray-800 border border-gray-700 rounded-xl p-6 w-full max-w-md z-50 shadow-2xl">
          <div className="flex items-center justify-between mb-4">
            <Dialog.Title className="text-lg font-semibold text-gray-100">{title}</Dialog.Title>
            <button onClick={onClose} className="text-gray-400 hover:text-gray-200"><X size={18} /></button>
          </div>
          {children}
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  )
}
