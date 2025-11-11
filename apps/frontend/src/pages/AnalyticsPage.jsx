import { lazy, Suspense } from 'react';
import { Package, DollarSign, TrendingUp, Percent } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import ErrorBoundary from '@/components/ui/ErrorBoundary';
import MetricCard from '@/components/analytics/MetricCard';

// PERFORMANCE: Lazy load chart components (341KB recharts bundle)
// Only loads when user navigates to analytics page
const ShipmentVolumeChart = lazy(() => import('@/components/analytics/ShipmentVolumeChart'));
const CarrierDistributionChart = lazy(() => import('@/components/analytics/CarrierDistributionChart'));
const CostBreakdownChart = lazy(() => import('@/components/analytics/CostBreakdownChart'));

// Loading skeleton for charts
const ChartSkeleton = () => (
  <div className="flex items-center justify-center h-64 bg-muted/50 rounded-lg animate-pulse">
    <div className="text-sm text-muted-foreground">Loading chart...</div>
  </div>
);

const metrics = [
  {
    title: 'Total Shipments',
    value: '2,612',
    change: '+12.5%',
    trend: 'up',
    icon: Package,
    color: 'primary',
  },
  {
    title: 'Total Spending',
    value: '$43,025',
    change: '+8.2%',
    trend: 'up',
    icon: DollarSign,
    color: 'success',
  },
  {
    title: 'Average Cost',
    value: '$16.47',
    change: '-3.1%',
    trend: 'down',
    icon: TrendingUp,
    color: 'warning',
  },
  {
    title: 'Success Rate',
    value: '94.3%',
    change: '+2.4%',
    trend: 'up',
    icon: Percent,
    color: 'secondary',
  },
];

const topDestinations = [
  { city: 'New York, NY', shipments: 342, percentage: 13 },
  { city: 'Los Angeles, CA', shipments: 298, percentage: 11 },
  { city: 'Chicago, IL', shipments: 276, percentage: 11 },
  { city: 'Houston, TX', shipments: 245, percentage: 9 },
  { city: 'Phoenix, AZ', shipments: 198, percentage: 8 },
];

function AnalyticsPageContent() {
  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Analytics</h2>
          <p className="text-muted-foreground">
            Insights and analytics for your shipping operations
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">Last 7 Days</Button>
          <Button variant="outline">Last 30 Days</Button>
          <Button variant="default">Last 90 Days</Button>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {metrics.map((metric, index) => (
          <MetricCard key={metric.title} {...metric} delay={index * 0.1} />
        ))}
      </div>

      {/* Charts Row 1 */}
      <div className="grid gap-4 lg:grid-cols-2">
        <Suspense fallback={<ChartSkeleton />}>
          <ShipmentVolumeChart />
        </Suspense>
        <Suspense fallback={<ChartSkeleton />}>
          <CarrierDistributionChart />
        </Suspense>
      </div>

      {/* Charts Row 2 */}
      <div className="grid gap-4 lg:grid-cols-3">
        <Suspense fallback={<ChartSkeleton />}>
          <CostBreakdownChart />
        </Suspense>

        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Top Destinations</CardTitle>
            <CardDescription>Most common shipping destinations</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {topDestinations.map((dest, index) => (
                <div key={dest.city} className="flex items-center gap-4">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10 text-primary font-bold">
                    {index + 1}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-medium">{dest.city}</span>
                      <span className="text-sm text-muted-foreground">
                        {dest.shipments} shipments
                      </span>
                    </div>
                    <div className="relative h-2 rounded-full bg-muted overflow-hidden">
                      <div
                        className="absolute inset-y-0 left-0 bg-primary rounded-full transition-all"
                        style={{ width: `${dest.percentage * 7.7}%` }}
                      />
                    </div>
                  </div>
                  <div className="text-sm font-medium text-muted-foreground w-12 text-right">
                    {dest.percentage}%
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Performance Summary */}
      <Card>
        <CardHeader>
          <CardTitle>Performance Summary</CardTitle>
          <CardDescription>Key performance indicators</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="space-y-2">
              <p className="text-sm font-medium text-muted-foreground">Average Delivery Time</p>
              <p className="text-2xl font-bold">2.8 days</p>
              <p className="text-xs text-green-600">↓ 0.3 days faster</p>
            </div>
            <div className="space-y-2">
              <p className="text-sm font-medium text-muted-foreground">On-Time Delivery</p>
              <p className="text-2xl font-bold">94.3%</p>
              <p className="text-xs text-green-600">↑ 2.4% improvement</p>
            </div>
            <div className="space-y-2">
              <p className="text-sm font-medium text-muted-foreground">Exception Rate</p>
              <p className="text-2xl font-bold">2.1%</p>
              <p className="text-xs text-red-600">↑ 0.3% increase</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default function AnalyticsPage() {
  return (
    <ErrorBoundary>
      <AnalyticsPageContent />
    </ErrorBoundary>
  );
}
