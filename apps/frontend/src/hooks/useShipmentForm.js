import { useState } from 'react';

/**
 * Custom hook for managing shipment form state
 */
export function useShipmentForm() {
  const [formData, setFormData] = useState({
    to_address: {
      name: '',
      street1: '',
      city: '',
      state: '',
      zip: '',
      country: 'US',
    },
    from_address: {
      name: '',
      street1: '',
      city: '',
      state: '',
      zip: '',
      country: 'US',
    },
    parcel: {
      length: 10,
      width: 8,
      height: 5,
      weight: 2,
    },
    carrier: 'USPS',
  });

  const updateToAddress = (field, value) => {
    setFormData((prev) => ({
      ...prev,
      to_address: { ...prev.to_address, [field]: value },
    }));
  };

  const updateFromAddress = (field, value) => {
    setFormData((prev) => ({
      ...prev,
      from_address: { ...prev.from_address, [field]: value },
    }));
  };

  const updateParcel = (field, value) => {
    setFormData((prev) => ({
      ...prev,
      parcel: { ...prev.parcel, [field]: parseFloat(value) || 0 },
    }));
  };

  const updateCarrier = (value) => {
    setFormData((prev) => ({ ...prev, carrier: value }));
  };

  const resetForm = () => {
    setFormData({
      to_address: { name: '', street1: '', city: '', state: '', zip: '', country: 'US' },
      from_address: { name: '', street1: '', city: '', state: '', zip: '', country: 'US' },
      parcel: { length: 10, width: 8, height: 5, weight: 2 },
      carrier: 'USPS',
    });
  };

  const isValid = () => {
    const { to_address, from_address, parcel } = formData;
    return (
      to_address.name &&
      to_address.street1 &&
      to_address.city &&
      to_address.state &&
      to_address.zip &&
      from_address.name &&
      from_address.street1 &&
      from_address.city &&
      from_address.state &&
      from_address.zip &&
      parcel.length > 0 &&
      parcel.width > 0 &&
      parcel.height > 0 &&
      parcel.weight > 0
    );
  };

  return {
    formData,
    updateToAddress,
    updateFromAddress,
    updateParcel,
    updateCarrier,
    resetForm,
    isValid,
  };
}
