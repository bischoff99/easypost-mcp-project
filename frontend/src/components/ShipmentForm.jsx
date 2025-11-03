import React from 'react';
import './ShipmentForm.css';

export default function ShipmentForm({ formData, onUpdate, onSubmit, loading, disabled }) {
  const { to_address, from_address, parcel, carrier } = formData;

  const handleAddressChange = (type, field, value) => {
    onUpdate(type, field, value);
  };

  const handleParcelChange = (field, value) => {
    onUpdate('parcel', field, value);
  };

  const handleCarrierChange = (value) => {
    onUpdate('carrier', null, value);
  };

  return (
    <form className="shipment-form" onSubmit={onSubmit}>
      <div className="form-section">
        <h3>From Address</h3>
        <input
          type="text"
          placeholder="Name"
          value={from_address.name}
          onChange={(e) => handleAddressChange('from', 'name', e.target.value)}
          required
          disabled={disabled}
        />
        <input
          type="text"
          placeholder="Street Address"
          value={from_address.street1}
          onChange={(e) => handleAddressChange('from', 'street1', e.target.value)}
          required
          disabled={disabled}
        />
        <div className="form-row">
          <input
            type="text"
            placeholder="City"
            value={from_address.city}
            onChange={(e) => handleAddressChange('from', 'city', e.target.value)}
            required
            disabled={disabled}
          />
          <input
            type="text"
            placeholder="State"
            value={from_address.state}
            onChange={(e) => handleAddressChange('from', 'state', e.target.value)}
            maxLength="2"
            required
            disabled={disabled}
          />
          <input
            type="text"
            placeholder="ZIP"
            value={from_address.zip}
            onChange={(e) => handleAddressChange('from', 'zip', e.target.value)}
            required
            disabled={disabled}
          />
        </div>
      </div>

      <div className="form-section">
        <h3>To Address</h3>
        <input
          type="text"
          placeholder="Name"
          value={to_address.name}
          onChange={(e) => handleAddressChange('to', 'name', e.target.value)}
          required
          disabled={disabled}
        />
        <input
          type="text"
          placeholder="Street Address"
          value={to_address.street1}
          onChange={(e) => handleAddressChange('to', 'street1', e.target.value)}
          required
          disabled={disabled}
        />
        <div className="form-row">
          <input
            type="text"
            placeholder="City"
            value={to_address.city}
            onChange={(e) => handleAddressChange('to', 'city', e.target.value)}
            required
            disabled={disabled}
          />
          <input
            type="text"
            placeholder="State"
            value={to_address.state}
            onChange={(e) => handleAddressChange('to', 'state', e.target.value)}
            maxLength="2"
            required
            disabled={disabled}
          />
          <input
            type="text"
            placeholder="ZIP"
            value={to_address.zip}
            onChange={(e) => handleAddressChange('to', 'zip', e.target.value)}
            required
            disabled={disabled}
          />
        </div>
      </div>

      <div className="form-section">
        <h3>Package Details</h3>
        <div className="form-row">
          <input
            type="number"
            placeholder="Length (in)"
            value={parcel.length}
            onChange={(e) => handleParcelChange('length', e.target.value)}
            min="0.1"
            step="0.1"
            required
            disabled={disabled}
          />
          <input
            type="number"
            placeholder="Width (in)"
            value={parcel.width}
            onChange={(e) => handleParcelChange('width', e.target.value)}
            min="0.1"
            step="0.1"
            required
            disabled={disabled}
          />
          <input
            type="number"
            placeholder="Height (in)"
            value={parcel.height}
            onChange={(e) => handleParcelChange('height', e.target.value)}
            min="0.1"
            step="0.1"
            required
            disabled={disabled}
          />
          <input
            type="number"
            placeholder="Weight (oz)"
            value={parcel.weight}
            onChange={(e) => handleParcelChange('weight', e.target.value)}
            min="0.1"
            step="0.1"
            required
            disabled={disabled}
          />
        </div>
      </div>

      <div className="form-section">
        <h3>Carrier</h3>
        <select
          value={carrier}
          onChange={(e) => handleCarrierChange(e.target.value)}
          disabled={disabled}
        >
          <option value="USPS">USPS</option>
          <option value="FedEx">FedEx</option>
          <option value="UPS">UPS</option>
        </select>
      </div>

      <button type="submit" disabled={loading || disabled} className="btn-primary">
        {loading ? 'Creating Shipment...' : 'Create Shipment'}
      </button>
    </form>
  );
}

