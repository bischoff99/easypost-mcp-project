import { useState, useEffect } from 'react';
import { Plus } from 'lucide-react';
import { toast } from 'sonner';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { SkeletonCard } from '@/components/ui/Skeleton';
import ShipmentTable from '@/components/shipments/ShipmentTable';
import ShipmentFilters from '@/components/shipments/ShipmentFilters';
import { shipmentAPI } from '@/services/api';

export default function ShipmentsPage() {
  const [filters, setFilters] = useState({});
  const [shipments, setShipments] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // Fetch real shipments data
  useEffect(() => {
    const fetchShipments = async () => {
      try {
        setIsLoading(true);

        // Fetch recent shipments from API
        const response = await shipmentAPI.getRecentShipments(50); // Get up to 50 shipments

        if (response.status === 'success' && response.data) {
          // Transform API data to match component expectations
          const transformedShipments = response.data.map((shipment, index) => ({
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

          setShipments(transformedShipments);
        } else {
          // Fallback to mock data if API fails
          toast.info('Using Demo Data', { description: 'Showing sample shipments for demonstration' });
          setShipments([
            {
              id: '1',
              tracking_number: 'EZ1234567890',
              status: 'in_transit',
              carrier: 'USPS',
              service: 'Priority Mail',
              from: 'San Francisco, CA',
              to: 'New York, NY',
              cost: 12.5,
              created_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
            },
            {
              id: '2',
              tracking_number: 'EZ9876543210',
              status: 'delivered',
              carrier: 'UPS',
              service: 'Ground',
              from: 'Austin, TX',
              to: 'Seattle, WA',
              cost: 18.75,
              created_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
            },
            {
              id: '3',
              tracking_number: 'EZ5555555555',
              status: 'pending',
              carrier: 'FedEx',
              service: 'Express',
              from: 'Miami, FL',
              to: 'Boston, MA',
              cost: 25.0,
              created_at: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString(),
            },
          ]);
        }
      } catch (error) {
        toast.error('Failed to Load Shipments', { description: 'Using demo data instead' });
        // Fallback to mock data
        setShipments([
          {
            id: '1',
            tracking_number: 'EZ1234567890',
            status: 'in_transit',
            carrier: 'USPS',
            service: 'Priority Mail',
            from: 'San Francisco, CA',
            to: 'New York, NY',
            cost: 12.5,
            created_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
          },
          {
            id: '2',
            tracking_number: 'EZ9876543210',
            status: 'delivered',
            carrier: 'UPS',
            service: 'Ground',
            from: 'Austin, TX',
            to: 'Seattle, WA',
            cost: 18.75,
            created_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
          },
          {
            id: '3',
            tracking_number: 'EZ5555555555',
            status: 'pending',
            carrier: 'FedEx',
            service: 'Express',
            from: 'Miami, FL',
            to: 'Boston, MA',
            cost: 25.0,
            created_at: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString(),
          },
        ]);
      } finally {
        setIsLoading(false);
      }
    };

    fetchShipments();
  }, []);

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
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
        <Button className="gap-2">
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
      <Card>
        <CardHeader>
          <CardTitle>All Shipments</CardTitle>
          <CardDescription>Complete history of your shipments</CardDescription>
        </CardHeader>
        <CardContent>
          <ShipmentTable shipments={shipments} isLoading={isLoading} />
        </CardContent>
      </Card>
    </div>
  );
}
