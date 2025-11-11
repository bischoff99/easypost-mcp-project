import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Separator } from '@/components/ui/Separator'
import { Info } from 'lucide-react'
import { formatCurrency } from '@/services/currencyService'
import { calculateTaxesAndDuties } from '@/services/internationalShippingService'
import { COUNTRIES } from '@/lib/constants/countries'

/**
 * PriceBreakdown Component
 *
 * Displays itemized cost breakdown with taxes and duties
 */
export default function PriceBreakdown({ itemTotal, shippingRate, country, currency }) {
  if (!shippingRate) {
    return null
  }

  // Calculate taxes and duties
  const taxes = calculateTaxesAndDuties({
    country,
    itemValue: itemTotal,
    shippingCost: shippingRate.rate,
  })

  const subtotal = itemTotal
  const shipping = shippingRate.rate
  const taxTotal = taxes.total
  const grandTotal = subtotal + shipping + taxTotal

  return (
    <Card>
      <CardHeader>
        <CardTitle>Price Breakdown</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {/* Subtotal */}
        <div className="flex items-center justify-between">
          <span className="text-sm text-muted-foreground">Subtotal</span>
          <span className="font-medium">{formatCurrency(subtotal, currency)}</span>
        </div>

        {/* Shipping */}
        <div className="flex items-center justify-between">
          <span className="text-sm text-muted-foreground">Shipping</span>
          <span className="font-medium">{formatCurrency(shipping, currency)}</span>
        </div>

        <Separator />

        {/* Taxes & Duties */}
        {taxes.applicable && (
          <>
            <div className="space-y-2">
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-2">
                  <Info className="h-4 w-4 text-muted-foreground mt-0.5" />
                  <div>
                    <p className="text-sm font-medium">Taxes & Duties</p>
                    <p className="text-xs text-muted-foreground">
                      Estimated for {getCountryName(country)}
                    </p>
                  </div>
                </div>
                <span className="font-medium">{formatCurrency(taxTotal, currency)}</span>
              </div>

              {/* VAT/GST */}
              {taxes.vat > 0 && (
                <div className="flex items-center justify-between pl-6">
                  <span className="text-xs text-muted-foreground">
                    VAT/GST ({(taxes.vatRate * 100).toFixed(0)}%)
                  </span>
                  <span className="text-xs">{formatCurrency(taxes.vat, currency)}</span>
                </div>
              )}

              {/* Customs Duty */}
              {taxes.customsDuty > 0 && (
                <div className="flex items-center justify-between pl-6">
                  <span className="text-xs text-muted-foreground">
                    Customs Duty ({(taxes.customsDutyRate * 100).toFixed(1)}%)
                  </span>
                  <span className="text-xs">{formatCurrency(taxes.customsDuty, currency)}</span>
                </div>
              )}
            </div>

            <Separator />
          </>
        )}

        {!taxes.applicable && taxes.threshold > 0 && (
          <>
            <div className="flex items-start gap-2 p-3 bg-green-50 dark:bg-green-950 rounded-lg">
              <Info className="h-4 w-4 text-green-600 mt-0.5" />
              <p className="text-xs text-green-700 dark:text-green-400">
                No additional taxes or duties apply (under{' '}
                {formatCurrency(taxes.threshold, currency)} threshold)
              </p>
            </div>
            <Separator />
          </>
        )}

        {/* Total */}
        <div className="flex items-center justify-between pt-2">
          <span className="text-lg font-bold">Total</span>
          <span className="text-lg font-bold">{formatCurrency(grandTotal, currency)}</span>
        </div>

        {/* Currency note */}
        {currency !== 'USD' && (
          <p className="text-xs text-muted-foreground text-center">
            Prices shown in {currency}. Original pricing in USD.
          </p>
        )}
      </CardContent>
    </Card>
  )
}

/**
 * Get country name from code
 */
function getCountryName(code) {
  const country = COUNTRIES.find((c) => c.code === code)
  return country ? country.name : code
}
