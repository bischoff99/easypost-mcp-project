import { renderHook, act } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { useShipmentForm } from './useShipmentForm';

describe('useShipmentForm', () => {
  it('should initialize with default structure', () => {
    const { result } = renderHook(() => useShipmentForm());

    expect(result.current.formData).toBeDefined();
    expect(result.current.formData.to_address).toBeDefined();
    expect(result.current.formData.from_address).toBeDefined();
    expect(result.current.formData.parcel).toBeDefined();
    expect(result.current.formData.carrier).toBe('USPS');
  });

  it('should update to_address fields', () => {
    const { result } = renderHook(() => useShipmentForm());

    act(() => {
      result.current.updateToAddress('name', 'John Doe');
    });

    expect(result.current.formData.to_address.name).toBe('John Doe');
  });

  it('should update from_address fields', () => {
    const { result } = renderHook(() => useShipmentForm());

    act(() => {
      result.current.updateFromAddress('street1', '123 Main St');
    });

    expect(result.current.formData.from_address.street1).toBe('123 Main St');
  });

  it('should update parcel dimensions', () => {
    const { result } = renderHook(() => useShipmentForm());

    act(() => {
      result.current.updateParcel('weight', '5');
    });

    expect(result.current.formData.parcel.weight).toBe(5);
  });

  it('should validate form completeness', () => {
    const { result } = renderHook(() => useShipmentForm());

    // Initially incomplete (empty addresses)
    expect(result.current.isValid()).toBeFalsy();

    // Fill required fields
    act(() => {
      result.current.updateToAddress('name', 'John Doe');
      result.current.updateToAddress('street1', '123 Main St');
      result.current.updateToAddress('city', 'San Francisco');
      result.current.updateToAddress('state', 'CA');
      result.current.updateToAddress('zip', '94102');

      result.current.updateFromAddress('name', 'Jane Smith');
      result.current.updateFromAddress('street1', '456 Oak Ave');
      result.current.updateFromAddress('city', 'Los Angeles');
      result.current.updateFromAddress('state', 'CA');
      result.current.updateFromAddress('zip', '90001');
    });

    // Should be valid now
    expect(result.current.isValid()).toBe(true);
  });

  it('should reset form to defaults', () => {
    const { result } = renderHook(() => useShipmentForm());

    // Modify some fields
    act(() => {
      result.current.updateToAddress('name', 'John Doe');
      result.current.updateParcel('weight', '10');
    });

    expect(result.current.formData.to_address.name).toBe('John Doe');
    expect(result.current.formData.parcel.weight).toBe(10);

    // Reset
    act(() => {
      result.current.resetForm();
    });

    expect(result.current.formData.to_address.name).toBe('');
    expect(result.current.formData.parcel.weight).toBe(2); // default weight
  });

  it('should update carrier', () => {
    const { result } = renderHook(() => useShipmentForm());

    act(() => {
      result.current.updateCarrier('FedEx');
    });

    expect(result.current.formData.carrier).toBe('FedEx');
  });
});
