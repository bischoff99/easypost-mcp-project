import { Package, TruckIcon, DollarSign, CheckCircle, Plus, Search, BarChart } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import StatsCard from '@/components/dashboard/StatsCard';
import QuickActionCard from '@/components/dashboard/QuickActionCard';
import { formatRelativeTime } from '@/lib/utils';

const stats = [
  {
    name: 'Total Shipments',
    value: '2,456',
    change: '+12.5%',
    trend: 'up',
    icon: Package,
  },
  {
    name: 'Active Deliveries',
    value: '145',
    change: '-2.3%',
    trend: 'down',
    icon: TruckIcon,
  },
  {
    name: 'Total Cost',
    value: '$12,458',
    change: '+8.1%',
    trend: 'up',
    icon: DollarSign,
  },
  {
    name: 'On-Time Rate',
    value: '94.2%',
    change: '+1.2%',
    trend: 'up',
    icon: CheckCircle,
  },
];

const quickActions = [
  {
    title: 'Create Shipment',
    description: 'Create a new shipping label',
    icon: Plus,
    color: 'primary',
  },
  {
    title: 'Track Package',
    description: 'Track your package in real-time',
    icon: Search,
    color: 'secondary',
  },
  {
    title: 'View Analytics',
    description: 'See insights and reports',
    icon: BarChart,
    color: 'accent',
  },
];

const recentActivity = [
  {
    id: 1,
    type: 'shipment_created',
    tracking: 'EZ1234567890',
    message: 'New shipment created to New York, NY',
    timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
    status: 'pending',
  },
  {
    id: 2,
    type: 'shipment_delivered',
    tracking: 'EZ9876543210',
    message: 'Shipment delivered to Seattle, WA',
    timestamp: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
    status: 'delivered',
  },
  {
    id: 3,
    type: 'shipment_in_transit',
    tracking: 'EZ5555555555',
    message: 'Shipment in transit to Boston, MA',
    timestamp: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
    status: 'in_transit',
  },
];

const statusColors = {
  pending: 'warning',
  in_transit: 'default',
  delivered: 'success',
};

export default function DashboardPage() {
  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
        <p className="text-muted-foreground">
          Welcome back! Here's an overview of your shipping operations.
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
              onClick={() => {
                // TODO: Implement navigation based on action
              }}
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

        {/* Carrier Performance */}
        <Card>
          <CardHeader>
            <CardTitle>Carrier Performance</CardTitle>
            <CardDescription>Delivery success rates</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { carrier: 'USPS', rate: 96, shipments: 1205 },
                { carrier: 'UPS', rate: 94, shipments: 842 },
                { carrier: 'FedEx', rate: 92, shipments: 409 },
              ].map((item) => (
                <div key={item.carrier} className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span className="font-medium">{item.carrier}</span>
                    <span className="text-muted-foreground">
                      {item.shipments} shipments
                    </span>
                  </div>
                  <div className="relative h-2 rounded-full bg-muted overflow-hidden">
                    <div
                      className="absolute inset-y-0 left-0 bg-primary rounded-full transition-all"
                      style={{ width: `${item.rate}%` }}
                    />
                  </div>
                  <div className="text-right text-xs text-muted-foreground">
                    {item.rate}% on-time
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
