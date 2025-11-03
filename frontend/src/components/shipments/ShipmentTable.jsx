import { useState } from 'react';
import {
  Package,
  TruckIcon,
  CheckCircle,
  Clock,
  AlertTriangle,
  ExternalLink,
  Printer,
  X,
  Download,
} from 'lucide-react';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/Table';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { SkeletonTable } from '@/components/ui/Skeleton';
import { exportShipmentsToCSV, exportSelectedShipmentsToCSV } from '@/lib/exportUtils';
import { formatDate, formatCurrency, formatRelativeTime } from '@/lib/utils';

const statusConfig = {
  delivered: {
    variant: 'success',
    icon: CheckCircle,
    label: 'Delivered',
  },
  in_transit: {
    variant: 'default',
    icon: TruckIcon,
    label: 'In Transit',
  },
  pending: {
    variant: 'warning',
    icon: Clock,
    label: 'Pending',
  },
  exception: {
    variant: 'destructive',
    icon: AlertTriangle,
    label: 'Exception',
  },
};

// Mock data for demonstration
const mockShipments = [
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
    label_url: '#',
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
    label_url: '#',
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
    label_url: '#',
  },
];

export default function ShipmentTable({ shipments: propShipments, isLoading = false }) {
  // Use prop shipments if provided, otherwise fallback to mock data
  const shipments = propShipments || mockShipments;
  const [selectedRows, setSelectedRows] = useState(new Set());

  if (isLoading) {
    return <SkeletonTable rows={5} columns={8} />;
  }

  const handleExportAll = () => {
    exportShipmentsToCSV(shipments, `all-shipments-${new Date().toISOString().split('T')[0]}`);
  };

  const handleExportSelected = () => {
    if (selectedRows.size === 0) return;
    exportSelectedShipmentsToCSV(
      shipments,
      selectedRows,
      `selected-shipments-${new Date().toISOString().split('T')[0]}`
    );
  };

  const toggleRow = id => {
    const newSelected = new Set(selectedRows);
    if (newSelected.has(id)) {
      newSelected.delete(id);
    } else {
      newSelected.add(id);
    }
    setSelectedRows(newSelected);
  };

  const toggleAll = () => {
    if (selectedRows.size === shipments.length) {
      setSelectedRows(new Set());
    } else {
      setSelectedRows(new Set(shipments.map(s => s.id)));
    }
  };

  return (
    <div className="space-y-4">
      {selectedRows.size > 0 && (
        <div className="flex items-center gap-2 rounded-lg border border-border bg-muted/50 px-4 py-2">
          <span className="text-sm font-medium">{selectedRows.size} selected</span>
          <div className="flex gap-1 ml-4">
            <Button variant="outline" size="sm">
              <Printer className="h-4 w-4 mr-1" />
              Print Labels
            </Button>
            <Button variant="outline" size="sm" onClick={handleExportSelected}>
              <Download className="h-4 w-4 mr-1" />
              Export Selected
            </Button>
            <Button variant="outline" size="sm">
              <X className="h-4 w-4 mr-1" />
              Void
            </Button>
          </div>
        </div>
      )}

      <div className="rounded-lg border border-border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="w-12">
                <input
                  type="checkbox"
                  checked={selectedRows.size === shipments.length}
                  onChange={toggleAll}
                  className="rounded border-input"
                />
              </TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Tracking Number</TableHead>
              <TableHead>Route</TableHead>
              <TableHead>Carrier</TableHead>
              <TableHead>Service</TableHead>
              <TableHead>Cost</TableHead>
              <TableHead>Date</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {shipments.map(shipment => {
              const statusInfo = statusConfig[shipment.status] || statusConfig.pending;
              const StatusIcon = statusInfo.icon;

              return (
                <TableRow
                  key={shipment.id}
                  data-state={selectedRows.has(shipment.id) ? 'selected' : undefined}
                >
                  <TableCell>
                    <input
                      type="checkbox"
                      checked={selectedRows.has(shipment.id)}
                      onChange={() => toggleRow(shipment.id)}
                      className="rounded border-input"
                    />
                  </TableCell>
                  <TableCell>
                    <Badge variant={statusInfo.variant} className="gap-1">
                      <StatusIcon className="h-3 w-3" />
                      {statusInfo.label}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-sm">{shipment.tracking_number}</span>
                      <Button variant="ghost" size="icon" className="h-6 w-6">
                        <ExternalLink className="h-3 w-3" />
                      </Button>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1 text-sm">
                      <span className="text-muted-foreground">{shipment.from}</span>
                      <span>→</span>
                      <span className="font-medium">{shipment.to}</span>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <Package className="h-4 w-4 text-muted-foreground" />
                      <span className="font-medium">{shipment.carrier}</span>
                    </div>
                  </TableCell>
                  <TableCell>
                    <span className="text-sm text-muted-foreground">{shipment.service}</span>
                  </TableCell>
                  <TableCell>
                    <span className="font-medium">{formatCurrency(shipment.cost)}</span>
                  </TableCell>
                  <TableCell>
                    <div className="flex flex-col">
                      <span className="text-sm">{formatDate(shipment.created_at)}</span>
                      <span className="text-xs text-muted-foreground">
                        {formatRelativeTime(shipment.created_at)}
                      </span>
                    </div>
                  </TableCell>
                  <TableCell className="text-right">
                    <div className="flex justify-end gap-1">
                      <Button variant="ghost" size="sm">
                        Track
                      </Button>
                      <Button variant="ghost" size="sm">
                        <Printer className="h-4 w-4" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </div>

      {/* Export and Pagination */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="text-sm text-muted-foreground">
            Showing <span className="font-medium">{shipments.length}</span> of{' '}
            <span className="font-medium">{shipments.length}</span> shipments
          </div>
          <Button variant="outline" size="sm" onClick={handleExportAll}>
            <Download className="h-4 w-4 mr-1" />
            Export All
          </Button>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" disabled>
            Previous
          </Button>
          <Button variant="outline" size="sm" disabled>
            Next
          </Button>
        </div>
      </div>
    </div>
  );
}
