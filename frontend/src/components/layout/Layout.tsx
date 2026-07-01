import { Navbar } from './Navbar'
export function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-gray-900">
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 py-6">{children}</main>
    </div>
  )
}
