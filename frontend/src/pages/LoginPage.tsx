import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { Input } from '../components/ui/Input'
import { Button } from '../components/ui/Button'
import { TrendingUp } from 'lucide-react'

export function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(''); setLoading(true)
    try { await login(email, password); navigate('/dashboard') }
    catch (e: any) { setError(e.response?.data?.detail || 'Invalid credentials') }
    finally { setLoading(false) }
  }

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center p-4">
      <div className="bg-gray-800 border border-gray-700 rounded-2xl p-8 w-full max-w-md shadow-2xl">
        <div className="flex items-center gap-2 justify-center mb-8 text-blue-400 text-2xl font-bold">
          <TrendingUp size={28} /> StockTracker
        </div>
        <h2 className="text-xl font-semibold text-gray-100 mb-6 text-center">Sign in to your account</h2>
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <Input label="Email" type="email" placeholder="you@example.com" value={email} onChange={e => setEmail(e.target.value)} required />
          <Input label="Password" type="password" placeholder="••••••••" value={password} onChange={e => setPassword(e.target.value)} required />
          {error && <p className="text-red-400 text-sm bg-red-900/20 border border-red-800 rounded-lg p-3">{error}</p>}
          <Button type="submit" size="lg" disabled={loading} className="mt-2">{loading ? 'Signing in...' : 'Sign In'}</Button>
        </form>
        <p className="text-center text-gray-500 text-sm mt-6">Don't have an account? <Link to="/register" className="text-blue-400 hover:text-blue-300">Register</Link></p>
      </div>
    </div>
  )
}
