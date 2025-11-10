import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { toast } from 'sonner';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import CountrySelector from './CountrySelector';
import ShippingOptions from './ShippingOptions';
import PriceBreakdown from './PriceBreakdown';
import useShippingRates from '@/hooks/useShippingRates';
import { getCurrencyFromCountry } from '@/services/currencyService';
import { Loader2 } from 'lucide-react';

/**
 * InternationalShippingForm Component
 *
 * Complete form for international shipping with:
 * - Country selection
 * - Address input
 * - Shipping rate calculation
 * - Price breakdown with taxes
 */
export default function InternationalShippingForm() {
  const { t } = useTranslation();
  const { getRates, rates, isLoading, error: _error } = useShippingRates();

  const [selectedCountry, setSelectedCountry] = useState('GB');
  const [selectedRate, setSelectedRate] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    street1: '',
    street2: '',
    city: '',
    state: '',
    zip: '',
    phone: '',
  });

  const currency = getCurrencyFromCountry(selectedCountry);
  const itemTotal = 100; // Example item total

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleCountryChange = (country) => {
    setSelectedCountry(country);
    setSelectedRate(null);
  };

  const handleGetRates = async () => {
    if (!formData.street1 || !formData.city || !formData.zip) {
      toast.error('Please fill in all required fields');
      return;
    }

    try {
      await getRates({
        from_address: {
          name: 'Sender Name',
          street1: '123 Main St',
          city: 'San Francisco',
          state: 'CA',
          zip: '94107',
          country: 'US',
        },
        to_address: {
          ...formData,
          country: selectedCountry,
        },
        parcel: {
          length: 10,
          width: 8,
          height: 6,
          weight: 16,
        },
      });

      toast.success('Shipping rates retrieved');
    } catch (err) {
      toast.error('Failed to get rates', {
        description: err.message || 'Please try again',
      });
    }
  };

  return (
    <div className="container mx-auto max-w-6xl py-8 px-4">
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold">International Shipping</h1>
          <p className="text-muted-foreground">
            Get rates and ship to over 200 countries worldwide
          </p>
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          {/* Left Column - Address Form */}
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>{t('shipping.selectDestination')}</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Country Selector */}
                <div>
                  <label className="text-sm font-medium mb-2 block">
                    {t('address.country')}
                  </label>
                  <CountrySelector
                    value={selectedCountry}
                    onChange={handleCountryChange}
                    disabled={isLoading}
                  />
                </div>

                {/* Name */}
                <div>
                  <label className="text-sm font-medium mb-2 block">
                    {t('address.name')}
                  </label>
                  <Input
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    placeholder="John Doe"
                  />
                </div>

                {/* Street Address */}
                <div>
                  <label className="text-sm font-medium mb-2 block">
                    {t('address.street1')} *
                  </label>
                  <Input
                    name="street1"
                    value={formData.street1}
                    onChange={handleInputChange}
                    placeholder="123 Main Street"
                    required
                  />
                </div>

                {/* Street 2 */}
                <div>
                  <label className="text-sm font-medium mb-2 block">
                    {t('address.street2')}
                  </label>
                  <Input
                    name="street2"
                    value={formData.street2}
                    onChange={handleInputChange}
                    placeholder="Apt 4B"
                  />
                </div>

                {/* City */}
                <div>
                  <label className="text-sm font-medium mb-2 block">
                    {t('address.city')} *
                  </label>
                  <Input
                    name="city"
                    value={formData.city}
                    onChange={handleInputChange}
                    placeholder="London"
                    required
                  />
                </div>

                {/* State/Province */}
                <div>
                  <label className="text-sm font-medium mb-2 block">
                    {t('address.state')}
                  </label>
                  <Input
                    name="state"
                    value={formData.state}
                    onChange={handleInputChange}
                    placeholder="Greater London"
                  />
                </div>

                {/* Postal Code */}
                <div>
                  <label className="text-sm font-medium mb-2 block">
                    {t('address.zip')} *
                  </label>
                  <Input
                    name="zip"
                    value={formData.zip}
                    onChange={handleInputChange}
                    placeholder="SW1A 1AA"
                    required
                  />
                </div>

                {/* Phone */}
                <div>
                  <label className="text-sm font-medium mb-2 block">
                    {t('address.phone')}
                  </label>
                  <Input
                    name="phone"
                    value={formData.phone}
                    onChange={handleInputChange}
                    placeholder="+44 20 1234 5678"
                  />
                </div>

                <Button
                  onClick={handleGetRates}
                  disabled={isLoading}
                  className="w-full"
                >
                  {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                  Get Shipping Rates
                </Button>
              </CardContent>
            </Card>
          </div>

          {/* Right Column - Rates & Pricing */}
          <div className="space-y-6">
            <ShippingOptions
              rates={rates}
              selectedRate={selectedRate}
              onSelectRate={setSelectedRate}
              currency={currency}
            />

            {selectedRate && (
              <PriceBreakdown
                itemTotal={itemTotal}
                shippingRate={selectedRate}
                country={selectedCountry}
                currency={currency}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
