import React from 'react'
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom'
import UserPage from './pages/UserPage'
import AdminPage from './pages/AdminPage'

function NavBar() {
  const location = useLocation()

  return (
    <nav className="navbar">
      <div className="navbar-content">
        <h1>🌿 环保文献智能数据库</h1>
        <div className="nav-links">
          <Link
            to="/"
            className={location.pathname === '/' ? 'active' : ''}
          >
            📚 文献检索
          </Link>
          <Link
            to="/admin"
            className={location.pathname === '/admin' ? 'active' : ''}
          >
            ⚙️ 文章管理
          </Link>
        </div>
      </div>
    </nav>
  )
}

function App() {
  return (
    <Router>
      <div className="app">
        <NavBar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<UserPage />} />
            <Route path="/admin" element={<AdminPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
