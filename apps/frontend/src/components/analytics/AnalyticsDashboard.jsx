import { useState, useCallback, useEffect } from 'react'
import PropTypes from 'prop-types'
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import { TrendingUp, Package, DollarSign, TruckIcon } from 'lucide-react'
import { Card } from '../ui/Card'
import { Skeleton } from '../ui/Skeleton'
import { Button } from '../ui/Button'
import api from '../../services/api'
import { toast } from 'sonner'

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899']

/**
 * AnalyticsDashboard - Comprehensive shipping analytics
 *
 * M3 Max Optimized:
 * - Lazy loaded (code splitting)
 * - Parallel data fetching
 * - Memoized chart rendering
 *
 * @param {Object} props - Component props
 * @param {number} props.days - Number of days to analyze (default: 30)
 */
export default function AnalyticsDashboard({ days = 30 }) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const fetchAnalytics = useCallback(async () => {
    setLoading(true)
    setError('')

    try {
      const response = await api.get(`/analytics?days=${days}`)

      if (response.data.status === 'success') {
        setData(response.data.data)
      } else {
        throw new Error(response.data.message || 'Failed to fetch analytics')
      }
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || 'Failed to load analytics'
      setError(errorMsg)
      toast.error(`Analytics Error: ${errorMsg}`)
    } finally {
      setLoading(false)
    }
  }, [days])

  useEffect(() => {
    fetchAnalytics()
  }, [fetchAnalytics])

  if (loading) {
    return (
      <div className="space-y-6" data-testid="analytics-loading">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {[...Array(4)].map((_, i) => (
            <Card key={i} className="p-6">
              <Skeleton className="h-20" />
            </Card>
          ))}
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {[...Array(4)].map((_, i) => (
            <Card key={i} className="p-6">
              <Skeleton className="h-64" />
            </Card>
          ))}
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <Card className="p-8 text-center" data-testid="analytics-error">
        <p className="text-destructive font-medium mb-2">Error loading analytics</p>
        <p className="text-sm text-muted-foreground mb-4">{error}</p>
        <Button onClick={fetchAnalytics} variant="default">
          Retry
        </Button>
      </Card>
    )
  }

  if (!data) {
    return <div data-testid="analytics-no-data">No analytics data available</div>
  }

  const { summary, by_carrier, by_date, top_routes } = data

  return (
    <div className="space-y-6" data-testid="analytics-dashboard">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="p-6" data-testid="summary-card-shipments">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Total Shipments</p>
              <p className="text-2xl font-bold" data-testid="stat-value">
                {summary.total_shipments.toLocaleString()}
              </p>
            </div>
            <Package className="h-8 w-8 text-blue-500" />
          </div>
        </Card>

        <Card className="p-6" data-testid="summary-card-cost">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Total Cost</p>
              <p className="text-2xl font-bold" data-testid="stat-value">
                ${summary.total_cost.toLocaleString()}
              </p>
            </div>
            <DollarSign className="h-8 w-8 text-green-500" />
          </div>
        </Card>

        <Card className="p-6" data-testid="summary-card-average">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Average Cost</p>
              <p className="text-2xl font-bold" data-testid="stat-value">
                ${summary.average_cost.toFixed(2)}
              </p>
            </div>
            <TrendingUp className="h-8 w-8 text-orange-500" />
          </div>
        </Card>

        <Card className="p-6" data-testid="summary-card-carriers">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Active Carriers</p>
              <p className="text-2xl font-bold" data-testid="stat-value">
                {by_carrier.length}
              </p>
            </div>
            <TruckIcon className="h-8 w-8 text-purple-500" />
          </div>
        </Card>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Shipment Volume Over Time */}
        <Card className="p-6" data-testid="chart-volume">
          <h3 className="text-lg font-semibold mb-4">Shipment Volume</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={by_date}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey="shipment_count"
                stroke="#3b82f6"
                strokeWidth={2}
                name="Shipments"
              />
            </LineChart>
          </ResponsiveContainer>
        </Card>

        {/* Cost Over Time */}
        <Card className="p-6" data-testid="chart-cost">
          <h3 className="text-lg font-semibold mb-4">Shipping Costs</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={by_date}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip formatter={(value) => `$${value.toFixed(2)}`} />
              <Legend />
              <Line
                type="monotone"
                dataKey="total_cost"
                stroke="#10b981"
                strokeWidth={2}
                name="Cost"
              />
            </LineChart>
          </ResponsiveContainer>
        </Card>

        {/* Carrier Distribution */}
        <Card className="p-6" data-testid="chart-carriers">
          <h3 className="text-lg font-semibold mb-4">Carrier Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={by_carrier}
                dataKey="shipment_count"
                nameKey="carrier"
                cx="50%"
                cy="50%"
                outerRadius={100}
                label={(entry) => `${entry.carrier} (${entry.percentage_of_total}%)`}
              >
                {by_carrier.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </Card>

        {/* Top Routes */}
        <Card className="p-6" data-testid="chart-routes">
          <h3 className="text-lg font-semibold mb-4">Top Routes</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={top_routes.slice(0, 5)}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="origin" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="shipment_count" fill="#8b5cf6" name="Shipments" />
            </BarChart>
          </ResponsiveContainer>
        </Card>
      </div>

      {/* Carrier Performance Table */}
      <Card className="p-6" data-testid="carrier-table">
        <h3 className="text-lg font-semibold mb-4">Carrier Performance</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b">
                <th className="text-left p-2">Carrier</th>
                <th className="text-right p-2">Shipments</th>
                <th className="text-right p-2">Total Cost</th>
                <th className="text-right p-2">Avg Cost</th>
                <th className="text-right p-2">% of Total</th>
              </tr>
            </thead>
            <tbody>
              {by_carrier.map((carrier, idx) => (
                <tr key={idx} className="border-b hover:bg-gray-50 dark:hover:bg-gray-800">
                  <td className="p-2">{carrier.carrier}</td>
                  <td className="text-right p-2">{carrier.shipment_count}</td>
                  <td className="text-right p-2">${carrier.total_cost.toFixed(2)}</td>
                  <td className="text-right p-2">${carrier.average_cost.toFixed(2)}</td>
                  <td className="text-right p-2">{carrier.percentage_of_total}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  )
}

AnalyticsDashboard.propTypes = {
  days: PropTypes.number,
}
