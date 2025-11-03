import { useState, useRef } from 'react';
import { Upload, FileText, X, AlertCircle, CheckCircle } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/Table';

const REQUIRED_COLUMNS = ['name', 'street1', 'city', 'state', 'zip'];

export default function CSVUpload({ onUpload }) {
  const [file, setFile] = useState(null);
  const [data, setData] = useState([]);
  const [errors, setErrors] = useState([]);
  const [validRows, setValidRows] = useState(0);
  const fileInputRef = useRef(null);

  const validateRow = (row, index) => {
    const rowErrors = [];
    REQUIRED_COLUMNS.forEach((col) => {
      if (!row[col] || row[col].trim() === '') {
        rowErrors.push(`Row ${index + 2}: Missing '${col}'`);
      }
    });
    if (row.zip && !/^\d{5}(-\d{4})?$/.test(row.zip)) {
      rowErrors.push(`Row ${index + 2}: Invalid ZIP`);
    }
    return rowErrors;
  };

  const parseCSV = (text) => {
    const lines = text.split('\n').filter((line) => line.trim());
    if (lines.length < 2) return { data: [], errors: ['Empty CSV'] };

    const headers = lines[0].split(',').map((h) => h.trim().toLowerCase());
    const missing = REQUIRED_COLUMNS.filter((col) => !headers.includes(col));
    if (missing.length > 0) {
      return { data: [], errors: [`Missing columns: ${missing.join(', ')}`] };
    }

    const parsedData = [];
    const allErrors = [];

    for (let i = 1; i < lines.length; i++) {
      const values = lines[i].split(',').map((v) => v.trim());
      const row = {};
      headers.forEach((header, index) => {
        row[header] = values[index] || '';
      });

      const rowErrors = validateRow(row, i - 1);
      allErrors.push(...rowErrors);
      if (rowErrors.length === 0) parsedData.push(row);
    }

    return { data: parsedData, errors: allErrors };
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (!selectedFile) return;
    if (!selectedFile.name.endsWith('.csv')) {
      setErrors(['Please upload a CSV file']);
      return;
    }

    setFile(selectedFile);
    const reader = new FileReader();
    reader.onload = (event) => {
      const { data: parsedData, errors: parseErrors } = parseCSV(event.target.result);
      setData(parsedData);
      setErrors(parseErrors);
      setValidRows(parsedData.length);
    };
    reader.readAsText(selectedFile);
  };

  const handleRemove = () => {
    setFile(null);
    setData([]);
    setErrors([]);
    setValidRows(0);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const handleUpload = () => {
    if (data.length === 0) return;
    onUpload?.(data);
    handleRemove();
  };

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle>Upload CSV</CardTitle>
          <CardDescription>Required: {REQUIRED_COLUMNS.join(', ')}</CardDescription>
        </CardHeader>
        <CardContent>
          {!file ? (
            <div
              className="border-2 border-dashed rounded-lg p-12 text-center hover:border-primary cursor-pointer"
              onClick={() => fileInputRef.current?.click()}
            >
              <Upload className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
              <p className="text-lg font-medium">Click or drag CSV file</p>
              <input ref={fileInputRef} type="file" accept=".csv" onChange={handleFileChange} className="hidden" />
            </div>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center gap-3">
                  <FileText className="h-8 w-8 text-primary" />
                  <div>
                    <p className="font-medium">{file.name}</p>
                    <p className="text-sm text-muted-foreground">{(file.size / 1024).toFixed(2)} KB</p>
                  </div>
                </div>
                <Button variant="ghost" size="icon" onClick={handleRemove}><X className="h-4 w-4" /></Button>
              </div>

              <div className="grid gap-4 md:grid-cols-2">
                <Card>
                  <CardContent className="flex items-center gap-4 pt-6">
                    <CheckCircle className="h-8 w-8 text-green-600" />
                    <div>
                      <p className="text-2xl font-bold">{validRows}</p>
                      <p className="text-sm text-muted-foreground">Valid rows</p>
                    </div>
                  </CardContent>
                </Card>
                <Card>
                  <CardContent className="flex items-center gap-4 pt-6">
                    <AlertCircle className="h-8 w-8 text-red-600" />
                    <div>
                      <p className="text-2xl font-bold">{errors.length}</p>
                      <p className="text-sm text-muted-foreground">Errors</p>
                    </div>
                  </CardContent>
                </Card>
              </div>

              {errors.length > 0 && (
                <Card className="border-red-600/50">
                  <CardHeader><CardTitle className="text-red-600">Errors</CardTitle></CardHeader>
                  <CardContent>
                    <ul className="space-y-1 text-sm">
                      {errors.slice(0, 10).map((error, i) => <li key={i} className="text-red-600">• {error}</li>)}
                      {errors.length > 10 && <li className="italic">... {errors.length - 10} more</li>}
                    </ul>
                  </CardContent>
                </Card>
              )}

              <div className="flex justify-end gap-2">
                <Button variant="outline" onClick={handleRemove}>Cancel</Button>
                <Button onClick={handleUpload} disabled={data.length === 0}>
                  Upload {validRows} Address{validRows !== 1 ? 'es' : ''}
                </Button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {data.length > 0 && (
        <Card>
          <CardHeader><CardTitle>Preview (first 5)</CardTitle></CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Name</TableHead>
                  <TableHead>Address</TableHead>
                  <TableHead>City, State ZIP</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {data.slice(0, 5).map((row, i) => (
                  <TableRow key={i}>
                    <TableCell>{row.name}</TableCell>
                    <TableCell>{row.street1}</TableCell>
                    <TableCell>{row.city}, {row.state} {row.zip}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
            {data.length > 5 && <p className="text-sm text-muted-foreground mt-2">... {data.length - 5} more</p>}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
