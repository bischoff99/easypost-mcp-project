/**
 * Template: React Component
 * Usage: Copy pattern for new components
 * 
 * Replace:
 * - ComponentName: Your component name (PascalCase)
 * - Props: Component props interface
 */

import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';

export default function ComponentName({ prop1, prop2, onAction }) {
  const [state, setState] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const data = await api.getData();
        setState(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [prop1]);

  const handleAction = async () => {
    setLoading(true);
    try {
      await onAction();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="animate-spin">Loading...</div>;
  if (error) return <div className="text-red-500">Error: {error}</div>;

  return (
    <Card>
      <CardHeader>
        <CardTitle>Component Title</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <p>{prop1}</p>
          <Button onClick={handleAction}>Action</Button>
        </div>
      </CardContent>
    </Card>
  );
}

ComponentName.propTypes = {
  prop1: PropTypes.string.isRequired,
  prop2: PropTypes.number,
  onAction: PropTypes.func.isRequired,
};

ComponentName.defaultProps = {
  prop2: 0,
};
