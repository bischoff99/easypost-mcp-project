import { TrendingUp, TrendingDown } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { cn } from '@/lib/utils'

export default function StatsCard({
  title,
  name,
  value,
  note,
  change,
  trend,
  icon: Icon,
  delay = 0,
}) {
  // Support both 'title' and 'name' props for compatibility
  const displayTitle = title || name
  const isPositive = trend === 'up'
  const showTrend = change && trend

  return (
    <div>
      <Card className="hover:shadow-lg transition-shadow">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">{displayTitle}</CardTitle>
          <Icon className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{value}</div>
          {showTrend ? (
            <div className="flex items-center gap-1 mt-1">
              {isPositive ? (
                <TrendingUp className="h-4 w-4 text-green-600" />
              ) : (
                <TrendingDown className="h-4 w-4 text-red-600" />
              )}
              <p
                className={cn(
                  'text-xs font-medium',
                  isPositive ? 'text-green-600' : 'text-red-600'
                )}
              >
                {change} from last month
              </p>
            </div>
          ) : note ? (
            <p className="text-xs text-muted-foreground mt-1">{note}</p>
          ) : null}
        </CardContent>
      </Card>
    </div>
  )
}
