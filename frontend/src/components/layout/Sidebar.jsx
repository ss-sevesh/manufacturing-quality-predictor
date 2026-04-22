import { NavLink } from 'react-router-dom';
import { LayoutDashboard, FlaskConical, History, BarChart3, Activity } from 'lucide-react';

const links = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/predict', label: 'Predict', icon: FlaskConical },
  { to: '/history', label: 'History', icon: History },
  { to: '/performance', label: 'Performance', icon: BarChart3 },
  { to: '/monitoring', label: 'Monitoring', icon: Activity },
];

export default function Sidebar() {
  return (
    <aside className="fixed left-0 top-0 z-30 flex h-screen w-60 flex-col border-r border-gray-200 bg-white dark:border-gray-800 dark:bg-gray-900">
      <div className="flex h-16 items-center gap-2 px-6 border-b border-gray-200 dark:border-gray-800">
        <div className="h-8 w-8 rounded-lg bg-blue-600 flex items-center justify-center">
          <FlaskConical size={18} className="text-white" />
        </div>
        <span className="text-lg font-bold tracking-tight">QualityML</span>
      </div>

      <nav className="flex-1 px-3 py-4 space-y-1">
        {links.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300'
                  : 'text-gray-600 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-800'
              }`
            }
          >
            <Icon size={18} />
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="px-4 py-4 border-t border-gray-200 dark:border-gray-800">
        <p className="text-xs text-gray-400 dark:text-gray-500">MLP Quality Predictor v0.1.0</p>
      </div>
    </aside>
  );
}
