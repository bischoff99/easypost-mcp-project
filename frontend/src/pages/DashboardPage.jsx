import { Package, TruckIcon, DollarSign, CheckCircle } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';

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

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
        <p className="text-muted-foreground">
          Welcome back! Here's an overview of your shipping operations.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <Card key={stat.name}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{stat.name}</CardTitle>
              <stat.icon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className={`text-xs ${stat.trend === 'up' ? 'text-green-600' : 'text-red-600'}`}>
                {stat.change} from last month
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <Card className="hover:shadow-lg transition-shadow cursor-pointer">
          <CardHeader>
            <CardTitle>Create Shipment</CardTitle>
            <CardDescription>Create a new shipping label</CardDescription>
          </CardHeader>
        </Card>
        <Card className="hover:shadow-lg transition-shadow cursor-pointer">
          <CardHeader>
            <CardTitle>Track Package</CardTitle>
            <CardDescription>Track your package in real-time</CardDescription>
          </CardHeader>
        </Card>
        <Card className="hover:shadow-lg transition-shadow cursor-pointer">
          <CardHeader>
            <CardTitle>Compare Rates</CardTitle>
            <CardDescription>Compare carrier rates and services</CardDescription>
          </CardHeader>
        </Card>
      </div>

      {/* Recent Activity */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Activity</CardTitle>
          <CardDescription>Your latest shipment updates</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <p className="text-sm text-muted-foreground">No recent activity to display.</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

