import React, { useState, useEffect } from 'react';
import { shipmentAPI } from '../services/api';
import { useShipmentForm } from '../hooks/useShipmentForm';
import ShipmentForm from './ShipmentForm';
import './Dashboard.css';

export default function Dashboard() {
  const [shipment, setShipment] = useState(null);
  const [tracking, setTracking] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [serverStatus, setServerStatus] = useState('checking');
  const shipmentForm = useShipmentForm();

  // Check server health on mount
  useEffect(() => {
    checkServerHealth();
  }, []);

  const checkServerHealth = async () => {
    try {
      await shipmentAPI.healthCheck();
      setServerStatus('online');
    } catch (err) {
      setServerStatus('offline');
      setError('Backend server is not running. Please start it first.');
    }
  };

  const handleCreateShipment = async (e) => {
    e.preventDefault();

    if (!shipmentForm.isValid()) {
      setError('Please fill in all required fields');
      return;
    }

    setLoading(true);
    setError('');
    try {
      const result = await shipmentAPI.createShipment(shipmentForm.formData);
      setShipment(result);
      shipmentForm.resetForm();
    } catch (err) {
      setError(err.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleFormUpdate = (type, field, value) => {
    if (type === 'to') {
      shipmentForm.updateToAddress(field, value);
    } else if (type === 'from') {
      shipmentForm.updateFromAddress(field, value);
    } else if (type === 'parcel') {
      shipmentForm.updateParcel(field, value);
    } else if (type === 'carrier') {
      shipmentForm.updateCarrier(value);
    }
  };

  const handleGetTracking = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    const trackingNumber = e.target.elements.trackingNumber.value;
    try {
      const result = await shipmentAPI.getTracking(trackingNumber);
      setTracking(result);
    } catch (err) {
      setError(err.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard">
      <h1>EasyPost Shipping Dashboard</h1>

      <div className={`status-badge ${serverStatus}`}>
        Server: {serverStatus === 'online' ? '✓ Online' : '✗ Offline'}
      </div>

      {error && <div className="error">{error}</div>}

      <section>
        <h2>Create Shipment</h2>
        <ShipmentForm
          formData={shipmentForm.formData}
          onUpdate={handleFormUpdate}
          onSubmit={handleCreateShipment}
          loading={loading}
          disabled={serverStatus === 'offline'}
        />

        {shipment && shipment.status === 'success' && shipment.data && (
          <div className="card">
            <h3>✓ Shipment Created</h3>
            <p><strong>ID:</strong> {shipment.data.shipment_id}</p>
            <p><strong>Tracking:</strong> {shipment.data.tracking_number}</p>
            <p><strong>Rate:</strong> ${shipment.data.rate}</p>
            <p><strong>Carrier:</strong> {shipment.data.carrier}</p>
            {shipment.data.label_url && (
              <a href={shipment.data.label_url} target="_blank" rel="noreferrer" className="btn-primary">
                Download Label
              </a>
            )}
          </div>
        )}
      </section>

      <section>
        <h2>Track Shipment</h2>
        <form onSubmit={handleGetTracking}>
          <input
            type="text"
            name="trackingNumber"
            placeholder="Enter tracking number"
            required
            disabled={loading || serverStatus === 'offline'}
          />
          <button type="submit" disabled={loading || serverStatus === 'offline'}>
            {loading ? 'Loading...' : 'Track Shipment'}
          </button>
        </form>

        {tracking && tracking.status === 'success' && tracking.data && (
          <div className="card">
            <h3>📦 Tracking Info</h3>
            <p><strong>Status:</strong> {tracking.data.status_detail}</p>
            <p><strong>Last Updated:</strong> {tracking.data.updated_at}</p>
            {tracking.data.events && tracking.data.events.length > 0 && (
              <div className="events">
                <h4>Events:</h4>
                <ul>
                  {tracking.data.events.map((event, i) => (
                    <li key={i}>
                      <span className="timestamp">{event.timestamp}</span>
                      <span className="message">{event.message}</span>
                      {event.location && <span className="location">({event.location})</span>}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </section>
    </div>
  );
}
