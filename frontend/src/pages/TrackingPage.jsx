import { useState } from 'react';
import { Search, Package, MapPin, CheckCircle, Clock, TruckIcon } from 'lucide-react';
import { toast } from 'sonner';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { formatDate } from '@/lib/utils';
import { shipmentAPI } from '@/services/api';

const mockTrackingData = {
  tracking_number: 'EZ1234567890',
  status: 'in_transit',
  carrier: 'USPS',
  service: 'Priority Mail',
  est_delivery: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000).toISOString(),
  from: { city: 'San Francisco', state: 'CA', zip: '94102' },
  to: { city: 'New York', state: 'NY', zip: '10001' },
  events: [
    {
      status: 'out_for_delivery',
      message: 'Out for delivery',
      location: 'New York, NY 10001',
      timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
    },
    {
      status: 'in_transit',
      message: 'Arrived at distribution center',
      location: 'Newark, NJ 07102',
      timestamp: new Date(Date.now() - 12 * 60 * 60 * 1000).toISOString(),
    },
    {
      status: 'in_transit',
      message: 'In transit',
      location: 'Philadelphia, PA 19019',
      timestamp: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
    },
    {
      status: 'accepted',
      message: 'Shipment accepted',
      location: 'San Francisco, CA 94102',
      timestamp: new Date(Date.now() - 48 * 60 * 60 * 1000).toISOString(),
    },
  ],
};

const statusIcons = {
  accepted: Clock,
  in_transit: TruckIcon,
  out_for_delivery: Package,
  delivered: CheckCircle,
};

export default function TrackingPage() {
  const [trackingNumber, setTrackingNumber] = useState('');
  const [trackingData, setTrackingData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleTrack = async () => {
    if (!trackingNumber.trim()) {
      toast.error('Please enter a tracking number');
      return;
    }

    setLoading(true);
    try {
      // Call real tracking API
      const response = await shipmentAPI.getTracking(trackingNumber.trim());

      if (response.status === 'success' && response.data) {
        setTrackingData(response.data);
        toast.success('Tracking information retrieved');
      } else {
        // Fallback to mock data for demo
        toast.info('Using Demo Data', { description: 'Showing sample tracking for demonstration' });
        setTrackingData(mockTrackingData);
      }
    } catch (error) {
      // Log error in development only
      if (import.meta.env.DEV) {
        console.error('Tracking error:', error);
      }
      toast.info('Using Demo Data', { description: 'Showing sample tracking for demonstration' });
      setTrackingData(mockTrackingData);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Track Package</h2>
        <p className="text-muted-foreground">Track your shipments in real-time</p>
      </div>

      {/* Search */}
      <Card>
        <CardHeader>
          <CardTitle>Enter Tracking Number</CardTitle>
          <CardDescription>Track your package by entering the tracking number</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex gap-2">
            <Input
              placeholder="Enter tracking number (e.g., EZ1234567890)"
              value={trackingNumber}
              onChange={(e) => setTrackingNumber(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleTrack()}
            />
            <Button onClick={handleTrack} disabled={!trackingNumber || loading}>
              <Search className="h-4 w-4 mr-2" />
              {loading ? 'Tracking...' : 'Track'}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Tracking Results */}
      {trackingData && (
        <>
          {/* Status Overview */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="flex items-center gap-2">
                    <Package className="h-5 w-5" />
                    {trackingData.tracking_number}
                  </CardTitle>
                  <CardDescription className="mt-1">
                    {trackingData.carrier} - {trackingData.service}
                  </CardDescription>
                </div>
                <Badge variant="default" className="text-sm">
                  In Transit
                </Badge>
              </div>
            </CardHeader>
            <CardContent>
              <div className="grid gap-6 md:grid-cols-3">
                <div className="space-y-1">
                  <p className="text-sm font-medium text-muted-foreground">Origin</p>
                  <div className="flex items-start gap-2">
                    <MapPin className="h-4 w-4 mt-1 text-muted-foreground" />
                    <div>
                      <p className="font-medium">
                        {trackingData.from.city}, {trackingData.from.state}
                      </p>
                      <p className="text-sm text-muted-foreground">{trackingData.from.zip}</p>
                    </div>
                  </div>
                </div>
                <div className="space-y-1">
                  <p className="text-sm font-medium text-muted-foreground">Destination</p>
                  <div className="flex items-start gap-2">
                    <MapPin className="h-4 w-4 mt-1 text-muted-foreground" />
                    <div>
                      <p className="font-medium">
                        {trackingData.to.city}, {trackingData.to.state}
                      </p>
                      <p className="text-sm text-muted-foreground">{trackingData.to.zip}</p>
                    </div>
                  </div>
                </div>
                <div className="space-y-1">
                  <p className="text-sm font-medium text-muted-foreground">Est. Delivery</p>
                  <p className="font-medium">{formatDate(trackingData.est_delivery)}</p>
                  <p className="text-sm text-muted-foreground">By end of day</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Tracking Timeline */}
          <Card>
            <CardHeader>
              <CardTitle>Tracking History</CardTitle>
              <CardDescription>Detailed shipment journey</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="relative space-y-6">
                {/* Timeline line */}
                <div className="absolute left-6 top-2 bottom-2 w-0.5 bg-border" />

                {trackingData.events.map((event, index) => {
                  const Icon = statusIcons[event.status] || Package;
                  const isFirst = index === 0;

                  return (
                    <div key={index} className="relative flex gap-4">
                      <div
                        className={`relative z-10 flex h-12 w-12 items-center justify-center rounded-full border-2 ${
                          isFirst
                            ? 'border-primary bg-primary text-primary-foreground'
                            : 'border-border bg-background'
                        }`}
                      >
                        <Icon className="h-5 w-5" />
                      </div>
                      <div className="flex-1 pt-1">
                        <div className="flex items-start justify-between">
                          <div>
                            <p className={`font-medium ${isFirst ? 'text-primary' : ''}`}>
                              {event.message}
                            </p>
                            <p className="text-sm text-muted-foreground mt-1">{event.location}</p>
                          </div>
                          <div className="text-right">
                            <p className="text-sm font-medium">{formatDate(event.timestamp)}</p>
                            <p className="text-xs text-muted-foreground">
                              {new Date(event.timestamp).toLocaleTimeString()}
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        </>
      )}

      {/* Empty State */}
      {!trackingData && !loading && (
        <Card className="border-dashed">
          <CardContent className="flex flex-col items-center justify-center py-12">
            <Package className="h-12 w-12 text-muted-foreground mb-4" />
            <p className="text-lg font-medium">No tracking data</p>
            <p className="text-sm text-muted-foreground">Enter a tracking number to get started</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
