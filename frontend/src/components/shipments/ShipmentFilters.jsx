import { Search, Filter, X } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Badge } from '@/components/ui/Badge';

export default function ShipmentFilters({ filters, onFilterChange, onClearFilters }) {
  const activeFiltersCount = Object.values(filters || {}).filter(Boolean).length;

  return (
    <div className="space-y-4">
      {/* Search Bar */}
      <div className="flex gap-2">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search by tracking number, address..."
            className="pl-9"
            value={filters?.search || ''}
            onChange={(e) => onFilterChange?.('search', e.target.value)}
          />
        </div>
        <Button variant="outline" className="gap-2">
          <Filter className="h-4 w-4" />
          Filters
          {activeFiltersCount > 0 && (
            <Badge variant="secondary" className="ml-1 h-5 w-5 rounded-full p-0 text-xs">
              {activeFiltersCount}
            </Badge>
          )}
        </Button>
      </div>

      {/* Active Filters */}
      {activeFiltersCount > 0 && (
        <div className="flex flex-wrap gap-2 items-center">
          <span className="text-sm text-muted-foreground">Active filters:</span>
          {filters.search && (
            <Badge variant="secondary" className="gap-2">
              Search: {filters.search}
              <X
                className="h-3 w-3 cursor-pointer"
                onClick={() => onFilterChange?.('search', '')}
              />
            </Badge>
          )}
          {filters.carrier && (
            <Badge variant="secondary" className="gap-2">
              Carrier: {filters.carrier}
              <X
                className="h-3 w-3 cursor-pointer"
                onClick={() => onFilterChange?.('carrier', '')}
              />
            </Badge>
          )}
          {filters.status && (
            <Badge variant="secondary" className="gap-2">
              Status: {filters.status}
              <X
                className="h-3 w-3 cursor-pointer"
                onClick={() => onFilterChange?.('status', '')}
              />
            </Badge>
          )}
          <Button
            variant="ghost"
            size="sm"
            onClick={onClearFilters}
            className="h-7 text-xs"
          >
            Clear all
          </Button>
        </div>
      )}
    </div>
  );
}

