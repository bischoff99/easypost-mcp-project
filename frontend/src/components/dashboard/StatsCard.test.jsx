import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { Package } from 'lucide-react';
import StatsCard from './StatsCard';

describe('StatsCard', () => {
  it('renders with all props', () => {
    render(
      <StatsCard
        title="Total Shipments"
        value="2,456"
        change="+12.5%"
        trend="up"
        icon={Package}
        delay={0}
      />
    );

    expect(screen.getByText('Total Shipments')).toBeInTheDocument();
    expect(screen.getByText('2,456')).toBeInTheDocument();
    expect(screen.getByText('+12.5% from last month')).toBeInTheDocument();
  });

  it('shows trending up icon when trend is up', () => {
    const { container } = render(
      <StatsCard
        title="Test"
        value="100"
        change="+10%"
        trend="up"
        icon={Package}
      />
    );

    // Check for green color class (trending up)
    const changeText = screen.getByText('+10% from last month');
    expect(changeText).toHaveClass('text-green-600');
  });

  it('shows trending down icon when trend is down', () => {
    const { container } = render(
      <StatsCard
        title="Test"
        value="100"
        change="-5%"
        trend="down"
        icon={Package}
      />
    );

    // Check for red color class (trending down)
    const changeText = screen.getByText('-5% from last month');
    expect(changeText).toHaveClass('text-red-600');
  });
});
