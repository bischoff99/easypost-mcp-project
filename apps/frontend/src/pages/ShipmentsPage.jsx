import { useState } from 'react';
import { Plus, Package, ArrowRight } from 'lucide-react';
import { toast } from 'sonner';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import DataTable from '@/components/ui/DataTable';
import EmptyState from '@/components/ui/EmptyState';
import ShipmentFilters from '@/components/shipments/ShipmentFilters';
import ErrorBoundary from '@/components/ui/ErrorBoundary';
import { shipmentAPI } from '@/services/api';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { Skeleton, SkeletonCard } from '@/components/ui/Skeleton';

function ShipmentsPageContent() {
  const navigate = useNavigate();
  const [filters, setFilters] = useState({});

  // Fetch shipments using React Query
  const {
    data: shipments = [],
    isLoading,
    error,
  } = useQuery({
    queryKey: ['shipments', 'recent', filters],
    queryFn: async () => {
      const response = await shipmentAPI.getRecentShipments(50);
      if (response.status === 'success' && response.data) {
        return response.data.map((shipment, index) => ({
          id: shipment.id || `shipment-${index + 1}`,
          tracking_number: shipment.tracking_number || '',
          status: shipment.status || 'pending',
          carrier: shipment.carrier || 'Unknown',
          service: shipment.service || 'Standard',
          from: shipment.from || 'Unknown',
          to: shipment.to || 'Unknown',
          cost: parseFloat(shipment.rate || '0'),
          created_at: shipment.created_at || new Date().toISOString(),
        }));
      }
      throw new Error(response.message || 'Failed to fetch shipments');
    },
    staleTime: 30000, // 30 seconds
  });

  // Show loading skeleton
  if (isLoading) {
    return (
      <div className="space-y-6 animate-fade-in">
        <div>
          <Skeleton className="h-9 w-48 mb-2" />
          <Skeleton className="h-5 w-96" />
        </div>
        <div className="grid gap-4">
          {Array.from({ length: 5 }).map((_, i) => (
            <SkeletonCard key={i} />
          ))}
        </div>
      </div>
    );
  }

  // Handle error
  if (error) {
    toast.error('Failed to load shipments', {
      description: error.message || 'Unable to fetch shipments data',
    });
  }

  const handleFilterChange = (key, value) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  const handleClearFilters = () => {
    setFilters({});
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Shipments</h2>
          <p className="text-muted-foreground">View and manage all your shipments</p>
        </div>
        <Button className="gap-2" onClick={() => navigate('/shipments/new')} aria-label="Create new shipment">
          <Plus className="h-4 w-4" />
          New Shipment
        </Button>
      </div>

      {/* Filters */}
      <Card>
        <CardHeader>
          <CardTitle>Search & Filter</CardTitle>
          <CardDescription>Find shipments quickly</CardDescription>
        </CardHeader>
        <CardContent>
          <ShipmentFilters
            filters={filters}
            onFilterChange={handleFilterChange}
            onClearFilters={handleClearFilters}
          />
        </CardContent>
      </Card>

      {/* Table */}
      {shipments.length === 0 && !isLoading ? (
        <Card>
          <CardContent className="pt-6">
            <EmptyState
              icon={Package}
              title="No shipments yet"
              description="Get started by creating your first shipment. Track packages, manage deliveries, and streamline your shipping process."
              action={() => navigate('/shipments/new')}
              actionLabel="Create Shipment"
              secondaryAction={() => navigate('/tracking')}
              secondaryActionLabel="Track Existing"
            />
          </CardContent>
        </Card>
      ) : (
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>All Shipments</CardTitle>
                <CardDescription>Complete history of your shipments</CardDescription>
              </div>
              <Badge variant="secondary">{shipments.length} total</Badge>
            </div>
          </CardHeader>
          <CardContent>
            <DataTable
              columns={[
                {
                  key: 'tracking_number',
                  header: 'Tracking Number',
                  render: (row) => (
                    <span className="font-mono text-sm">{row.tracking_number}</span>
                  ),
                },
                {
                  key: 'status',
                  header: 'Status',
                  render: (row) => {
                    const statusColors = {
                      pending: 'bg-yellow-500/10 text-yellow-700 dark:text-yellow-400',
                      in_transit: 'bg-blue-500/10 text-blue-700 dark:text-blue-400',
                      delivered: 'bg-green-500/10 text-green-700 dark:text-green-400',
                      cancelled: 'bg-red-500/10 text-red-700 dark:text-red-400',
                    };
                    return (
                      <Badge className={statusColors[row.status] || statusColors.pending}>
                        {row.status.replace('_', ' ')}
                      </Badge>
                    );
                  },
                },
                {
                  key: 'carrier',
                  header: 'Carrier',
                },
                {
                  key: 'service',
                  header: 'Service',
                },
                {
                  key: 'from',
                  header: 'Origin',
                },
                {
                  key: 'to',
                  header: 'Destination',
                },
                {
                  key: 'cost',
                  header: 'Cost',
                  render: (row) => `$${row.cost.toFixed(2)}`,
                },
                {
                  key: 'created_at',
                  header: 'Created',
                  render: (row) => new Date(row.created_at).toLocaleDateString(),
                },
                {
                  key: 'actions',
                  header: '',
                  sortable: false,
                  render: (row) => (
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={(e) => {
                        e.stopPropagation();
                        navigate(`/tracking?number=${row.tracking_number}`);
                      }}
                    >
                      Track <ArrowRight className="ml-1 h-3 w-3" />
                    </Button>
                  ),
                },
              ]}
              data={shipments}
              onRowClick={(row) => navigate(`/tracking?number=${row.tracking_number}`)}
              isLoading={isLoading}
              emptyMessage="No shipments match your filters"
              searchPlaceholder="Search by tracking number, carrier, origin..."
              pageSize={10}
            />
          </CardContent>
        </Card>
      )}
    </div>
  );
}

export default function ShipmentsPage() {
  return (
    <ErrorBoundary>
      <ShipmentsPageContent />
    </ErrorBoundary>
  );
}
