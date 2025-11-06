import QuickActionCard from '@/components/dashboard/QuickActionCard';
import StatsCard from '@/components/dashboard/StatsCard';
import { Badge } from '@/components/ui/Badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Skeleton, SkeletonCard, SkeletonStats, SkeletonText } from '@/components/ui/Skeleton';
import { formatRelativeTime } from '@/lib/utils';
import { shipmentAPI } from '@/services/api';
import { BarChart, CheckCircle, DollarSign, Package, Plus, Search, TruckIcon } from 'lucide-react';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'sonner';

// Quick Actions (static)
const quickActions = [
  {
    title: 'Create Shipment',
    description: 'Create a new shipping label',
    icon: Plus,
    color: 'primary',
    path: '/shipments',
  },
  {
    title: 'Track Package',
    description: 'Track your package in real-time',
    icon: Search,
    color: 'secondary',
    path: '/tracking',
  },
  {
    title: 'View Analytics',
    description: 'See insights and reports',
    icon: BarChart,
    color: 'accent',
    path: '/analytics',
  },
];

const statusColors = {
  pending: 'warning',
  in_transit: 'default',
  delivered: 'success',
};

export default function DashboardPage() {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(true);
  const [stats, setStats] = useState([]);
  const [recentActivity, setRecentActivity] = useState([]);
  const [carrierPerformance, setCarrierPerformance] = useState([]);

  // Fetch real data from API
  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setIsLoading(true);

        // Fetch stats, recent shipments, and carrier performance in parallel
        const [statsResponse, recentResponse, carrierResponse] = await Promise.all([
          shipmentAPI.getStats(),
          shipmentAPI.getRecentShipments(5),
          shipmentAPI.getCarrierPerformance(),
        ]);

        // Transform stats data - EasyPost API provides live snapshots only
        if (statsResponse.status === 'success' && statsResponse.data) {
          const statsData = statsResponse.data;
          setStats([
            {
              name: statsData.total_shipments?.label || 'Total Shipments',
              value: statsData.total_shipments?.value?.toLocaleString() || '0',
              note: statsData.total_shipments?.note || 'Last 100 from API',
              icon: Package,
            },
            {
              name: statsData.in_transit?.label || 'In Transit',
              value: statsData.in_transit?.value?.toLocaleString() || '0',
              note: statsData.in_transit?.note || 'Currently shipping',
              icon: TruckIcon,
            },
            {
              name: statsData.total_cost?.label || 'Total Spent',
              value: `$${statsData.total_cost?.value?.toFixed(2) || '0.00'}`,
              note: statsData.total_cost?.note || 'From shipment rates',
              icon: DollarSign,
            },
            {
              name: statsData.delivery_rate?.label || 'Delivery Rate',
              value: `${(statsData.delivery_rate?.value * 100)?.toFixed(1) || '0'}%`,
              note: statsData.delivery_rate?.note || 'Delivered / Total',
              icon: CheckCircle,
            },
          ]);
        }

        // Set carrier performance data
        if (carrierResponse.status === 'success' && carrierResponse.data) {
          setCarrierPerformance(carrierResponse.data);
        }

        // Transform recent shipments data
        if (recentResponse.status === 'success' && recentResponse.data) {
          const transformedActivity = recentResponse.data.map((shipment, index) => {
            // Extract destination city from to_address object
            let destination = 'Unknown';
            if (shipment.to_address?.city) {
              destination = shipment.to_address.state
                ? `${shipment.to_address.city}, ${shipment.to_address.state}`
                : shipment.to_address.city;
            } else if (shipment.to) {
              destination = shipment.to;
            }

            return {
              id: shipment.id || index + 1,
              type: 'shipment_created',
              tracking: shipment.tracking_number || 'N/A',
              message: `Shipment created to ${destination}`,
              timestamp: shipment.created_at || new Date().toISOString(),
              status: shipment.status || 'pending',
            };
          });
          setRecentActivity(transformedActivity);
        }
      } catch {
        toast.error('Failed to Load Dashboard', { description: 'Cannot connect to EasyPost API' });
        // Fallback to empty state if API fails
        setStats([
          {
            name: 'Total Shipments',
            value: '0',
            note: 'API connection failed',
            icon: Package,
          },
          {
            name: 'In Transit',
            value: '0',
            note: 'API connection failed',
            icon: TruckIcon,
          },
          {
            name: 'Total Spent',
            value: '$0.00',
            note: 'API connection failed',
            icon: DollarSign,
          },
          {
            name: 'Delivery Rate',
            value: '0%',
            note: 'API connection failed',
            icon: CheckCircle,
          },
        ]);

        // Empty state - no mock data to avoid confusion
        setRecentActivity([]);
        setCarrierPerformance([]);
      } finally {
        setIsLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (isLoading) {
    return (
      <div className="space-y-6 animate-fade-in">
        {/* Header Skeleton */}
        <div>
          <Skeleton className="h-9 w-48 mb-2" />
          <SkeletonText lines={1} className="w-96" />
        </div>

        {/* Stats Grid Skeleton */}
        <SkeletonStats count={4} />

        {/* Quick Actions Skeleton */}
        <div>
          <Skeleton className="h-6 w-32 mb-4" />
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {Array.from({ length: 3 }).map((_, i) => (
              <SkeletonCard key={i} />
            ))}
          </div>
        </div>

        <div className="grid gap-4 lg:grid-cols-2">
          {/* Recent Activity Skeleton */}
          <SkeletonCard />

          {/* Carrier Performance Skeleton */}
          <SkeletonCard />
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
        <p className="text-muted-foreground">
          Live snapshot from EasyPost API • Last 100 shipments • Historical trends require database
          storage
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat, index) => (
          <StatsCard key={stat.name} {...stat} delay={index * 0.1} />
        ))}
      </div>

      {/* Quick Actions */}
      <div>
        <h3 className="text-lg font-semibold mb-4">Quick Actions</h3>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {quickActions.map((action, index) => (
            <QuickActionCard
              key={action.title}
              {...action}
              delay={0.4 + index * 0.1}
              onClick={() => navigate(action.path)}
            />
          ))}
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        {/* Recent Activity */}
        <Card>
          <CardHeader>
            <CardTitle>Recent Activity</CardTitle>
            <CardDescription>Your latest shipment updates</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentActivity.map((activity) => (
                <div
                  key={activity.id}
                  className="flex items-start gap-4 pb-4 border-b border-border last:border-0 last:pb-0"
                >
                  <div className="rounded-full bg-primary/10 p-2">
                    <Package className="h-4 w-4 text-primary" />
                  </div>
                  <div className="flex-1 space-y-1">
                    <div className="flex items-center justify-between">
                      <p className="text-sm font-medium">{activity.message}</p>
                      <Badge variant={statusColors[activity.status]} className="text-xs">
                        {activity.status.replace('_', ' ')}
                      </Badge>
                    </div>
                    <div className="flex items-center gap-2 text-xs text-muted-foreground">
                      <span className="font-mono">{activity.tracking}</span>
                      <span>•</span>
                      <span>{formatRelativeTime(activity.timestamp)}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Carrier Usage */}
        <Card>
          <CardHeader>
            <CardTitle>Carrier Distribution</CardTitle>
            <CardDescription>Shipments by carrier (last 100)</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {carrierPerformance.length > 0 ? (
                carrierPerformance.map((item) => (
                  <div key={item.carrier} className="space-y-2">
                    <div className="flex items-center justify-between text-sm">
                      <span className="font-medium">{item.carrier}</span>
                      <span className="text-muted-foreground">
                        {item.shipments} total • {item.delivered || 0} delivered
                      </span>
                    </div>
                    <div className="relative h-2 rounded-full bg-muted overflow-hidden">
                      <div
                        className="absolute inset-y-0 left-0 bg-primary rounded-full transition-all"
                        style={{ width: `${item.rate}%` }}
                      />
                    </div>
                    <div className="text-right text-xs text-muted-foreground">
                      {item.rate}% delivery completion
                    </div>
                  </div>
                ))
              ) : (
                <p className="text-sm text-muted-foreground text-center py-4">
                  No carrier data available
                </p>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
