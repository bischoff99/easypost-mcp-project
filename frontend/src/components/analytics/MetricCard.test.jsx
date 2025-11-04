import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { Package } from 'lucide-react';
import MetricCard from './MetricCard';

describe('MetricCard', () => {
  it('renders with all props', () => {
    render(
      <MetricCard
        title="Revenue"
        value="$12,456"
        change="+8.1%"
        trend="up"
        icon={Package}
        color="primary"
        delay={0}
      />
    );

    expect(screen.getByText('Revenue')).toBeInTheDocument();
    expect(screen.getByText('$12,456')).toBeInTheDocument();
    expect(screen.getByText('+8.1%')).toBeInTheDocument();
  });

  it('shows trending up when trend is up', () => {
    render(
      <MetricCard
        title="Test"
        value="100"
        change="+10%"
        trend="up"
        icon={Package}
      />
    );

    const changeText = screen.getByText('+10%');
    expect(changeText).toHaveClass('text-green-600');
  });

  it('shows trending down when trend is down', () => {
    render(
      <MetricCard
        title="Test"
        value="100"
        change="-5%"
        trend="down"
        icon={Package}
      />
    );

    const changeText = screen.getByText('-5%');
    expect(changeText).toHaveClass('text-red-600');
  });

  it('renders different color variants', () => {
    const { rerender } = render(
      <MetricCard
        title="Test"
        value="100"
        change="+5%"
        trend="up"
        icon={Package}
        color="primary"
      />
    );

    expect(screen.getByText('Test')).toBeInTheDocument();

    // Test all color variants
    ['secondary', 'success', 'warning'].forEach(color => {
      rerender(
        <MetricCard
          title="Test"
          value="100"
          change="+5%"
          trend="up"
          icon={Package}
          color={color}
        />
      );
      expect(screen.getByText('Test')).toBeInTheDocument();
    });
  });
});
