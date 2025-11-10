import { useActionState, useEffect } from 'react';
import { useFormStatus } from 'react-dom';
import { X } from 'lucide-react';
import { toast } from 'sonner';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { logger } from '@/lib/logger';
import { shipmentAPI } from '@/services/api';

/**
 * Submit button component using useFormStatus
 * Automatically shows pending state during form submission
 */
function SubmitButton({ isEditMode }) {
  const { pending } = useFormStatus();
  return (
    <Button type="submit" disabled={pending}>
      {pending ? 'Saving...' : isEditMode ? 'Update Address' : 'Create Address'}
    </Button>
  );
}

/**
 * AddressForm Component (React 19 Modernized)
 *
 * Uses React 19's useActionState and useFormStatus for:
 * - Automatic pending state management
 * - Built-in form action handling
 * - Better performance with form actions
 * - Simplified state management
 */
export default function AddressForm({ isOpen, onClose, onSuccess, address = null }) {
  const isEditMode = !!address;

  // Form action using React 19's useActionState
  const [formState, formAction, isPending] = useActionState(
    async (previousState, formData) => {
      try {
        // Extract form data
        const addressData = {
          name: formData.get('name') || '',
          company: formData.get('company') || '',
          street1: formData.get('street1') || '',
          street2: formData.get('street2') || '',
          city: formData.get('city') || '',
          state: formData.get('state') || '',
          zip: formData.get('zip') || '',
          country: formData.get('country') || 'US',
          phone: formData.get('phone') || '',
          email: formData.get('email') || '',
          is_default: formData.get('is_default') === 'on',
        };

        // Validate form
        const errors = [];
        if (!addressData.name?.trim()) errors.push('Name is required');
        if (!addressData.street1?.trim()) errors.push('Street address is required');
        if (!addressData.city?.trim()) errors.push('City is required');
        if (!addressData.state?.trim()) errors.push('State is required');
        if (!addressData.zip?.trim()) errors.push('ZIP code is required');

        // ZIP code format validation
        if (addressData.zip && !/^\d{5}(-\d{4})?$/.test(addressData.zip.trim())) {
          errors.push('Invalid ZIP code format (use 12345 or 12345-6789)');
        }

        // State format validation
        if (addressData.state && addressData.state.trim().length !== 2) {
          errors.push('State must be 2 letters (e.g., CA, NY)');
        }

        // Email validation
        if (
          addressData.email &&
          !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(addressData.email)
        ) {
          errors.push('Invalid email format');
        }

        // Phone validation
        if (
          addressData.phone &&
          (!/^[\d\s\-()+]+$/.test(addressData.phone) || addressData.phone.length < 10)
        ) {
          errors.push('Invalid phone number format');
        }

        if (errors.length > 0) {
          errors.forEach((error) => toast.error(error));
          return { success: false, errors };
        }

        // Save address
        if (isEditMode) {
          await shipmentAPI.updateAddress(address.id, addressData);
          toast.success('Address updated successfully');
        } else {
          await shipmentAPI.createAddress(addressData);
          toast.success('Address created successfully');
        }

        // Call success callback
        if (onSuccess) {
          onSuccess(addressData);
        }

        // Close modal
        onClose();

        return { success: true, errors: [] };
      } catch (error) {
        logger.error('Failed to save address:', error);
        toast.error(isEditMode ? 'Failed to update address' : 'Failed to create address', {
          description: error.message || 'Please try again',
        });
        return { success: false, errors: [error.message] };
      }
    },
    { success: false, errors: [] }
  );

  // Reset form when address prop changes
  useEffect(() => {
    if (!isOpen) return;
    // Form will be reset via defaultValue props
  }, [address, isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="bg-background rounded-lg shadow-lg w-full max-w-2xl max-h-[90vh] overflow-y-auto m-4">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b">
          <h2 className="text-2xl font-bold">
            {isEditMode ? 'Edit Address' : 'Add New Address'}
          </h2>
          <Button variant="ghost" size="icon" onClick={onClose} disabled={isPending}>
            <X className="h-4 w-4" />
          </Button>
        </div>

        {/* Form */}
        <form action={formAction} className="p-6 space-y-6">
          {/* Name and Company */}
          <div className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2">
              <label htmlFor="name" className="text-sm font-medium">
                Name <span className="text-destructive">*</span>
              </label>
              <Input
                id="name"
                name="name"
                defaultValue={address?.name || ''}
                placeholder="John Doe"
                required
              />
            </div>
            <div className="space-y-2">
              <label htmlFor="company" className="text-sm font-medium">
                Company
              </label>
              <Input
                id="company"
                name="company"
                defaultValue={address?.company || ''}
                placeholder="Acme Corp"
              />
            </div>
          </div>

          {/* Street Address */}
          <div className="space-y-2">
            <label htmlFor="street1" className="text-sm font-medium">
              Street Address <span className="text-destructive">*</span>
            </label>
            <Input
              id="street1"
              name="street1"
              defaultValue={address?.street1 || ''}
              placeholder="123 Main St"
              required
            />
          </div>

          <div className="space-y-2">
            <label htmlFor="street2" className="text-sm font-medium">
              Street Address 2
            </label>
            <Input
              id="street2"
              name="street2"
              defaultValue={address?.street2 || ''}
              placeholder="Apt 4B"
            />
          </div>

          {/* City, State, ZIP */}
          <div className="grid gap-4 md:grid-cols-3">
            <div className="space-y-2">
              <label htmlFor="city" className="text-sm font-medium">
                City <span className="text-destructive">*</span>
              </label>
              <Input
                id="city"
                name="city"
                defaultValue={address?.city || ''}
                placeholder="San Francisco"
                required
              />
            </div>
            <div className="space-y-2">
              <label htmlFor="state" className="text-sm font-medium">
                State <span className="text-destructive">*</span>
              </label>
              <Input
                id="state"
                name="state"
                defaultValue={address?.state || ''}
                placeholder="CA"
                maxLength={2}
                required
                onInput={(e) => {
                  e.target.value = e.target.value.toUpperCase();
                }}
              />
            </div>
            <div className="space-y-2">
              <label htmlFor="zip" className="text-sm font-medium">
                ZIP Code <span className="text-destructive">*</span>
              </label>
              <Input
                id="zip"
                name="zip"
                defaultValue={address?.zip || ''}
                placeholder="94102"
                required
              />
            </div>
          </div>

          {/* Country */}
          <div className="space-y-2">
            <label htmlFor="country" className="text-sm font-medium">
              Country
            </label>
            <select
              id="country"
              name="country"
              defaultValue={address?.country || 'US'}
              className="w-full h-9 rounded-md border border-input bg-background px-3 py-1 text-sm"
            >
              <option value="US">United States</option>
              <option value="CA">Canada</option>
              <option value="MX">Mexico</option>
              <option value="GB">United Kingdom</option>
            </select>
          </div>

          {/* Phone and Email */}
          <div className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2">
              <label htmlFor="phone" className="text-sm font-medium">
                Phone
              </label>
              <Input
                id="phone"
                name="phone"
                type="tel"
                defaultValue={address?.phone || ''}
                placeholder="(415) 555-0123"
              />
            </div>
            <div className="space-y-2">
              <label htmlFor="email" className="text-sm font-medium">
                Email
              </label>
              <Input
                id="email"
                name="email"
                type="email"
                defaultValue={address?.email || ''}
                placeholder="john@example.com"
              />
            </div>
          </div>

          {/* Default Address */}
          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="is_default"
              name="is_default"
              defaultChecked={address?.is_default || false}
              className="h-4 w-4 rounded border-input"
            />
            <label htmlFor="is_default" className="text-sm font-medium cursor-pointer">
              Set as default address
            </label>
          </div>

          {/* Actions */}
          <div className="flex justify-end gap-2 pt-4 border-t">
            <Button type="button" variant="outline" onClick={onClose} disabled={isPending}>
              Cancel
            </Button>
            <SubmitButton isEditMode={isEditMode} />
          </div>
        </form>
      </div>
    </div>
  );
}
