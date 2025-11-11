import { useState } from 'react';
import { Search, Package, MapPin, CheckCircle, Clock, TruckIcon } from 'lucide-react';
import { toast } from 'sonner';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import ErrorBoundary from '@/components/ui/ErrorBoundary';
import { formatDate } from '@/lib/utils';
import { shipmentAPI } from '@/services/api';
import { useQuery } from '@tanstack/react-query';

const statusIcons = {
  accepted: Clock,
  in_transit: TruckIcon,
  out_for_delivery: Package,
  delivered: CheckCircle,
};

function TrackingPageContent() {
  const [trackingNumber, setTrackingNumber] = useState('');

  // Fetch tracking data using React Query
  const {
    data: trackingData,
    isLoading,
    error: _error,
    refetch,
  } = useQuery({
    queryKey: ['tracking', trackingNumber],
    queryFn: async () => {
      if (!trackingNumber.trim()) {
        return null;
      }
      const response = await shipmentAPI.getTracking(trackingNumber.trim());
      if (response.status === 'success' && response.data) {
        return response.data;
      }
      throw new Error(response.message || 'Failed to fetch tracking information');
    },
    enabled: false, // Only fetch when manually triggered
    retry: false,
  });

  const handleTrack = () => {
    if (!trackingNumber.trim()) {
      toast.error('Please enter a tracking number');
      return;
    }
    refetch();
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
          <CardDescription id="tracking-description">Track your package by entering the tracking number</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex gap-2">
            <Input
              placeholder="Enter tracking number (e.g., EZ1234567890)"
              value={trackingNumber}
              onChange={(e) => setTrackingNumber(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleTrack()}
              aria-label="Tracking number input"
              aria-describedby="tracking-description"
            />
            <Button onClick={handleTrack} disabled={!trackingNumber.trim() || isLoading} aria-label="Track shipment">
              <Search className="h-4 w-4 mr-2" />
              {isLoading ? 'Tracking...' : 'Track'}
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
      {!trackingData && !isLoading && (
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

export default function TrackingPage() {
  return (
    <ErrorBoundary>
      <TrackingPageContent />
    </ErrorBoundary>
  );
}
