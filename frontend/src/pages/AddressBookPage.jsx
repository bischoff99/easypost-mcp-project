import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';

export default function AddressBookPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Address Book</h2>
        <p className="text-muted-foreground">
          Manage your saved addresses
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Saved Addresses</CardTitle>
          <CardDescription>Your frequently used addresses</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">Address book coming soon...</p>
        </CardContent>
      </Card>
    </div>
  );
}

