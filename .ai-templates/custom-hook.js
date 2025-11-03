/**
 * Template: Custom React Hook
 * Usage: Copy pattern for new hooks
 * 
 * Replace:
 * - HookName: Your hook name (useSomething)
 * - State: State variables
 * - Logic: Hook logic
 */

import { useState, useEffect, useCallback } from 'react';
import { toast } from 'sonner';
import api from '@/services/api';

export const useHookName = (initialValue) => {
  const [data, setData] = useState(initialValue);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch data
  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await api.get('/endpoint');
      setData(result.data);
      return result.data;
    } catch (err) {
      const message = err.message || 'Failed to fetch data';
      setError(message);
      toast.error('Error', { description: message });
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  // Update data
  const updateData = useCallback(async (newData) => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await api.post('/endpoint', newData);
      setData(result.data);
      toast.success('Updated successfully');
      return result.data;
    } catch (err) {
      const message = err.message || 'Failed to update';
      setError(message);
      toast.error('Error', { description: message });
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  // Reset
  const reset = useCallback(() => {
    setData(initialValue);
    setError(null);
  }, [initialValue]);

  // Auto-fetch on mount
  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return {
    data,
    loading,
    error,
    fetchData,
    updateData,
    reset,
  };
};
