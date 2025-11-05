import { motion } from 'framer-motion';
import { TrendingUp, TrendingDown } from 'lucide-react';
import PropTypes from 'prop-types';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { cn } from '@/lib/utils';

export default function StatsCard({ title, name, value, note, change, trend, icon: Icon, delay = 0 }) {
  // Support both 'title' and 'name' props for compatibility
  const displayTitle = title || name;
  const isPositive = trend === 'up';
  const showTrend = change && trend;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay }}
    >
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
                className={cn('text-xs font-medium', isPositive ? 'text-green-600' : 'text-red-600')}
              >
                {change} from last month
              </p>
            </div>
          ) : note ? (
            <p className="text-xs text-muted-foreground mt-1">{note}</p>
          ) : null}
        </CardContent>
      </Card>
    </motion.div>
  );
}

StatsCard.propTypes = {
  title: PropTypes.string,  // Optional, falls back to name
  name: PropTypes.string,  // Alternative to title
  value: PropTypes.string.isRequired,
  note: PropTypes.string,  // Optional note instead of trend
  change: PropTypes.string,  // Optional change percentage
  trend: PropTypes.oneOf(['up', 'down']),  // Optional trend
  icon: PropTypes.elementType.isRequired,
  delay: PropTypes.number,
};
