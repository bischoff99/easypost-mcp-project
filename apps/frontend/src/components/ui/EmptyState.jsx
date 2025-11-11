import { Button } from './Button';

/**
 * EmptyState Component
 *
 * Beautiful empty state component for when there's no data to display
 * Supports custom icons, titles, descriptions, and action buttons
 */
export default function EmptyState({
  icon: Icon,
  title,
  description,
  action,
  actionLabel,
  secondaryAction,
  secondaryActionLabel,
  className = '',
}) {
  return (
    <div className={`flex flex-col items-center justify-center py-12 px-4 text-center ${className}`}>
      {Icon && (
        <div className="mb-6 rounded-full bg-muted/50 p-6">
          <Icon className="h-12 w-12 text-muted-foreground" />
        </div>
      )}

      <h3 className="text-xl font-semibold mb-2">
        {title}
      </h3>

      {description && (
        <p className="text-sm text-muted-foreground max-w-md mb-6">
          {description}
        </p>
      )}

      {(action || secondaryAction) && (
        <div className="flex gap-3">
          {action && (
            <Button onClick={action} size="lg">
              {actionLabel || 'Get Started'}
            </Button>
          )}
          {secondaryAction && (
            <Button onClick={secondaryAction} variant="outline" size="lg">
              {secondaryActionLabel || 'Learn More'}
            </Button>
          )}
        </div>
      )}
    </div>
  );
}





















