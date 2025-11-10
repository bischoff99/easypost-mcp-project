import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Package, X } from 'lucide-react';
import * as Dialog from '@radix-ui/react-dialog';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { shipmentAPI } from '@/services/api';
import { logger } from '@/lib/logger';

/**
 * SearchModal Component
 *
 * Global search modal with ⌘K keyboard shortcut
 * Searches shipments, tracking numbers, and addresses
 */
export default function SearchModal() {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const navigate = useNavigate();

  // Keyboard shortcut handler
  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setOpen(true);
      }
      if (e.key === 'Escape' && open) {
        setOpen(false);
        setQuery('');
        setResults([]);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [open]);

  // Search handler
  const handleSearch = async (searchQuery) => {
    if (!searchQuery.trim()) {
      setResults([]);
      return;
    }

    setIsSearching(true);
    try {
      // Search shipments
      const shipmentsResponse = await shipmentAPI.getRecentShipments(20);
      const shipments = shipmentsResponse.data || [];

      // Filter results
      const filtered = shipments.filter((shipment) => {
        const searchLower = searchQuery.toLowerCase();
        return (
          shipment.tracking_number?.toLowerCase().includes(searchLower) ||
          shipment.id?.toLowerCase().includes(searchLower) ||
          shipment.from_address?.name?.toLowerCase().includes(searchLower) ||
          shipment.to_address?.name?.toLowerCase().includes(searchLower) ||
          shipment.carrier?.toLowerCase().includes(searchLower)
        );
      });

      setResults(filtered.slice(0, 10)); // Limit to 10 results
    } catch (error) {
      logger.error('Search error:', error);
      setResults([]);
    } finally {
      setIsSearching(false);
    }
  };

  // Debounced search
  useEffect(() => {
    if (!query.trim()) {
      setResults([]);
      return;
    }

    const timer = setTimeout(() => {
      handleSearch(query);
    }, 300);

    return () => clearTimeout(timer);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [query]);

  const handleResultClick = (shipment) => {
    navigate(`/shipments`);
    setOpen(false);
    setQuery('');
    setResults([]);
  };

  return (
    <Dialog.Root open={open} onOpenChange={setOpen}>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0" />
        <Dialog.Content className="fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] gap-4 border bg-background p-6 shadow-lg duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%] rounded-lg">
          <div className="flex flex-col space-y-4">
            <div className="flex items-center justify-between">
              <Dialog.Title className="text-lg font-semibold">Search</Dialog.Title>
              <Dialog.Close asChild>
                <Button variant="ghost" size="icon" className="h-6 w-6">
                  <X className="h-4 w-4" />
                  <span className="sr-only">Close</span>
                </Button>
              </Dialog.Close>
            </div>

            <div className="relative">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                type="text"
                placeholder="Search shipments, tracking numbers..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="pl-9 pr-4"
                autoFocus
              />
              <kbd className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground opacity-100">
                <span className="text-xs">⌘</span>K
              </kbd>
            </div>

            {isSearching && (
              <div className="flex items-center justify-center py-8">
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary"></div>
              </div>
            )}

            {!isSearching && query && results.length === 0 && (
              <div className="py-8 text-center text-sm text-muted-foreground">
                No results found for &quot;{query}&quot;
              </div>
            )}

            {!isSearching && results.length > 0 && (
              <div className="max-h-[300px] overflow-y-auto">
                <div className="space-y-1">
                  {results.map((shipment) => (
                    <button
                      key={shipment.id}
                      onClick={() => handleResultClick(shipment)}
                      className="w-full flex items-center gap-3 rounded-lg p-3 text-left hover:bg-accent transition-colors"
                    >
                      <div className="flex h-10 w-10 items-center justify-center rounded-md bg-primary/10">
                        <Package className="h-5 w-5 text-primary" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="text-sm font-medium truncate">
                          {shipment.tracking_number || shipment.id}
                        </div>
                        <div className="text-xs text-muted-foreground truncate">
                          {shipment.carrier} • {shipment.service}
                        </div>
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {!query && (
              <div className="py-8 text-center text-sm text-muted-foreground">
                Start typing to search shipments and tracking numbers
              </div>
            )}
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
