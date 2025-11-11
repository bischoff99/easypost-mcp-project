import { motion } from 'framer-motion';
import PropTypes from 'prop-types';
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
    <motion.div
      animate={{ rotate: 360 }}
      transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
      className={cn(
        'rounded-full border-2 border-t-transparent',
        sizeClasses[size],
        variantClasses[variant],
        className
      )}
    />
  );
}

LoadingSpinner.propTypes = {
  size: PropTypes.oneOf(['sm', 'md', 'lg', 'xl']),
  variant: PropTypes.oneOf(['primary', 'secondary', 'muted']),
  className: PropTypes.string,
};

/**
 * LoadingOverlay Component
 *
 * Full-screen loading overlay with spinner
 */
export function LoadingOverlay({ message = 'Loading...', className = '' }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className={cn(
        'fixed inset-0 z-50 flex flex-col items-center justify-center bg-background/80 backdrop-blur-sm',
        className
      )}
    >
      <LoadingSpinner size="lg" />
      {message && <p className="mt-4 text-sm text-muted-foreground">{message}</p>}
    </motion.div>
  );
}

LoadingOverlay.propTypes = {
  message: PropTypes.string,
  className: PropTypes.string,
};

/**
 * SkeletonLoader Component
 *
 * Skeleton loader for content placeholders
 */
export function SkeletonLoader({ className = '', rows = 1 }) {
  return (
    <div className="space-y-3">
      {[...Array(rows)].map((_, i) => (
        <motion.div
          key={i}
          initial={{ opacity: 0 }}
          animate={{ opacity: [0.5, 1, 0.5] }}
          transition={{ duration: 1.5, repeat: Infinity, delay: i * 0.1 }}
          className={cn('h-4 bg-muted rounded', className)}
        />
      ))}
    </div>
  );
}

SkeletonLoader.propTypes = {
  className: PropTypes.string,
  rows: PropTypes.number,
};





















