import { Search, Plus } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import ThemeToggle from '@/components/ui/ThemeToggle';
import SearchModal from '@/components/ui/SearchModal';
import NotificationsDropdown from '@/components/ui/NotificationsDropdown';
import LanguageSelector from '@/components/international/LanguageSelector';
import useUIStore from '@/stores/useUIStore';
import { cn } from '@/lib/utils';
import { useNavigate } from 'react-router-dom';

export default function Header() {
  const { sidebarCollapsed } = useUIStore();
  const navigate = useNavigate();

  return (
    <>
      <header
        className={cn(
          'fixed top-0 right-0 z-30 h-16 border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 transition-all duration-300',
          sidebarCollapsed ? 'left-16' : 'left-64'
        )}
      >
        <div className="flex h-full items-center justify-between px-6">
          {/* Search */}
          <div className="flex-1 max-w-md">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <input
                type="text"
                placeholder="Search shipments, tracking numbers..."
                className="w-full rounded-lg border border-input bg-background pl-9 pr-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring cursor-pointer"
                onClick={() => {
                  // Trigger search modal on click
                  const event = new KeyboardEvent('keydown', {
                    key: 'k',
                    metaKey: true,
                    bubbles: true,
                  });
                  window.dispatchEvent(event);
                }}
                readOnly
                aria-label="Search shipments and tracking numbers"
                onKeyDown={(e) => {
                  if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
                    e.preventDefault();
                    const event = new KeyboardEvent('keydown', {
                      key: 'k',
                      metaKey: true,
                      bubbles: true,
                    });
                    window.dispatchEvent(event);
                  }
                }}
              />
              <kbd className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground opacity-100">
                <span className="text-xs">⌘</span>K
              </kbd>
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center gap-2">
            <Button
              variant="default"
              size="sm"
              className="gap-2"
              onClick={() => navigate('/shipments/new')}
            >
              <Plus className="h-4 w-4" />
              <span className="hidden sm:inline">New Shipment</span>
            </Button>

            <NotificationsDropdown />

            <LanguageSelector />

            <ThemeToggle />

            <div className="ml-2 flex items-center gap-2">
              <button
                className="h-8 w-8 rounded-full bg-primary flex items-center justify-center text-primary-foreground font-medium text-sm hover:opacity-80 transition-opacity"
                aria-label="User menu"
              >
                U
              </button>
            </div>
          </div>
        </div>
      </header>
      <SearchModal />
    </>
  );
}
