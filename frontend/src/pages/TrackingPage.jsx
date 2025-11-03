import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';

export default function TrackingPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Tracking</h2>
        <p className="text-muted-foreground">
          Track your packages in real-time
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Package Tracking</CardTitle>
          <CardDescription>Enter tracking number to see live updates</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">Tracking interface coming soon...</p>
        </CardContent>
      </Card>
    </div>
  );
}

