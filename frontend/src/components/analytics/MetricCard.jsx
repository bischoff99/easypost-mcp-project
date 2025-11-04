import { motion } from 'framer-motion';
import { TrendingUp, TrendingDown } from 'lucide-react';
import PropTypes from 'prop-types';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { cn } from '@/lib/utils';

export default function MetricCard({ title, value, change, trend, icon: Icon, color = 'primary', delay = 0 }) {
  const isPositive = trend === 'up';

  const colorClasses = {
    primary: 'text-primary',
    secondary: 'text-secondary',
    success: 'text-green-600',
    warning: 'text-yellow-600',
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3, delay }}
    >
      <Card className="relative overflow-hidden">
        <div className={cn('absolute top-0 right-0 w-32 h-32 opacity-10', colorClasses[color])}>
          <Icon className="w-full h-full" />
        </div>
        <CardHeader className="relative">
          <div className="flex items-center justify-between">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              {title}
            </CardTitle>
            <Icon className={cn('h-5 w-5', colorClasses[color])} />
          </div>
        </CardHeader>
        <CardContent className="relative">
          <div className="text-3xl font-bold">{value}</div>
          <div className="flex items-center gap-1 mt-2">
            {isPositive ? (
              <TrendingUp className="h-4 w-4 text-green-600" />
            ) : (
              <TrendingDown className="h-4 w-4 text-red-600" />
            )}
            <span
              className={cn(
                'text-sm font-medium',
                isPositive ? 'text-green-600' : 'text-red-600'
              )}
            >
              {change}
            </span>
            <span className="text-sm text-muted-foreground">vs last period</span>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}

MetricCard.propTypes = {
  title: PropTypes.string.isRequired,
  value: PropTypes.string.isRequired,
  change: PropTypes.string.isRequired,
  trend: PropTypes.oneOf(['up', 'down']).isRequired,
  icon: PropTypes.elementType.isRequired,
  color: PropTypes.oneOf(['primary', 'secondary', 'success', 'warning']),
  delay: PropTypes.number,
};
