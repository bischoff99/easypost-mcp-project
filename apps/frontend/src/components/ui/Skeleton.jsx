import { cn } from '@/lib/utils';

// Enhanced Skeleton with better shimmer effect
function Skeleton({ className, ...props }) {
  return (
    <div
      className={cn(
        'animate-pulse rounded-md bg-muted relative overflow-hidden',
        'before:absolute before:inset-0 before:-translate-x-full',
        'before:bg-gradient-to-r before:from-transparent before:via-white/10 before:to-transparent',
        'before:animate-[shimmer_1.5s_ease-in-out_infinite]',
        className
      )}
      {...props}
    />
  );
}

// Specialized skeleton components for different content types
function SkeletonText({ lines = 1, className, ...props }) {
  if (lines === 1) {
    return <Skeleton className={cn('h-4 w-full', className)} {...props} />;
  }

  return (
    <div className="space-y-2">
      {Array.from({ length: lines }).map((_, i) => (
        <Skeleton
          key={i}
          className={cn(
            'h-4',
            i === lines - 1 ? 'w-3/4' : 'w-full', // Last line shorter
            className
          )}
          {...props}
        />
      ))}
    </div>
  );
}

function SkeletonCard({ className, ...props }) {
  return (
    <div className={cn('rounded-lg border border-border p-6 space-y-4', className)} {...props}>
      <Skeleton className="h-6 w-1/3" />
      <SkeletonText lines={2} />
      <div className="flex gap-2">
        <Skeleton className="h-8 w-20" />
        <Skeleton className="h-8 w-16" />
      </div>
    </div>
  );
}

function SkeletonTable({ rows = 5, columns = 4, className, ...props }) {
  return (
    <div className={cn('space-y-4', className)} {...props}>
      {/* Table Header */}
      <div className="flex gap-4 pb-2 border-b border-border">
        {Array.from({ length: columns }).map((_, i) => (
          <Skeleton key={`header-${i}`} className="h-4 flex-1" />
        ))}
      </div>

      {/* Table Rows */}
      {Array.from({ length: rows }).map((_, rowIndex) => (
        <div key={`row-${rowIndex}`} className="flex gap-4 py-3">
          {Array.from({ length: columns }).map((_, colIndex) => (
            <Skeleton
              key={`cell-${rowIndex}-${colIndex}`}
              className={cn(
                'h-4 flex-1',
                colIndex === 0 ? 'w-12' : colIndex === columns - 1 ? 'w-24' : ''
              )}
            />
          ))}
        </div>
      ))}
    </div>
  );
}

function SkeletonStats({ count = 4, className, ...props }) {
  return (
    <div className={cn('grid gap-4 md:grid-cols-2 lg:grid-cols-4', className)} {...props}>
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="rounded-lg border border-border p-6 space-y-3">
          <div className="flex items-center justify-between">
            <Skeleton className="h-4 w-20" />
            <Skeleton className="h-6 w-6 rounded-full" />
          </div>
          <Skeleton className="h-8 w-16" />
          <Skeleton className="h-3 w-24" />
        </div>
      ))}
    </div>
  );
}

export { Skeleton, SkeletonText, SkeletonCard, SkeletonTable, SkeletonStats };
