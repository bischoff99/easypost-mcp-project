import { useState } from 'react';
import { Plus } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import ShipmentTable from '@/components/shipments/ShipmentTable';
import ShipmentFilters from '@/components/shipments/ShipmentFilters';

export default function ShipmentsPage() {
  const [filters, setFilters] = useState({});

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
          <p className="text-muted-foreground">
            View and manage all your shipments
          </p>
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
          <ShipmentTable />
        </CardContent>
      </Card>
    </div>
  );
}
