import { Check, Package, Truck, Plane } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { formatCurrency } from '@/services/currencyService'
import {
  getEstimatedDeliveryDate,
  parseDeliveryDays,
} from '@/services/internationalShippingService'

/**
 * ShippingOptions Component
 *
 * Displays available shipping methods with costs and delivery estimates
 */
export default function ShippingOptions({ rates, selectedRate, onSelectRate, currency }) {
  if (!rates || rates.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Shipping Options</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            Enter destination details to see available shipping options
          </p>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Shipping Options</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {rates.map((rate) => {
          const isSelected = selectedRate?.id === rate.id
          const deliveryDays = parseDeliveryDays(rate.service)
          const estimatedDate = getEstimatedDeliveryDate(deliveryDays)

          return (
            <button
              key={rate.id}
              onClick={() => onSelectRate(rate)}
              className={`w-full text-left p-4 rounded-lg border-2 transition-all ${
                isSelected ? 'border-primary bg-primary/5' : 'border-border hover:border-primary/50'
              }`}
              aria-label={`Select ${rate.service} shipping option`}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-3">
                  {getServiceIcon(rate.service)}
                  <div>
                    <div className="flex items-center gap-2">
                      <h4 className="font-semibold">{rate.carrier}</h4>
                      {isSelected && <Check className="h-4 w-4 text-primary" />}
                    </div>
                    <p className="text-sm text-muted-foreground">{rate.service}</p>
                    <p className="text-xs text-muted-foreground mt-1">
                      Est. delivery: {estimatedDate} ({deliveryDays} days)
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="font-bold">{formatCurrency(rate.rate, currency || 'USD')}</p>
                  {rate.original_rate && currency !== 'USD' && (
                    <p className="text-xs text-muted-foreground">
                      ({formatCurrency(rate.original_rate, 'USD')})
                    </p>
                  )}
                </div>
              </div>
            </button>
          )
        })}
      </CardContent>
    </Card>
  )
}

/**
 * Get icon based on service type
 */
function getServiceIcon(service) {
  const serviceLower = service.toLowerCase()

  if (serviceLower.includes('express') || serviceLower.includes('overnight')) {
    return (
      <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-500/10">
        <Plane className="h-5 w-5 text-blue-600" />
      </div>
    )
  }

  if (serviceLower.includes('priority')) {
    return (
      <div className="flex h-10 w-10 items-center justify-center rounded-full bg-orange-500/10">
        <Truck className="h-5 w-5 text-orange-600" />
      </div>
    )
  }

  return (
    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-green-500/10">
      <Package className="h-5 w-5 text-green-600" />
    </div>
  )
}
