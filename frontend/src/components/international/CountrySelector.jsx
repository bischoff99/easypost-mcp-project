import { useState } from 'react';
import { Check, ChevronDown, Globe } from 'lucide-react';
import * as Select from '@radix-ui/react-select';
import { COUNTRIES, REGIONS } from '@/data/countries';
import { Button } from '@/components/ui/Button';

/**
 * CountrySelector Component
 *
 * Dropdown for selecting destination country with flags and regions
 */
export default function CountrySelector({ value, onChange, disabled }) {
  const [open, setOpen] = useState(false);

  const selectedCountry = COUNTRIES.find((c) => c.code === value);

  return (
    <Select.Root value={value} onValueChange={onChange} open={open} onOpenChange={setOpen}>
      <Select.Trigger asChild>
        <Button
          variant="outline"
          className="w-full justify-between"
          disabled={disabled}
          aria-label="Select destination country"
        >
          <span className="flex items-center gap-2">
            {selectedCountry ? (
              <>
                <span className="text-lg">{getFlagEmoji(selectedCountry.code)}</span>
                <span>{selectedCountry.name}</span>
              </>
            ) : (
              <>
                <Globe className="h-4 w-4" />
                <span>Select country</span>
              </>
            )}
          </span>
          <ChevronDown className="h-4 w-4 opacity-50" />
        </Button>
      </Select.Trigger>

      <Select.Portal>
        <Select.Content
          className="overflow-hidden rounded-md border bg-background shadow-lg z-50 max-h-[300px]"
          position="popper"
          sideOffset={5}
        >
          <Select.Viewport className="p-1">
            {REGIONS.map((region) => (
              <Select.Group key={region}>
                <Select.Label className="px-3 py-2 text-xs font-semibold text-muted-foreground">
                  {region}
                </Select.Label>
                {COUNTRIES.filter((c) => c.region === region).map((country) => (
                  <Select.Item
                    key={country.code}
                    value={country.code}
                    className="relative flex items-center gap-2 px-3 py-2 text-sm outline-none cursor-pointer hover:bg-accent rounded-sm data-[highlighted]:bg-accent"
                  >
                    <span className="text-lg">{getFlagEmoji(country.code)}</span>
                    <Select.ItemText>{country.name}</Select.ItemText>
                    {value === country.code && (
                      <Select.ItemIndicator className="ml-auto">
                        <Check className="h-4 w-4" />
                      </Select.ItemIndicator>
                    )}
                  </Select.Item>
                ))}
              </Select.Group>
            ))}
          </Select.Viewport>
        </Select.Content>
      </Select.Portal>
    </Select.Root>
  );
}

/**
 * Get flag emoji from country code
 */
function getFlagEmoji(countryCode) {
  const codePoints = countryCode
    .toUpperCase()
    .split('')
    .map((char) => 127397 + char.charCodeAt());
  return String.fromCodePoint(...codePoints);
}
