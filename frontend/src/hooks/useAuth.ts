import { useAuthStore } from '../store/authStore'
import api from '../lib/api'

export function useAuth() {
  const { token, user, setToken, setUser, logout } = useAuthStore()

  const login = async (email: string, password: string) => {
    const res = await api.post('/auth/login', { email, password })
    setToken(res.data.access_token)
    const me = await api.get('/auth/me')
    setUser(me.data)
    return res.data
  }

  const register = async (email: string, password: string) => {
    await api.post('/auth/register', { email, password })
  }

  return { token, user, login, register, logout, isAuthenticated: !!token }
}
