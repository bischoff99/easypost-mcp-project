import { motion } from 'framer-motion';
import { Button } from './Button';
import PropTypes from 'prop-types';

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
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className={`flex flex-col items-center justify-center py-12 px-4 text-center ${className}`}
    >
      {Icon && (
        <motion.div
          initial={{ scale: 0.8 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.1, type: 'spring', stiffness: 200 }}
          className="mb-6 rounded-full bg-muted/50 p-6"
        >
          <Icon className="h-12 w-12 text-muted-foreground" />
        </motion.div>
      )}

      <motion.h3
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
        className="text-xl font-semibold mb-2"
      >
        {title}
      </motion.h3>

      {description && (
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="text-sm text-muted-foreground max-w-md mb-6"
        >
          {description}
        </motion.p>
      )}

      {(action || secondaryAction) && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="flex gap-3"
        >
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
        </motion.div>
      )}
    </motion.div>
  );
}

EmptyState.propTypes = {
  icon: PropTypes.elementType,
  title: PropTypes.string.isRequired,
  description: PropTypes.string,
  action: PropTypes.func,
  actionLabel: PropTypes.string,
  secondaryAction: PropTypes.func,
  secondaryActionLabel: PropTypes.string,
  className: PropTypes.string,
};





















