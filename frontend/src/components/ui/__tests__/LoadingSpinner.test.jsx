import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { LoadingSpinner, LoadingOverlay, SkeletonLoader } from '../LoadingSpinner';

describe('LoadingSpinner', () => {
  it('renders with default props', () => {
    const { container } = render(<LoadingSpinner />);
    const spinner = container.querySelector('div');

    expect(spinner).toBeInTheDocument();
    expect(spinner).toHaveClass('rounded-full');
  });

  it('renders with different sizes', () => {
    const { container: small } = render(<LoadingSpinner size="sm" />);
    const { container: large } = render(<LoadingSpinner size="lg" />);

    expect(small.querySelector('div')).toHaveClass('h-4', 'w-4');
    expect(large.querySelector('div')).toHaveClass('h-12', 'w-12');
  });

  it('renders with different variants', () => {
    const { container: primary } = render(<LoadingSpinner variant="primary" />);
    const { container: secondary } = render(<LoadingSpinner variant="secondary" />);

    expect(primary.querySelector('div')).toHaveClass('border-primary');
    expect(secondary.querySelector('div')).toHaveClass('border-secondary');
  });

  it('applies custom className', () => {
    const { container } = render(<LoadingSpinner className="custom-class" />);

    expect(container.querySelector('.custom-class')).toBeInTheDocument();
  });
});

describe('LoadingOverlay', () => {
  it('renders with default message', () => {
    render(<LoadingOverlay />);

    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('renders with custom message', () => {
    render(<LoadingOverlay message="Please wait..." />);

    expect(screen.getByText('Please wait...')).toBeInTheDocument();
  });

  it('renders without message', () => {
    render(<LoadingOverlay message="" />);

    expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
  });

  it('has fixed positioning', () => {
    const { container } = render(<LoadingOverlay />);
    const overlay = container.querySelector('div');

    expect(overlay).toHaveClass('fixed', 'inset-0');
  });
});

describe('SkeletonLoader', () => {
  it('renders single row by default', () => {
    const { container } = render(<SkeletonLoader />);
    const skeletons = container.querySelectorAll('.animate-pulse');

    expect(skeletons).toHaveLength(1);
  });

  it('renders multiple rows', () => {
    const { container } = render(<SkeletonLoader rows={5} />);
    const skeletons = container.querySelectorAll('.animate-pulse');

    expect(skeletons).toHaveLength(5);
  });

  it('applies custom className', () => {
    const { container } = render(<SkeletonLoader className="h-20" />);
    const skeleton = container.querySelector('.h-20');

    expect(skeleton).toBeInTheDocument();
  });

  it('has animation class', () => {
    const { container } = render(<SkeletonLoader />);
    const skeleton = container.querySelector('div > div');

    expect(skeleton).toHaveClass('animate-pulse');
  });
});
