import { cn } from '@/lib/utils';

/**
 * LoadingSpinner Component
 *
 * Versatile loading spinner with multiple variants and sizes
 */
export function LoadingSpinner({ size = 'md', variant = 'primary', className = '' }) {
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-8 w-8',
    lg: 'h-12 w-12',
    xl: 'h-16 w-16',
  };

  const variantClasses = {
    primary: 'border-primary',
    secondary: 'border-secondary',
    muted: 'border-muted-foreground',
  };

  return (
    <div
      className={cn(
        'rounded-full border-2 border-t-transparent animate-spin',
        sizeClasses[size],
        variantClasses[variant],
        className
      )}
    />
  );
}

/**
 * LoadingOverlay Component
 *
 * Full-screen loading overlay with spinner
 */
export function LoadingOverlay({ message = 'Loading...', className = '' }) {
  return (
    <div
      className={cn(
        'fixed inset-0 z-50 flex flex-col items-center justify-center bg-background/80 backdrop-blur-sm',
        className
      )}
    >
      <LoadingSpinner size="lg" />
      {message && <p className="mt-4 text-sm text-muted-foreground">{message}</p>}
    </div>
  );
}

/**
 * SkeletonLoader Component
 *
 * Skeleton loader for content placeholders
 */
export function SkeletonLoader({ className = '', rows = 1 }) {
  return (
    <div className="space-y-3">
      {[...Array(rows)].map((_, i) => (
        <div
          key={i}
          className={cn('h-4 bg-muted rounded animate-pulse', className)}
        />
      ))}
    </div>
  );
}
