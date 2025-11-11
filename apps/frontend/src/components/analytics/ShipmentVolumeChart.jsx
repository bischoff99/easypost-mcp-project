import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';

const data = [
  { date: 'Jan 1', shipments: 45, cost: 560 },
  { date: 'Jan 8', shipments: 52, cost: 648 },
  { date: 'Jan 15', shipments: 61, cost: 762 },
  { date: 'Jan 22', shipments: 58, cost: 725 },
  { date: 'Jan 29', shipments: 67, cost: 835 },
  { date: 'Feb 5', shipments: 73, cost: 912 },
  { date: 'Feb 12', shipments: 69, cost: 863 },
  { date: 'Feb 19', shipments: 78, cost: 975 },
  { date: 'Feb 26', shipments: 85, cost: 1062 },
  { date: 'Mar 5', shipments: 92, cost: 1150 },
];

export default function ShipmentVolumeChart() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Shipment Volume</CardTitle>
        <CardDescription>Weekly shipment and cost trends</CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
            <XAxis
              dataKey="date"
              className="text-xs"
              tick={{ fill: 'hsl(var(--muted-foreground))' }}
            />
            <YAxis className="text-xs" tick={{ fill: 'hsl(var(--muted-foreground))' }} />
            <Tooltip
              contentStyle={{
                backgroundColor: 'hsl(var(--card))',
                border: '1px solid hsl(var(--border))',
                borderRadius: '8px',
              }}
            />
            <Legend />
            <Line
              type="monotone"
              dataKey="shipments"
              stroke="hsl(var(--primary))"
              strokeWidth={2}
              dot={{ fill: 'hsl(var(--primary))' }}
              activeDot={{ r: 6 }}
            />
            <Line
              type="monotone"
              dataKey="cost"
              stroke="hsl(var(--destructive))"
              strokeWidth={2}
              dot={{ fill: 'hsl(var(--destructive))' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
