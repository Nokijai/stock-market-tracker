import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import { useMarketStatus } from '../../hooks/useMarket'
import { TrendingUp, LayoutDashboard, Briefcase, Eye, Newspaper, Bell, LogOut } from 'lucide-react'

const NAV = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/portfolio', label: 'Portfolio', icon: Briefcase },
  { to: '/watchlist', label: 'Watchlist', icon: Eye },
  { to: '/news',      label: 'News',      icon: Newspaper },
  { to: '/alerts',    label: 'Alerts',    icon: Bell },
]

export function Navbar() {
  const { user, logout } = useAuth()
  const { data: status } = useMarketStatus()
  const navigate = useNavigate()
  const location = useLocation()

  const handleLogout = () => { logout(); navigate('/login') }

  const isActive = (to: string) =>
    to === '/dashboard'
      ? location.pathname === to
      : location.pathname.startsWith(to)

  return (
    <>
      {/* ── Top bar ── */}
      <nav className="bg-gray-900 border-b border-gray-700 sticky top-0 z-30">
        <div className="max-w-7xl mx-auto px-4 flex items-center justify-between h-14">
          <Link to="/dashboard" className="flex items-center gap-2 font-bold text-blue-400 text-lg">
            <TrendingUp size={20} /> StockTracker
          </Link>

          {/* Desktop nav */}
          <div className="hidden md:flex items-center gap-1">
            {NAV.map(({ to, label, icon: Icon }) => (
              <Link
                key={to}
                to={to}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm transition-colors
                  ${isActive(to) ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-gray-100 hover:bg-gray-800'}`}
              >
                <Icon size={15} />{label}
              </Link>
            ))}
          </div>

          <div className="flex items-center gap-3">
            {status && (
              <div className="flex items-center gap-1.5 text-xs">
                <span className={`w-2 h-2 rounded-full ${status.is_open ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`} />
                <span className={status.is_open ? 'text-green-400' : 'text-red-400'}>
                  {status.is_open ? 'Market Open' : status.session === 'pre' ? 'Pre-Market' : status.session === 'after' ? 'After-Hours' : 'Closed'}
                </span>
              </div>
            )}
            <span className="text-xs text-gray-500 hidden sm:block">{user?.email}</span>
            <button onClick={handleLogout} className="text-gray-400 hover:text-gray-200 p-1 rounded">
              <LogOut size={16} />
            </button>
          </div>
        </div>
      </nav>

      {/* ── Mobile bottom tab bar ── */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 z-30 bg-gray-900 border-t border-gray-700">
        <div className="flex items-center justify-around h-16">
          {NAV.map(({ to, label, icon: Icon }) => (
            <Link
              key={to}
              to={to}
              className={`flex flex-col items-center gap-0.5 px-3 py-2 rounded-lg text-xs transition-colors
                ${isActive(to) ? 'text-blue-400' : 'text-gray-500 hover:text-gray-300'}`}
            >
              <Icon size={20} />
              <span>{label}</span>
            </Link>
          ))}
        </div>
      </nav>
    </>
  )
}
