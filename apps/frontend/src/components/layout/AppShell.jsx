import { Outlet } from 'react-router-dom';
import Header from './Header';
import Sidebar from './Sidebar';
import useUIStore from '@/stores/useUIStore';
import { cn } from '@/lib/utils';

/**
 * AppShell Component
 *
 * Main layout wrapper that provides:
 * - Persistent header
 * - Collapsible sidebar navigation
 * - Main content area with outlet for page components
 */
export default function AppShell() {
  const { sidebarCollapsed } = useUIStore();

  return (
    <div className="min-h-screen bg-background">
      <Sidebar />
      <Header />
      
      {/* Main content area */}
      <main
        className={cn(
          'pt-16 transition-all duration-300',
          sidebarCollapsed ? 'pl-16' : 'pl-64'
        )}
      >
        <div className="container mx-auto p-6">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
