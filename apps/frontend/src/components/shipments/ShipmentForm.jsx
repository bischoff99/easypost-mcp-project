import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { shipmentAPI } from '@/services/api';
import { DollarSign, MapPin, Package, Ruler, X } from 'lucide-react';
import { useState } from 'react';
import { toast } from 'sonner';

/**
 * ShipmentForm Component
 *
 * Multi-step form for creating shipments:
 * 1. Addresses (from/to)
 * 2. Parcel details
 * 3. Get rates
 * 4. Select carrier and buy
 */

export default function ShipmentForm({ isOpen, onClose, onSuccess }) {
  const [step, setStep] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [rates, setRates] = useState([]);
  const [selectedRate, setSelectedRate] = useState(null);

  const [formData, setFormData] = useState({
    from_address: {
      name: '',
      street1: '',
      city: '',
      state: '',
      zip: '',
      country: 'US',
      phone: '',
    },
    to_address: {
      name: '',
      street1: '',
      city: '',
      state: '',
      zip: '',
      country: 'US',
      phone: '',
    },
    parcel: {
      length: '',
      width: '',
      height: '',
      weight: '',
    },
  });

  const handleInputChange = (section, field, value) => {
    setFormData((prev) => ({
      ...prev,
      [section]: {
        ...prev[section],
        [field]: value,
      },
    }));
  };

  const handleGetRates = async () => {
    try {
      setIsLoading(true);

      const response = await shipmentAPI.getRates({
        from_address: formData.from_address,
        to_address: formData.to_address,
        parcel: {
          length: parseFloat(formData.parcel.length),
          width: parseFloat(formData.parcel.width),
          height: parseFloat(formData.parcel.height),
          weight: parseFloat(formData.parcel.weight),
        },
      });

      if (response.status === 'success' && response.data) {
        setRates(response.data);
        setStep(3);
        toast.success('Rates Retrieved', {
          description: `Found ${response.data.length} available rates`,
        });
      } else {
        toast.error('Failed to get rates', {
          description: response.message || 'Please try again',
        });
      }
    } catch (error) {
      toast.error('Error', {
        description: error.message || 'Failed to fetch rates',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleBuyShipment = async () => {
    if (!selectedRate) {
      toast.error('No rate selected');
      return;
    }

    try {
      setIsLoading(true);

      const response = await shipmentAPI.buyShipment({
        from_address: formData.from_address,
        to_address: formData.to_address,
        parcel: {
          length: parseFloat(formData.parcel.length),
          width: parseFloat(formData.parcel.width),
          height: parseFloat(formData.parcel.height),
          weight: parseFloat(formData.parcel.weight),
        },
        rate_id: selectedRate.id,
      });

      if (response.status === 'success') {
        toast.success('Shipment Created!', {
          description: `Tracking: ${response.data.tracking_number}`,
        });
        onSuccess?.(response.data);
        handleClose();
      } else {
        toast.error('Failed to create shipment', {
          description: response.message || 'Please try again',
        });
      }
    } catch (error) {
      toast.error('Error', {
        description: error.message || 'Failed to create shipment',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleClose = () => {
    setStep(1);
    setRates([]);
    setSelectedRate(null);
    setFormData({
      from_address: {
        name: '',
        street1: '',
        city: '',
        state: '',
        zip: '',
        country: 'US',
        phone: '',
      },
      to_address: {
        name: '',
        street1: '',
        city: '',
        state: '',
        zip: '',
        country: 'US',
        phone: '',
      },
      parcel: {
        length: '',
        width: '',
        height: '',
        weight: '',
      },
    });
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
      <Card className="w-full max-w-4xl max-h-[90vh] overflow-y-auto m-4">
        <div className="sticky top-0 bg-background border-b p-6 flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold">Create New Shipment</h2>
            <p className="text-sm text-muted-foreground">
              Step {step} of 3:{' '}
              {step === 1 ? 'Addresses' : step === 2 ? 'Parcel Details' : 'Select Rate'}
            </p>
          </div>
          <Button variant="ghost" size="icon" onClick={handleClose}>
            <X className="h-5 w-5" />
          </Button>
        </div>

        <div className="p-6">
          {/* Step 1: Addresses */}
          {step === 1 && (
            <div className="space-y-6">
              {/* From Address */}
              <div className="space-y-4">
                <div className="flex items-center gap-2">
                  <MapPin className="h-5 w-5 text-primary" />
                  <h3 className="text-lg font-semibold">From Address</h3>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <input
                    type="text"
                    placeholder="Name"
                    value={formData.from_address.name}
                    onChange={(e) => handleInputChange('from_address', 'name', e.target.value)}
                    className="col-span-2 rounded-lg border border-input bg-background px-4 py-2"
                  />
                  <input
                    type="text"
                    placeholder="Street Address"
                    value={formData.from_address.street1}
                    onChange={(e) => handleInputChange('from_address', 'street1', e.target.value)}
                    className="col-span-2 rounded-lg border border-input bg-background px-4 py-2"
                  />
                  <input
                    type="text"
                    placeholder="City"
                    value={formData.from_address.city}
                    onChange={(e) => handleInputChange('from_address', 'city', e.target.value)}
                    className="rounded-lg border border-input bg-background px-4 py-2"
                  />
                  <input
                    type="text"
                    placeholder="State"
                    value={formData.from_address.state}
                    onChange={(e) => handleInputChange('from_address', 'state', e.target.value)}
                    className="rounded-lg border border-input bg-background px-4 py-2"
                  />
                  <input
                    type="text"
                    placeholder="ZIP Code"
                    value={formData.from_address.zip}
                    onChange={(e) => handleInputChange('from_address', 'zip', e.target.value)}
                    className="rounded-lg border border-input bg-background px-4 py-2"
                  />
                  <input
                    type="text"
                    placeholder="Phone"
                    value={formData.from_address.phone}
                    onChange={(e) => handleInputChange('from_address', 'phone', e.target.value)}
                    className="rounded-lg border border-input bg-background px-4 py-2"
                  />
                </div>
              </div>

              {/* To Address */}
              <div className="space-y-4">
                <div className="flex items-center gap-2">
                  <MapPin className="h-5 w-5 text-success" />
                  <h3 className="text-lg font-semibold">To Address</h3>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <input
                    type="text"
                    placeholder="Name"
                    value={formData.to_address.name}
                    onChange={(e) => handleInputChange('to_address', 'name', e.target.value)}
                    className="col-span-2 rounded-lg border border-input bg-background px-4 py-2"
                  />
                  <input
                    type="text"
                    placeholder="Street Address"
                    value={formData.to_address.street1}
                    onChange={(e) => handleInputChange('to_address', 'street1', e.target.value)}
                    className="col-span-2 rounded-lg border border-input bg-background px-4 py-2"
                  />
                  <input
                    type="text"
                    placeholder="City"
                    value={formData.to_address.city}
                    onChange={(e) => handleInputChange('to_address', 'city', e.target.value)}
                    className="rounded-lg border border-input bg-background px-4 py-2"
                  />
                  <input
                    type="text"
                    placeholder="State"
                    value={formData.to_address.state}
                    onChange={(e) => handleInputChange('to_address', 'state', e.target.value)}
                    className="rounded-lg border border-input bg-background px-4 py-2"
                  />
                  <input
                    type="text"
                    placeholder="ZIP Code"
                    value={formData.to_address.zip}
                    onChange={(e) => handleInputChange('to_address', 'zip', e.target.value)}
                    className="rounded-lg border border-input bg-background px-4 py-2"
                  />
                  <input
                    type="text"
                    placeholder="Phone"
                    value={formData.to_address.phone}
                    onChange={(e) => handleInputChange('to_address', 'phone', e.target.value)}
                    className="rounded-lg border border-input bg-background px-4 py-2"
                  />
                </div>
              </div>

              <div className="flex justify-end">
                <Button onClick={() => setStep(2)}>Next: Parcel Details</Button>
              </div>
            </div>
          )}

          {/* Step 2: Parcel Details */}
          {step === 2 && (
            <div className="space-y-6">
              <div className="flex items-center gap-2">
                <Package className="h-5 w-5 text-primary" />
                <h3 className="text-lg font-semibold">Parcel Details</h3>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">
                    <Ruler className="inline h-4 w-4 mr-1" />
                    Length (inches)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    placeholder="10"
                    value={formData.parcel.length}
                    onChange={(e) => handleInputChange('parcel', 'length', e.target.value)}
                    className="w-full rounded-lg border border-input bg-background px-4 py-2"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">
                    <Ruler className="inline h-4 w-4 mr-1" />
                    Width (inches)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    placeholder="8"
                    value={formData.parcel.width}
                    onChange={(e) => handleInputChange('parcel', 'width', e.target.value)}
                    className="w-full rounded-lg border border-input bg-background px-4 py-2"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">
                    <Ruler className="inline h-4 w-4 mr-1" />
                    Height (inches)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    placeholder="4"
                    value={formData.parcel.height}
                    onChange={(e) => handleInputChange('parcel', 'height', e.target.value)}
                    className="w-full rounded-lg border border-input bg-background px-4 py-2"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">
                    <Package className="inline h-4 w-4 mr-1" />
                    Weight (oz)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    placeholder="16"
                    value={formData.parcel.weight}
                    onChange={(e) => handleInputChange('parcel', 'weight', e.target.value)}
                    className="w-full rounded-lg border border-input bg-background px-4 py-2"
                  />
                </div>
              </div>

              <div className="flex justify-between">
                <Button variant="outline" onClick={() => setStep(1)}>
                  Back
                </Button>
                <Button onClick={handleGetRates} disabled={isLoading}>
                  {isLoading ? 'Getting Rates...' : 'Get Rates'}
                </Button>
              </div>
            </div>
          )}

          {/* Step 3: Select Rate */}
          {step === 3 && (
            <div className="space-y-6">
              <div className="flex items-center gap-2">
                <DollarSign className="h-5 w-5 text-success" />
                <h3 className="text-lg font-semibold">Select Shipping Rate</h3>
              </div>

              <div className="space-y-3">
                {rates.map((rate) => (
                  <button
                    key={rate.id}
                    onClick={() => setSelectedRate(rate)}
                    className={`w-full p-4 rounded-lg border-2 text-left transition-all ${
                      selectedRate?.id === rate.id
                        ? 'border-primary bg-primary/5'
                        : 'border-border hover:border-primary/50'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="font-semibold">
                          {rate.carrier} - {rate.service}
                        </div>
                        <div className="text-sm text-muted-foreground">
                          Delivery: {rate.delivery_days} day{rate.delivery_days > 1 ? 's' : ''}
                          {rate.delivery_date &&
                            ` (${new Date(rate.delivery_date).toLocaleDateString()})`}
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-bold">
                          ${parseFloat(rate.rate).toFixed(2)}
                        </div>
                      </div>
                    </div>
                  </button>
                ))}
              </div>

              {rates.length === 0 && (
                <div className="text-center py-8 text-muted-foreground">No rates available</div>
              )}

              <div className="flex justify-between">
                <Button variant="outline" onClick={() => setStep(2)}>
                  Back
                </Button>
                <Button onClick={handleBuyShipment} disabled={!selectedRate || isLoading}>
                  {isLoading ? 'Creating...' : 'Buy Label'}
                </Button>
              </div>
            </div>
          )}
        </div>
      </Card>
    </div>
  );
}
