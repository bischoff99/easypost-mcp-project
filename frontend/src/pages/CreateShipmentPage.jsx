import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { shipmentAPI } from '@/services/api';
import { DollarSign, MapPin, Package, Ruler, ArrowLeft } from 'lucide-react';
import { useState, useOptimistic, useActionState, useTransition } from 'react';
import { toast } from 'sonner';
import { useNavigate } from 'react-router-dom';
import { logger } from '@/lib/logger';

/**
 * CreateShipmentPage Component
 *
 * Full-page multi-step form for creating shipments:
 * 1. Addresses (from/to)
 * 2. Parcel details
 * 3. Get rates
 * 4. Select carrier and buy
 */

export default function CreateShipmentPage() {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [rates, setRates] = useState([]);
  const [selectedRate, setSelectedRate] = useState(null);
  const [_isPending, startTransition] = useTransition();

  // Optimistic UI for rates - show rates immediately while fetching
  const [optimisticRates, addOptimisticRates] = useOptimistic(
    rates,
    (currentRates, newRates) => {
      // If newRates is an array, replace; if it's a loading indicator, keep current
      return Array.isArray(newRates) ? newRates : currentRates;
    }
  );

  // React 19 action for buying shipment
  const [_purchaseState, purchaseAction, isPurchasePending] = useActionState(
    async (previousState, formDataOrPayload) => {
      if (!selectedRate) {
        toast.error('No rate selected');
        return { success: false, error: 'No rate selected' };
      }

      // Handle both FormData (from form action) and direct payload
      let shipmentData;
      if (formDataOrPayload instanceof FormData) {
        shipmentData = {
          from_address: JSON.parse(formDataOrPayload.get('from_address')),
          to_address: JSON.parse(formDataOrPayload.get('to_address')),
          parcel: JSON.parse(formDataOrPayload.get('parcel')),
          rate_id: formDataOrPayload.get('rate_id'),
        };
      } else {
        shipmentData = formDataOrPayload;
      }

      try {
        const response = await shipmentAPI.buyShipment({
          from_address: shipmentData.from_address || formData.from_address,
          to_address: shipmentData.to_address || formData.to_address,
          parcel: {
            length: parseFloat(shipmentData.parcel?.length || formData.parcel.length),
            width: parseFloat(shipmentData.parcel?.width || formData.parcel.width),
            height: parseFloat(shipmentData.parcel?.height || formData.parcel.height),
            weight: parseFloat(shipmentData.parcel?.weight || formData.parcel.weight),
          },
          rate_id: shipmentData.rate_id || selectedRate.id,
        });

        if (response.status === 'success') {
          toast.success('Shipment Created!', {
            description: `Tracking: ${response.data.tracking_number}`,
          });
          startTransition(() => {
            navigate('/shipments');
          });
          return { success: true, trackingNumber: response.data.tracking_number };
        } else {
          toast.error('Failed to create shipment', {
            description: response.message || 'Please try again',
          });
          return { success: false, error: response.message };
        }
      } catch (error) {
        logger.error('Failed to create shipment:', error);
        toast.error('Error', {
          description: error.message || 'Failed to create shipment',
        });
        return { success: false, error: error.message };
      }
    },
    { success: false, error: null }
  );

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

      // Optimistically show loading state
      addOptimisticRates([]);

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
        // Update both actual and optimistic state
        setRates(response.data);
        addOptimisticRates(response.data);
        setStep(3);
        toast.success('Rates Retrieved', {
          description: `Found ${response.data.length} available rates`,
        });
      } else {
        toast.error('Failed to get rates', {
          description: response.message || 'Please try again',
        });
        addOptimisticRates([]);
      }
    } catch (error) {
      logger.error('Failed to fetch rates:', error);
      toast.error('Error', {
        description: error.message || 'Failed to fetch rates',
      });
      addOptimisticRates([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleBuyShipment = () => {
    if (!selectedRate) {
      toast.error('No rate selected');
      return;
    }

    // Use React 19 action with payload object
    purchaseAction({
      from_address: formData.from_address,
      to_address: formData.to_address,
      parcel: formData.parcel,
      rate_id: selectedRate.id,
    });
  };

  return (
    <div className="container mx-auto max-w-4xl py-8 px-4">
      <Card className="w-full">
        <div className="border-b p-6 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => navigate('/shipments')}
              className="mr-2"
            >
              <ArrowLeft className="h-5 w-5" />
            </Button>
            <div>
              <h2 className="text-2xl font-bold">Create New Shipment</h2>
              <p className="text-sm text-muted-foreground">
                Step {step} of 3:{' '}
                {step === 1 ? 'Addresses' : step === 2 ? 'Parcel Details' : 'Select Rate'}
              </p>
            </div>
          </div>
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
                {optimisticRates.length > 0 ? (
                  optimisticRates.map((rate) => (
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
                  ))
                ) : isLoading ? (
                  <div className="text-center py-8 text-muted-foreground">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-2"></div>
                    Fetching rates...
                  </div>
                ) : (
                  <div className="text-center py-8 text-muted-foreground">No rates available</div>
                )}
              </div>

              <div className="flex justify-between">
                <Button variant="outline" onClick={() => setStep(2)}>
                  Back
                </Button>
                <Button onClick={handleBuyShipment} disabled={!selectedRate || isPurchasePending}>
                  {isPurchasePending ? 'Creating...' : 'Buy Label'}
                </Button>
              </div>
            </div>
          )}
        </div>
      </Card>
    </div>
  );
}
