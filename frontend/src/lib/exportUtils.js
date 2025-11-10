/**
/**
 * Utility functions for exporting data in various formats
 */

/**
 * Convert array of objects to CSV string
 * @param {Array} data - Array of objects to export
 * @param {Array} headers - Array of header objects with key and label
 * @returns {string} CSV formatted string
 */
export function arrayToCSV(data, headers = null) {
  if (!data || data.length === 0) return '';

  // If no headers provided, use object keys from first item
  if (!headers) {
    const firstItem = data[0];
    headers = Object.keys(firstItem).map((key) => ({
      key,
      label: key.charAt(0).toUpperCase() + key.slice(1).replace(/_/g, ' '),
    }));
  }

  // Create CSV header row
  const headerRow = headers.map((h) => `"${h.label.replace(/"/g, '""')}"`).join(',');

  // Create CSV data rows
  const dataRows = data.map((item) =>
    headers
      .map((header) => {
        const value = item[header.key];
        if (value === null || value === undefined) return '';

        // Handle different data types
        let csvValue = String(value);

        // Format dates
        if (header.key.includes('date') || header.key.includes('created_at')) {
          try {
            const date = new Date(value);
            if (!isNaN(date.getTime())) {
              csvValue = date.toLocaleDateString();
            }
          } catch {
            // Keep original value if date parsing fails
          }
        }

        // Format currency
        if (header.key === 'cost' || header.key === 'rate') {
          const numValue = parseFloat(value);
          if (!isNaN(numValue)) {
            csvValue = `$${numValue.toFixed(2)}`;
          }
        }

        // Escape quotes and wrap in quotes
        csvValue = csvValue.replace(/"/g, '""');
        return `"${csvValue}"`;
      })
      .join(',')
  );

  return [headerRow, ...dataRows].join('\n');
}

/**
 * Download data as CSV file
 * @param {Array} data - Array of objects to export
 * @param {string} filename - Name of the file (without extension)
 * @param {Array} headers - Optional headers configuration
 */
export function downloadCSV(data, filename = 'export', headers = null) {
  const csvContent = arrayToCSV(data, headers);
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });

  // Create download link
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);
  link.setAttribute('href', url);
  link.setAttribute('download', `${filename}.csv`);
  link.style.visibility = 'hidden';

  // Trigger download
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);

  // Clean up
  URL.revokeObjectURL(url);
}

/**
 * Get headers configuration for shipments export
 * @returns {Array} Headers configuration
 */
export function getShipmentExportHeaders() {
  return [
    { key: 'id', label: 'Shipment ID' },
    { key: 'tracking_number', label: 'Tracking Number' },
    { key: 'status', label: 'Status' },
    { key: 'carrier', label: 'Carrier' },
    { key: 'service', label: 'Service' },
    { key: 'from', label: 'From' },
    { key: 'to', label: 'To' },
    { key: 'cost', label: 'Cost' },
    { key: 'created_at', label: 'Created Date' },
  ];
}

/**
 * Export shipments data to CSV
 * @param {Array} shipments - Array of shipment objects
 * @param {string} filename - Optional filename
 */
export function exportShipmentsToCSV(shipments, filename = 'shipments') {
  const headers = getShipmentExportHeaders();
  downloadCSV(shipments, filename, headers);
}

/**
 * Export selected shipments to CSV
 * @param {Array} allShipments - All available shipments
 * @param {Set} selectedIds - Set of selected shipment IDs
 * @param {string} filename - Optional filename
 */
export function exportSelectedShipmentsToCSV(
  allShipments,
  selectedIds,
  filename = 'selected-shipments'
) {
  const selectedShipments = allShipments.filter((shipment) => selectedIds.has(shipment.id));
  exportShipmentsToCSV(selectedShipments, filename);
}
