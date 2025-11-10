import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import EnhancedCard from '../EnhancedCard';
import { DollarSign } from 'lucide-react';

describe('EnhancedCard', () => {
  it('renders with title and description', () => {
    render(
      <EnhancedCard
        title="Revenue"
        description="Monthly total"
      />
    );

    expect(screen.getByText('Revenue')).toBeInTheDocument();
    expect(screen.getByText('Monthly total')).toBeInTheDocument();
  });

  it('renders with icon', () => {
    render(
      <EnhancedCard
        title="Revenue"
        icon={DollarSign}
      />
    );

    const icon = document.querySelector('svg');
    expect(icon).toBeInTheDocument();
  });

  it('renders children content', () => {
    render(
      <EnhancedCard title="Test">
        <div data-testid="child-content">Child content</div>
      </EnhancedCard>
    );

    expect(screen.getByTestId('child-content')).toBeInTheDocument();
    expect(screen.getByText('Child content')).toBeInTheDocument();
  });

  it('handles click events', () => {
    const handleClick = vi.fn();

    render(
      <EnhancedCard
        title="Clickable"
        onClick={handleClick}
      />
    );

    const card = screen.getByText('Clickable').closest('div').closest('div');
    fireEvent.click(card);

    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('applies gradient when enabled', () => {
    const { container } = render(
      <EnhancedCard
        title="Test"
        gradient={true}
      />
    );

    const gradient = container.querySelector('.bg-gradient-to-br');
    expect(gradient).toBeInTheDocument();
  });

  it('does not apply gradient when disabled', () => {
    const { container } = render(
      <EnhancedCard
        title="Test"
        gradient={false}
      />
    );

    const gradient = container.querySelector('.bg-gradient-to-br');
    expect(gradient).not.toBeInTheDocument();
  });

  it('applies custom className', () => {
    const { container } = render(
      <EnhancedCard
        title="Test"
        className="custom-class"
      />
    );

    expect(container.querySelector('.custom-class')).toBeInTheDocument();
  });

  it('renders without icon', () => {
    render(
      <EnhancedCard
        title="Test"
        description="Description"
      />
    );

    expect(screen.getByText('Test')).toBeInTheDocument();
    const icon = document.querySelector('.rounded-full.bg-primary\\/10');
    expect(icon).not.toBeInTheDocument();
  });

  it('renders without description', () => {
    render(
      <EnhancedCard
        title="Test"
      />
    );

    expect(screen.getByText('Test')).toBeInTheDocument();
  });

  it('has cursor-pointer when onClick provided', () => {
    const { container } = render(
      <EnhancedCard
        title="Test"
        onClick={vi.fn()}
      />
    );

    const card = container.querySelector('.cursor-pointer');
    expect(card).toBeInTheDocument();
  });
});
