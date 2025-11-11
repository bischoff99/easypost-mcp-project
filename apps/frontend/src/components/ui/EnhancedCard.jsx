import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './Card';
import { cn } from '@/lib/utils';

/**
 * EnhancedCard Component
 *
 * Card with hover effects, gradients, and animations
 * Features:
 * - Hover elevation
 * - Gradient overlays
 * - Smooth animations
 * - Interactive states
 */
export default function EnhancedCard({
  title,
  description,
  children,
  icon: Icon,
  gradient = false,
  hoverable = true,
  onClick,
  className = '',
  delay = 0,
}) {
  return (
    <div
      className={cn(
        onClick && 'cursor-pointer',
        className
      )}
      onClick={onClick}
    >
      <Card
        className={cn(
          'relative overflow-hidden transition-all duration-300',
          hoverable && 'hover:shadow-lg hover:shadow-primary/10',
          gradient && 'border-0'
        )}
      >
        {gradient && (
          <div className="absolute inset-0 bg-gradient-to-br from-primary/10 via-transparent to-primary/5" />
        )}

        <div className="relative z-10">
          <CardHeader className={cn(Icon && 'flex-row items-center justify-between space-y-0')}>
            <div className="space-y-1">
              {title && <CardTitle className="text-lg">{title}</CardTitle>}
              {description && (
                <CardDescription className="text-sm">{description}</CardDescription>
              )}
            </div>
            {Icon && (
              <div className="rounded-full bg-primary/10 p-3">
                <Icon className="h-5 w-5 text-primary" />
              </div>
            )}
          </CardHeader>

          {children && <CardContent>{children}</CardContent>}
        </div>

        {hoverable && (
          <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-primary/50 via-primary to-primary/50 transition-transform duration-300 hover:scale-x-100" />
        )}
      </Card>
    </div>
  );
}





















