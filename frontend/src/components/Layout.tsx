import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/auth';
import {
  LayoutDashboard, Brain, Database, Activity, Key, LogOut,
  Settings, ChevronDown, User
} from 'lucide-react';
import { useState } from 'react';

const NAV = [
  { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/models', icon: Brain, label: 'Models' },
  { to: '/datasets', icon: Database, label: 'Datasets' },
  { to: '/training', icon: Activity, label: 'Training' },
  { to: '/api-keys', icon: Key, label: 'API Keys' },
];

export default function Layout() {
  const navigate = useNavigate();
  const user = useAuthStore(s => s.user);
  const logout = useAuthStore(s => s.logout);
  const [userMenuOpen, setUserMenuOpen] = useState(false);

  const handleLogout = () => { logout(); navigate('/login'); };

  return (
    <div className="flex h-screen bg-gray-950 text-white overflow-hidden">
      {/* Sidebar */}
      <aside className="w-60 border-r border-gray-800 flex flex-col shrink-0">
        {/* Logo */}
        <div className="p-5 border-b border-gray-800">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-violet-600 flex items-center justify-center">
              <span className="text-white font-bold text-sm">M</span>
            </div>
            <span className="font-bold text-lg">ModelVault</span>
          </div>
        </div>

        {/* Nav */}
        <nav className="flex-1 p-3 space-y-0.5">
          {NAV.map(({ to, icon: Icon, label }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition ${
                  isActive
                    ? 'bg-violet-600/20 text-violet-400 font-medium'
                    : 'text-gray-400 hover:bg-gray-800 hover:text-gray-200'
                }`
              }
            >
              <Icon size={16} />
              {label}
            </NavLink>
          ))}
        </nav>

        {/* User */}
        <div className="p-3 border-t border-gray-800">
          <button
            onClick={() => setUserMenuOpen(o => !o)}
            className="w-full flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-gray-800 transition"
          >
            <div className="w-7 h-7 rounded-full bg-violet-600 flex items-center justify-center text-xs font-bold">
              {user?.username?.[0]?.toUpperCase() || 'U'}
            </div>
            <div className="flex-1 text-left min-w-0">
              <p className="text-sm text-white truncate">{user?.username}</p>
              <p className="text-xs text-gray-500 truncate">{user?.role}</p>
            </div>
            <ChevronDown size={14} className="text-gray-500" />
          </button>
          {userMenuOpen && (
            <div className="mt-1 bg-gray-800 border border-gray-700 rounded-lg overflow-hidden">
              <button className="w-full flex items-center gap-2 px-3 py-2 text-sm text-gray-300 hover:bg-gray-700">
                <User size={14} /> Profile
              </button>
              <button className="w-full flex items-center gap-2 px-3 py-2 text-sm text-gray-300 hover:bg-gray-700">
                <Settings size={14} /> Settings
              </button>
              <button onClick={handleLogout} className="w-full flex items-center gap-2 px-3 py-2 text-sm text-red-400 hover:bg-gray-700">
                <LogOut size={14} /> Logout
              </button>
            </div>
          )}
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-auto">
        <div className="p-8 max-w-7xl mx-auto">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
