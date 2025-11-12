import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card'
import { cn } from '@/lib/utils'

export default function QuickActionCard({
  title,
  description,
  icon: Icon,
  onClick,
  delay: _delay = 0,
  color = 'primary',
}) {
  const colorClasses = {
    primary: 'hover:bg-primary hover:text-primary-foreground',
    secondary: 'hover:bg-secondary hover:text-secondary-foreground',
    accent: 'hover:bg-accent hover:text-accent-foreground',
  }

  return (
    <div>
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
    </div>
  )
}
