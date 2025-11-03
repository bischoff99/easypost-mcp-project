import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';

export default function ShipmentsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Shipments</h2>
        <p className="text-muted-foreground">
          View and manage all your shipments
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Shipment History</CardTitle>
          <CardDescription>All shipments and their current status</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">Shipment table coming soon...</p>
        </CardContent>
      </Card>
    </div>
  );
}

