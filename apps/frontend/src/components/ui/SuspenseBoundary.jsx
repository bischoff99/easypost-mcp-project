import { Suspense, useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { Skeleton } from '@/components/ui/Skeleton';

/**
 * Navigation-aware loading component
 * Shows loading state during route transitions
 * Uses useLocation to detect route changes (works with BrowserRouter)
 */
export default function NavigationLoader() {
  const location = useLocation();
  const [isNavigating, setIsNavigating] = useState(false);

  useEffect(() => {
    // Use requestAnimationFrame to avoid synchronous setState warning
    let timer;
    const frame = requestAnimationFrame(() => {
      setIsNavigating(true);
      timer = setTimeout(() => setIsNavigating(false), 300);
    });
    return () => {
      cancelAnimationFrame(frame);
      if (timer) clearTimeout(timer);
    };
  }, [location.pathname]);

  if (isNavigating) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-background/80 backdrop-blur-sm">
        <div className="flex flex-col items-center gap-4">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          <p className="text-sm text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  return null;
}

/**
 * Page-level Suspense boundary with skeleton fallback
 */
export function PageSuspense({ children, fallback }) {
  return (
    <Suspense
      fallback={
        fallback || (
          <div className="space-y-6 animate-fade-in">
            <div>
              <Skeleton className="h-9 w-48 mb-2" />
              <Skeleton className="h-4 w-96" />
            </div>
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              {Array.from({ length: 4 }).map((_, i) => (
                <Skeleton key={i} className="h-32" />
              ))}
            </div>
          </div>
        )
      }
    >
      {children}
    </Suspense>
  );
}
