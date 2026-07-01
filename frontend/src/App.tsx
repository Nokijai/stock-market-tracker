import { Navigate, Route, Routes } from 'react-router-dom'
import { useAuthStore } from './store/authStore'
import { LoginPage } from './pages/LoginPage'
import { RegisterPage } from './pages/RegisterPage'
import { DashboardPage } from './pages/DashboardPage'
import { PortfolioPage } from './pages/PortfolioPage'
import { WatchlistPage } from './pages/WatchlistPage'
import { NewsPage } from './pages/NewsPage'
import { AlertsPage } from './pages/AlertsPage'
import { StockDetailPage } from './pages/StockDetailPage'

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const { token } = useAuthStore()
  return token ? <>{children}</> : <Navigate to="/login" replace />
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/dashboard" element={<PrivateRoute><DashboardPage /></PrivateRoute>} />
      <Route path="/portfolio" element={<PrivateRoute><PortfolioPage /></PrivateRoute>} />
      <Route path="/watchlist" element={<PrivateRoute><WatchlistPage /></PrivateRoute>} />
      <Route path="/news" element={<PrivateRoute><NewsPage /></PrivateRoute>} />
      <Route path="/alerts" element={<PrivateRoute><AlertsPage /></PrivateRoute>} />
      <Route path="/stock/:ticker" element={<PrivateRoute><StockDetailPage /></PrivateRoute>} />
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  )
}
