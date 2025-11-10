import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import EmptyState from '../EmptyState';
import { Package } from 'lucide-react';

describe('EmptyState', () => {
  it('renders with title and description', () => {
    render(
      <EmptyState
        title="No items"
        description="Get started by creating your first item"
      />
    );

    expect(screen.getByText('No items')).toBeInTheDocument();
    expect(screen.getByText('Get started by creating your first item')).toBeInTheDocument();
  });

  it('renders with icon', () => {
    render(
      <EmptyState
        icon={Package}
        title="No items"
      />
    );

    // Icon should be rendered
    const icon = document.querySelector('svg');
    expect(icon).toBeInTheDocument();
  });

  it('renders primary action button', () => {
    const handleAction = vi.fn();

    render(
      <EmptyState
        title="No items"
        action={handleAction}
        actionLabel="Create Item"
      />
    );

    const button = screen.getByText('Create Item');
    expect(button).toBeInTheDocument();

    fireEvent.click(button);
    expect(handleAction).toHaveBeenCalledTimes(1);
  });

  it('renders secondary action button', () => {
    const handlePrimary = vi.fn();
    const handleSecondary = vi.fn();

    render(
      <EmptyState
        title="No items"
        action={handlePrimary}
        actionLabel="Create"
        secondaryAction={handleSecondary}
        secondaryActionLabel="Import"
      />
    );

    const createButton = screen.getByText('Create');
    const importButton = screen.getByText('Import');

    expect(createButton).toBeInTheDocument();
    expect(importButton).toBeInTheDocument();

    fireEvent.click(importButton);
    expect(handleSecondary).toHaveBeenCalledTimes(1);
  });

  it('uses default action label when not provided', () => {
    render(
      <EmptyState
        title="No items"
        action={vi.fn()}
      />
    );

    expect(screen.getByText('Get Started')).toBeInTheDocument();
  });

  it('applies custom className', () => {
    const { container } = render(
      <EmptyState
        title="No items"
        className="custom-class"
      />
    );

    const emptyStateDiv = container.querySelector('.custom-class');
    expect(emptyStateDiv).toBeInTheDocument();
  });

  it('renders without actions', () => {
    render(
      <EmptyState
        title="No items"
        description="Just a message"
      />
    );

    expect(screen.getByText('No items')).toBeInTheDocument();
    expect(screen.queryByRole('button')).not.toBeInTheDocument();
  });

  it('renders without description', () => {
    render(
      <EmptyState
        title="No items"
        action={vi.fn()}
        actionLabel="Create"
      />
    );

    expect(screen.getByText('No items')).toBeInTheDocument();
    expect(screen.getByText('Create')).toBeInTheDocument();
  });
});
