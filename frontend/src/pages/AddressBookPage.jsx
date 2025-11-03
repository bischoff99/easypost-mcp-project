import { useState } from 'react';
import { Plus, Search, Edit2, Trash2, MapPin } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Badge } from '@/components/ui/Badge';

const mockAddresses = [
  {
    id: '1',
    name: 'John Doe',
    company: 'Acme Corp',
    street1: '123 Main St',
    street2: 'Suite 100',
    city: 'San Francisco',
    state: 'CA',
    zip: '94102',
    country: 'US',
    phone: '415-555-0123',
    email: 'john@acme.com',
    is_default: true,
  },
  {
    id: '2',
    name: 'Jane Smith',
    company: 'Tech Inc',
    street1: '456 Market St',
    street2: '',
    city: 'New York',
    state: 'NY',
    zip: '10001',
    country: 'US',
    phone: '212-555-0456',
    email: 'jane@tech.com',
    is_default: false,
  },
  {
    id: '3',
    name: 'Bob Johnson',
    company: '',
    street1: '789 Oak Ave',
    street2: 'Apt 5B',
    city: 'Austin',
    state: 'TX',
    zip: '78701',
    country: 'US',
    phone: '512-555-0789',
    email: 'bob@email.com',
    is_default: false,
  },
];

export default function AddressBookPage() {
  const [addresses, setAddresses] = useState(mockAddresses);
  const [searchQuery, setSearchQuery] = useState('');

  const filteredAddresses = addresses.filter(
    (addr) =>
      addr.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      addr.company.toLowerCase().includes(searchQuery.toLowerCase()) ||
      addr.city.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleDelete = (id) => {
    if (confirm('Are you sure you want to delete this address?')) {
      setAddresses(addresses.filter((addr) => addr.id !== id));
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Address Book</h2>
          <p className="text-muted-foreground">
            Manage your saved shipping addresses
          </p>
        </div>
        <Button className="gap-2">
          <Plus className="h-4 w-4" />
          Add Address
        </Button>
      </div>

      {/* Search */}
      <Card>
        <CardHeader>
          <CardTitle>Search Addresses</CardTitle>
          <CardDescription>Find addresses by name, company, or location</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              placeholder="Search addresses..."
              className="pl-9"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
        </CardContent>
      </Card>

      {/* Stats */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Addresses</CardTitle>
            <MapPin className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{addresses.length}</div>
            <p className="text-xs text-muted-foreground">Saved in your book</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Business Addresses</CardTitle>
            <MapPin className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {addresses.filter((a) => a.company).length}
            </div>
            <p className="text-xs text-muted-foreground">With company name</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Default Address</CardTitle>
            <MapPin className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">1</div>
            <p className="text-xs text-muted-foreground">Set as default</p>
          </CardContent>
        </Card>
      </div>

      {/* Address List */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {filteredAddresses.map((address) => (
          <Card key={address.id} className="relative overflow-hidden hover:shadow-lg transition-shadow">
            {address.is_default && (
              <div className="absolute top-0 right-0">
                <Badge variant="default" className="rounded-none rounded-bl-lg">
                  Default
                </Badge>
              </div>
            )}
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <CardTitle className="text-lg">{address.name}</CardTitle>
                  {address.company && (
                    <CardDescription className="mt-1">{address.company}</CardDescription>
                  )}
                </div>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-1 text-sm">
                <div className="flex items-start gap-2">
                  <MapPin className="h-4 w-4 mt-0.5 text-muted-foreground flex-shrink-0" />
                  <div>
                    <p>{address.street1}</p>
                    {address.street2 && <p>{address.street2}</p>}
                    <p>
                      {address.city}, {address.state} {address.zip}
                    </p>
                    <p className="text-muted-foreground">{address.country}</p>
                  </div>
                </div>
              </div>

              <div className="space-y-1 text-sm text-muted-foreground">
                <p>{address.phone}</p>
                <p>{address.email}</p>
              </div>

              <div className="flex gap-2 pt-2 border-t">
                <Button variant="outline" size="sm" className="flex-1">
                  <Edit2 className="h-3 w-3 mr-1" />
                  Edit
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  className="flex-1"
                  onClick={() => handleDelete(address.id)}
                >
                  <Trash2 className="h-3 w-3 mr-1" />
                  Delete
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Empty State */}
      {filteredAddresses.length === 0 && (
        <Card className="border-dashed">
          <CardContent className="flex flex-col items-center justify-center py-12">
            <MapPin className="h-12 w-12 text-muted-foreground mb-4" />
            <p className="text-lg font-medium">No addresses found</p>
            <p className="text-sm text-muted-foreground mb-4">
              {searchQuery
                ? 'Try a different search term'
                : 'Add your first address to get started'}
            </p>
            {!searchQuery && (
              <Button>
                <Plus className="h-4 w-4 mr-2" />
                Add Address
              </Button>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
