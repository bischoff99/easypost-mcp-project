import { render, screen, fireEvent } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import { Plus } from 'lucide-react'
import QuickActionCard from './QuickActionCard'

describe('QuickActionCard', () => {
  it('renders with all props', () => {
    const handleClick = vi.fn()

    render(
      <QuickActionCard
        title="Create Shipment"
        description="Create a new shipping label"
        icon={Plus}
        onClick={handleClick}
        delay={0}
        color="primary"
      />
    )

    expect(screen.getByText('Create Shipment')).toBeInTheDocument()
    expect(screen.getByText('Create a new shipping label')).toBeInTheDocument()
  })

  it('calls onClick when clicked', () => {
    const handleClick = vi.fn()

    render(
      <QuickActionCard
        title="Create Shipment"
        description="Create a new shipping label"
        icon={Plus}
        onClick={handleClick}
      />
    )

    const card = screen.getByText('Create Shipment').closest('.cursor-pointer')
    fireEvent.click(card)

    expect(handleClick).toHaveBeenCalledOnce()
  })

  it('renders different color variants', () => {
    const handleClick = vi.fn()

    const { rerender } = render(
      <QuickActionCard
        title="Test"
        description="Test description"
        icon={Plus}
        onClick={handleClick}
        color="primary"
      />
    )

    // Test that it renders without error for each color
    rerender(
      <QuickActionCard
        title="Test"
        description="Test description"
        icon={Plus}
        onClick={handleClick}
        color="secondary"
      />
    )

    rerender(
      <QuickActionCard
        title="Test"
        description="Test description"
        icon={Plus}
        onClick={handleClick}
        color="accent"
      />
    )

    expect(screen.getByText('Test')).toBeInTheDocument()
  })
})
