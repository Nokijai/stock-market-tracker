import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { Input } from '../components/ui/Input'
import { Button } from '../components/ui/Button'
import { TrendingUp } from 'lucide-react'

export function RegisterPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { register } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (password !== confirm) { setError('Passwords do not match'); return }
    setError(''); setLoading(true)
    try { await register(email, password); navigate('/login') }
    catch (e: any) { setError(e.response?.data?.detail || 'Registration failed') }
    finally { setLoading(false) }
  }

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center p-4">
      <div className="bg-gray-800 border border-gray-700 rounded-2xl p-8 w-full max-w-md shadow-2xl">
        <div className="flex items-center gap-2 justify-center mb-8 text-blue-400 text-2xl font-bold"><TrendingUp size={28}/> StockTracker</div>
        <h2 className="text-xl font-semibold text-gray-100 mb-6 text-center">Create your account</h2>
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <Input label="Email" type="email" placeholder="you@example.com" value={email} onChange={e => setEmail(e.target.value)} required />
          <Input label="Password" type="password" placeholder="At least 8 characters" value={password} onChange={e => setPassword(e.target.value)} required />
          <Input label="Confirm Password" type="password" placeholder="Repeat password" value={confirm} onChange={e => setConfirm(e.target.value)} required />
          {error && <p className="text-red-400 text-sm bg-red-900/20 border border-red-800 rounded-lg p-3">{error}</p>}
          <Button type="submit" size="lg" disabled={loading} className="mt-2">{loading ? 'Creating...' : 'Create Account'}</Button>
        </form>
        <p className="text-center text-gray-500 text-sm mt-6">Already have an account? <Link to="/login" className="text-blue-400 hover:text-blue-300">Sign in</Link></p>
      </div>
    </div>
  )
}
