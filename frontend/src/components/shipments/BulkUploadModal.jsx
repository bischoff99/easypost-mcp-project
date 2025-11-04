import { useState, useRef } from 'react';
import { X, Upload, FileText, CheckCircle, AlertCircle, Download } from 'lucide-react';
import { toast } from 'sonner';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { shipmentAPI } from '@/services/api';

/**
 * BulkUploadModal Component
 *
 * Bulk shipment creation with CSV upload:
 * 1. Upload CSV file (drag & drop or click)
 * 2. Preview & validate data
 * 3. Process shipments in parallel
 * 4. Show results with error report
 *
 * M3 Max Optimized: 32 concurrent API calls
 */

export default function BulkUploadModal({ isOpen, onClose, onSuccess }) {
  const [step, setStep] = useState(1);
  const [file, setFile] = useState(null);
  const [csvData, setCsvData] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [results, setResults] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileSelect = (selectedFile) => {
    if (!selectedFile) return;

    if (!selectedFile.name.endsWith('.csv')) {
      toast.error('Invalid file type', {
        description: 'Please upload a CSV file',
      });
      return;
    }

    setFile(selectedFile);

    // Parse CSV
    const reader = new FileReader();
    reader.onload = (e) => {
      const text = e.target.result;
      const lines = text.split('\n').filter((line) => line.trim());

      if (lines.length < 2) {
        toast.error('Empty CSV', {
          description: 'CSV file must contain headers and at least one row',
        });
        return;
      }

      // Parse headers and data
      const headers = lines[0].split(',').map((h) => h.trim());
      const data = lines.slice(1).map((line, index) => {
        const values = line.split(',').map((v) => v.trim());
        const row = { _index: index + 1 };
        headers.forEach((header, i) => {
          row[header] = values[i] || '';
        });
        return row;
      });

      setCsvData(data);
      setStep(2);
      toast.success('CSV Loaded', {
        description: `Found ${data.length} shipment${data.length > 1 ? 's' : ''}`,
      });
    };

    reader.onerror = () => {
      toast.error('Failed to read file');
    };

    reader.readAsText(selectedFile);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFile = e.dataTransfer.files[0];
    handleFileSelect(droppedFile);
  };

  const handleProcessBulk = async () => {
    try {
      setIsProcessing(true);
      setProgress(0);
      setStep(3);

      // Transform CSV data to shipment format
      const shipments = csvData.map((row) => ({
        from_address: {
          name: row.from_name || '',
          street1: row.from_street1 || '',
          city: row.from_city || '',
          state: row.from_state || '',
          zip: row.from_zip || '',
          country: row.from_country || 'US',
        },
        to_address: {
          name: row.to_name || '',
          street1: row.to_street1 || '',
          city: row.to_city || '',
          state: row.to_state || '',
          zip: row.to_zip || '',
          country: row.to_country || 'US',
        },
        parcel: {
          length: parseFloat(row.length) || 10,
          width: parseFloat(row.width) || 8,
          height: parseFloat(row.height) || 4,
          weight: parseFloat(row.weight) || 16,
        },
      }));

      // Call bulk endpoint (processes in parallel on backend)
      const response = await shipmentAPI.createBulkShipments(shipments, (progressPercent) => {
        setProgress(progressPercent);
      });

      if (response.status === 'success') {
        setResults(response.data);
        setStep(4);
        toast.success('Bulk Processing Complete!', {
          description: `${response.data.successful} of ${response.data.total} shipments created`,
        });
        onSuccess?.(response.data);
      } else {
        toast.error('Bulk processing failed', {
          description: response.message || 'Please try again',
        });
      }
    } catch (error) {
      toast.error('Error', {
        description: error.message || 'Failed to process shipments',
      });
    } finally {
      setIsProcessing(false);
    }
  };

  const handleDownloadErrors = () => {
    if (!results || !results.errors || results.errors.length === 0) return;

    // Create CSV with errors
    const headers = ['Row', 'Error'];
    const csvContent = [
      headers.join(','),
      ...results.errors.map((err) => `${err.index},${err.message}`),
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'bulk-upload-errors.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    toast.success('Error report downloaded');
  };

  const handleClose = () => {
    setStep(1);
    setFile(null);
    setCsvData([]);
    setProgress(0);
    setResults(null);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
      <Card className="w-full max-w-4xl max-h-[90vh] overflow-y-auto m-4">
        <div className="sticky top-0 bg-background border-b p-6 flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold">Bulk Upload Shipments</h2>
            <p className="text-sm text-muted-foreground">
              Step {step} of 4:{' '}
              {step === 1
                ? 'Upload CSV'
                : step === 2
                  ? 'Preview Data'
                  : step === 3
                    ? 'Processing'
                    : 'Results'}
            </p>
          </div>
          <Button variant="ghost" size="icon" onClick={handleClose}>
            <X className="h-5 w-5" />
          </Button>
        </div>

        <div className="p-6">
          {/* Step 1: Upload CSV */}
          {step === 1 && (
            <div className="space-y-6">
              <div
                className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
                  isDragging
                    ? 'border-primary bg-primary/5'
                    : 'border-border hover:border-primary/50'
                }`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
              >
                <Upload className="h-16 w-16 mx-auto mb-4 text-muted-foreground" />
                <h3 className="text-lg font-semibold mb-2">Upload CSV File</h3>
                <p className="text-sm text-muted-foreground mb-4">
                  Drag and drop your CSV file here, or click to browse
                </p>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".csv"
                  onChange={(e) => handleFileSelect(e.target.files[0])}
                  className="hidden"
                />
                <Button onClick={() => fileInputRef.current?.click()}>Browse Files</Button>
              </div>

              <div className="bg-muted/50 rounded-lg p-4">
                <h4 className="font-semibold mb-2 flex items-center gap-2">
                  <FileText className="h-4 w-4" />
                  CSV Format Requirements
                </h4>
                <p className="text-sm text-muted-foreground mb-2">
                  Your CSV file should include the following columns:
                </p>
                <code className="text-xs block bg-background p-3 rounded">
                  from_name, from_street1, from_city, from_state, from_zip, from_country,
                  <br />
                  to_name, to_street1, to_city, to_state, to_zip, to_country,
                  <br />
                  length, width, height, weight
                </code>
              </div>
            </div>
          )}

          {/* Step 2: Preview Data */}
          {step === 2 && (
            <div className="space-y-6">
              <div className="bg-muted/50 rounded-lg p-4">
                <h3 className="font-semibold mb-2">Preview</h3>
                <p className="text-sm text-muted-foreground">
                  {csvData.length} shipment{csvData.length > 1 ? 's' : ''} ready to process
                </p>
              </div>

              <div className="border rounded-lg overflow-x-auto max-h-96">
                <table className="w-full text-sm">
                  <thead className="bg-muted">
                    <tr>
                      <th className="p-2 text-left">#</th>
                      <th className="p-2 text-left">To Name</th>
                      <th className="p-2 text-left">To City</th>
                      <th className="p-2 text-left">To State</th>
                      <th className="p-2 text-left">Weight (oz)</th>
                    </tr>
                  </thead>
                  <tbody>
                    {csvData.slice(0, 10).map((row, index) => (
                      <tr key={index} className="border-t">
                        <td className="p-2">{row._index}</td>
                        <td className="p-2">{row.to_name}</td>
                        <td className="p-2">{row.to_city}</td>
                        <td className="p-2">{row.to_state}</td>
                        <td className="p-2">{row.weight}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                {csvData.length > 10 && (
                  <div className="p-2 text-center text-sm text-muted-foreground bg-muted/50">
                    ... and {csvData.length - 10} more
                  </div>
                )}
              </div>

              <div className="flex justify-between">
                <Button variant="outline" onClick={() => setStep(1)}>
                  Back
                </Button>
                <Button onClick={handleProcessBulk} disabled={isProcessing}>
                  Process {csvData.length} Shipment{csvData.length > 1 ? 's' : ''}
                </Button>
              </div>
            </div>
          )}

          {/* Step 3: Processing */}
          {step === 3 && (
            <div className="space-y-6 py-12">
              <div className="text-center">
                <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary/10 mb-4 animate-pulse">
                  <Upload className="h-8 w-8 text-primary" />
                </div>
                <h3 className="text-xl font-semibold mb-2">Processing Shipments...</h3>
                <p className="text-muted-foreground mb-6">
                  Creating {csvData.length} shipments in parallel
                </p>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Progress</span>
                  <span>{progress}%</span>
                </div>
                <div className="w-full bg-muted rounded-full h-2 overflow-hidden">
                  <div
                    className="bg-primary h-full transition-all duration-300"
                    style={{ width: `${progress}%` }}
                  />
                </div>
              </div>

              <p className="text-sm text-center text-muted-foreground">
                ⚡ M3 Max: Processing up to 32 shipments simultaneously
              </p>
            </div>
          )}

          {/* Step 4: Results */}
          {step === 4 && results && (
            <div className="space-y-6">
              <div className="grid grid-cols-3 gap-4">
                <Card className="p-4 bg-success/10 border-success/20">
                  <div className="flex items-center gap-3">
                    <CheckCircle className="h-8 w-8 text-success" />
                    <div>
                      <div className="text-2xl font-bold">{results.successful}</div>
                      <div className="text-sm text-muted-foreground">Successful</div>
                    </div>
                  </div>
                </Card>

                <Card className="p-4 bg-destructive/10 border-destructive/20">
                  <div className="flex items-center gap-3">
                    <AlertCircle className="h-8 w-8 text-destructive" />
                    <div>
                      <div className="text-2xl font-bold">{results.failed}</div>
                      <div className="text-sm text-muted-foreground">Failed</div>
                    </div>
                  </div>
                </Card>

                <Card className="p-4 bg-primary/10 border-primary/20">
                  <div className="flex items-center gap-3">
                    <FileText className="h-8 w-8 text-primary" />
                    <div>
                      <div className="text-2xl font-bold">{results.total}</div>
                      <div className="text-sm text-muted-foreground">Total</div>
                    </div>
                  </div>
                </Card>
              </div>

              {results.errors && results.errors.length > 0 && (
                <div className="border rounded-lg p-4 bg-destructive/5">
                  <h4 className="font-semibold mb-2 flex items-center gap-2">
                    <AlertCircle className="h-4 w-4" />
                    Errors ({results.errors.length})
                  </h4>
                  <div className="space-y-1 max-h-48 overflow-y-auto">
                    {results.errors.slice(0, 5).map((error, index) => (
                      <div key={index} className="text-sm">
                        <span className="font-medium">Row {error.index}:</span> {error.message}
                      </div>
                    ))}
                    {results.errors.length > 5 && (
                      <div className="text-sm text-muted-foreground">
                        ... and {results.errors.length - 5} more errors
                      </div>
                    )}
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    className="mt-3"
                    onClick={handleDownloadErrors}
                  >
                    <Download className="h-4 w-4 mr-2" />
                    Download Error Report
                  </Button>
                </div>
              )}

              <div className="flex justify-end gap-2">
                <Button variant="outline" onClick={handleClose}>
                  Close
                </Button>
                <Button onClick={() => window.location.reload()}>View Shipments</Button>
              </div>
            </div>
          )}
        </div>
      </Card>
    </div>
  );
}
