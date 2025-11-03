import { useState } from 'react';
import { Save, Bell, Eye, Globe, Shield, User } from 'lucide-react';
import { toast } from 'sonner';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import api from '@/services/api';

export default function SettingsPage() {
  const [settings, setSettings] = useState({
    apiKey: '••••••••••••••••••••',
    companyName: 'Acme Corp',
    email: 'admin@acme.com',
    phone: '415-555-0123',
    notifyOnShipment: true,
    notifyOnDelivery: true,
    notifyOnException: true,
    theme: 'system',
    language: 'en',
    timezone: 'America/Los_Angeles',
  });
  const [isSaving, setIsSaving] = useState(false);

  const handleSave = async () => {
    setIsSaving(true);
    try {
      // Save to backend API
      await api.post('/settings', settings);
      toast.success('Settings saved!', { 
        description: 'Your preferences have been updated successfully.' 
      });
    } catch (error) {
      toast.error('Failed to save settings', {
        description: error.message || 'Please try again later.'
      });
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in max-w-4xl">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Settings</h2>
        <p className="text-muted-foreground">
          Manage your account settings and preferences
        </p>
      </div>

      {/* Account Settings */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <User className="h-5 w-5" />
            <CardTitle>Account Information</CardTitle>
          </div>
          <CardDescription>Update your account details</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <label className="text-sm font-medium">Company Name</label>
            <Input
              value={settings.companyName}
              onChange={(e) => setSettings({ ...settings, companyName: e.target.value })}
            />
          </div>
          <div className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2">
              <label className="text-sm font-medium">Email</label>
              <Input
                type="email"
                value={settings.email}
                onChange={(e) => setSettings({ ...settings, email: e.target.value })}
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Phone</label>
              <Input
                type="tel"
                value={settings.phone}
                onChange={(e) => setSettings({ ...settings, phone: e.target.value })}
              />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* API Settings */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Shield className="h-5 w-5" />
            <CardTitle>API Configuration</CardTitle>
          </div>
          <CardDescription>Manage your EasyPost API credentials</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <label className="text-sm font-medium">EasyPost API Key</label>
            <div className="flex gap-2">
              <Input
                type="password"
                value={settings.apiKey}
                onChange={(e) => setSettings({ ...settings, apiKey: e.target.value })}
                className="font-mono"
              />
              <Button variant="outline">
                <Eye className="h-4 w-4" />
              </Button>
            </div>
            <p className="text-xs text-muted-foreground">
              Your API key is encrypted and stored securely
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Notification Settings */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Bell className="h-5 w-5" />
            <CardTitle>Notifications</CardTitle>
          </div>
          <CardDescription>Choose what notifications you receive</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium">Shipment Created</p>
              <p className="text-sm text-muted-foreground">
                Get notified when a new shipment is created
              </p>
            </div>
            <input
              type="checkbox"
              checked={settings.notifyOnShipment}
              onChange={(e) =>
                setSettings({ ...settings, notifyOnShipment: e.target.checked })
              }
              className="h-4 w-4 rounded border-input"
            />
          </div>
          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium">Delivery Completed</p>
              <p className="text-sm text-muted-foreground">
                Get notified when a package is delivered
              </p>
            </div>
            <input
              type="checkbox"
              checked={settings.notifyOnDelivery}
              onChange={(e) =>
                setSettings({ ...settings, notifyOnDelivery: e.target.checked })
              }
              className="h-4 w-4 rounded border-input"
            />
          </div>
          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium">Shipping Exceptions</p>
              <p className="text-sm text-muted-foreground">
                Get notified when there's a shipping exception
              </p>
            </div>
            <input
              type="checkbox"
              checked={settings.notifyOnException}
              onChange={(e) =>
                setSettings({ ...settings, notifyOnException: e.target.checked })
              }
              className="h-4 w-4 rounded border-input"
            />
          </div>
        </CardContent>
      </Card>

      {/* Preferences */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Globe className="h-5 w-5" />
            <CardTitle>Preferences</CardTitle>
          </div>
          <CardDescription>Customize your experience</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <label className="text-sm font-medium">Theme</label>
            <select
              value={settings.theme}
              onChange={(e) => setSettings({ ...settings, theme: e.target.value })}
              className="w-full h-9 rounded-md border border-input bg-transparent px-3 py-1 text-sm"
            >
              <option value="light">Light</option>
              <option value="dark">Dark</option>
              <option value="system">System</option>
            </select>
          </div>
          <div className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2">
              <label className="text-sm font-medium">Language</label>
              <select
                value={settings.language}
                onChange={(e) => setSettings({ ...settings, language: e.target.value })}
                className="w-full h-9 rounded-md border border-input bg-transparent px-3 py-1 text-sm"
              >
                <option value="en">English</option>
                <option value="es">Spanish</option>
                <option value="fr">French</option>
              </select>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Timezone</label>
              <select
                value={settings.timezone}
                onChange={(e) => setSettings({ ...settings, timezone: e.target.value })}
                className="w-full h-9 rounded-md border border-input bg-transparent px-3 py-1 text-sm"
              >
                <option value="America/Los_Angeles">Pacific Time</option>
                <option value="America/Denver">Mountain Time</option>
                <option value="America/Chicago">Central Time</option>
                <option value="America/New_York">Eastern Time</option>
              </select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Save Button */}
      <div className="flex justify-end">
        <Button onClick={handleSave} disabled={isSaving} className="gap-2">
          <Save className="h-4 w-4" />
          {isSaving ? 'Saving...' : 'Save Changes'}
        </Button>
      </div>
    </div>
  );
}
