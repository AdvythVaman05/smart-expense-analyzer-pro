// src/components/Navbar.jsx
import { LogOut, BarChart3 } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import './Navbar.css';

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const initials = user?.full_name
    ? user.full_name.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase()
    : user?.email?.[0]?.toUpperCase() ?? '?';

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <div className="brand-icon"><BarChart3 size={16} /></div>
        Smart Expense Analyzer
      </div>
      <div className="navbar-right">
        {user && (
          <div className="user-chip">
            <div className="avatar">{initials}</div>
            {user.full_name || user.email}
          </div>
        )}
        <button className="btn btn-ghost" onClick={handleLogout} title="Logout">
          <LogOut size={15} /> Logout
        </button>
      </div>
    </nav>
  );
}
