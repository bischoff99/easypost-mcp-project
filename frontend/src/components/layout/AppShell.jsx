import { useEffect } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';
import useUIStore from '@/stores/useUIStore';
import { cn } from '@/lib/utils';

export default function AppShell() {
  const { theme, sidebarCollapsed } = useUIStore();

  useEffect(() => {
    // Apply theme to document
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [theme]);

  return (
    <div className="min-h-screen bg-background">
      <Sidebar />
      <Header />
      <main
        className={cn('pt-16 transition-all duration-300', sidebarCollapsed ? 'pl-16' : 'pl-64')}
      >
        <div className="p-6">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
