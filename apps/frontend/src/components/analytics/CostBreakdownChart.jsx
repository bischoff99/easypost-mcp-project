import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card'

const data = [
  { name: 'USPS', value: 15062, percentage: 35 },
  { name: 'UPS', value: 13468, percentage: 31 },
  { name: 'FedEx', value: 9815, percentage: 23 },
  { name: 'DHL', value: 4680, percentage: 11 },
]

const COLORS = [
  'hsl(var(--primary))',
  'hsl(221.2 83.2% 63.3%)',
  'hsl(221.2 83.2% 73.3%)',
  'hsl(var(--muted))',
]

export default function CostBreakdownChart() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Cost Breakdown</CardTitle>
        <CardDescription>Spending by carrier</CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300} debounce={300}>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percentage }) => `${name} ${percentage}%`}
              outerRadius={100}
              fill="#8884d8"
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{
                backgroundColor: 'hsl(var(--card))',
                border: '1px solid hsl(var(--border))',
                borderRadius: '8px',
              }}
              formatter={(value) => `$${value.toLocaleString()}`}
            />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
