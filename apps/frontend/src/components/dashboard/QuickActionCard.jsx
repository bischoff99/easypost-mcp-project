import { motion } from 'framer-motion'
import PropTypes from 'prop-types'
import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card'
import { cn } from '@/lib/utils'

export default function QuickActionCard({
  title,
  description,
  icon: Icon,
  onClick,
  delay = 0,
  color = 'primary',
}) {
  const colorClasses = {
    primary: 'hover:bg-primary hover:text-primary-foreground',
    secondary: 'hover:bg-secondary hover:text-secondary-foreground',
    accent: 'hover:bg-accent hover:text-accent-foreground',
  }

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3, delay }}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
    >
      <Card
        className={cn('cursor-pointer transition-all hover:shadow-xl', colorClasses[color])}
        onClick={onClick}
      >
        <CardHeader className="flex flex-row items-center gap-4">
          <div className="rounded-full bg-primary/10 p-3">
            <Icon className="h-6 w-6 text-primary" />
          </div>
          <div className="flex-1">
            <CardTitle className="text-base">{title}</CardTitle>
            <CardDescription>{description}</CardDescription>
          </div>
        </CardHeader>
      </Card>
    </motion.div>
  )
}

QuickActionCard.propTypes = {
  title: PropTypes.string.isRequired,
  description: PropTypes.string.isRequired,
  icon: PropTypes.elementType.isRequired,
  onClick: PropTypes.func.isRequired,
  delay: PropTypes.number,
  color: PropTypes.oneOf(['primary', 'secondary', 'accent']),
}
