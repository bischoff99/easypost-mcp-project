import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import DataTable from '../DataTable';

describe('DataTable', () => {
  const mockColumns = [
    { key: 'name', header: 'Name', sortable: true },
    { key: 'status', header: 'Status', sortable: true },
    { key: 'value', header: 'Value', sortable: false },
  ];

  const mockData = [
    { id: '1', name: 'Item 1', status: 'active', value: 100 },
    { id: '2', name: 'Item 2', status: 'pending', value: 200 },
    { id: '3', name: 'Item 3', status: 'active', value: 150 },
  ];

  it('renders table with data', () => {
    render(<DataTable columns={mockColumns} data={mockData} />);

    expect(screen.getByText('Name')).toBeInTheDocument();
    expect(screen.getByText('Status')).toBeInTheDocument();
    expect(screen.getByText('Item 1')).toBeInTheDocument();
    expect(screen.getByText('Item 2')).toBeInTheDocument();
  });

  it('displays search input', () => {
    render(<DataTable columns={mockColumns} data={mockData} searchPlaceholder="Search items..." />);

    const searchInput = screen.getByPlaceholderText('Search items...');
    expect(searchInput).toBeInTheDocument();
  });

  it('filters data based on search query', async () => {
    render(<DataTable columns={mockColumns} data={mockData} />);

    const searchInput = screen.getByPlaceholderText('Search...');
    fireEvent.change(searchInput, { target: { value: 'Item 1' } });

    await waitFor(() => {
      expect(screen.getByText('Item 1')).toBeInTheDocument();
      expect(screen.queryByText('Item 2')).not.toBeInTheDocument();
    });
  });

  it('sorts data when column header is clicked', async () => {
    render(<DataTable columns={mockColumns} data={mockData} />);

    const nameHeader = screen.getByText('Name').closest('button');
    fireEvent.click(nameHeader);

    // Should be sorted in ascending order
    const rows = screen.getAllByRole('row');
    expect(rows[1]).toHaveTextContent('Item 1');

    // Click again for descending
    fireEvent.click(nameHeader);
    await waitFor(() => {
      const rowsDesc = screen.getAllByRole('row');
      expect(rowsDesc[1]).toHaveTextContent('Item 3');
    });
  });

  it('handles row click', () => {
    const handleRowClick = vi.fn();
    render(<DataTable columns={mockColumns} data={mockData} onRowClick={handleRowClick} />);

    const firstRow = screen.getByText('Item 1').closest('tr');
    fireEvent.click(firstRow);

    expect(handleRowClick).toHaveBeenCalledWith(mockData[0]);
  });

  it('handles row selection', () => {
    const handleRowSelect = vi.fn();
    render(<DataTable columns={mockColumns} data={mockData} onRowSelect={handleRowSelect} />);

    const checkboxes = screen.getAllByRole('checkbox');
    fireEvent.click(checkboxes[1]); // First data row checkbox

    expect(handleRowSelect).toHaveBeenCalled();
  });

  it('displays loading state', () => {
    render(<DataTable columns={mockColumns} data={[]} isLoading={true} />);

    // Should show skeleton loaders
    const skeletons = document.querySelectorAll('.animate-pulse');
    expect(skeletons.length).toBeGreaterThan(0);
  });

  it('displays empty message when no data', () => {
    render(<DataTable columns={mockColumns} data={[]} emptyMessage="No items found" />);

    expect(screen.getByText('No items found')).toBeInTheDocument();
  });

  it('paginates data correctly', () => {
    const largeData = Array.from({ length: 25 }, (_, i) => ({
      id: String(i + 1),
      name: `Item ${i + 1}`,
      status: 'active',
      value: i * 10,
    }));

    render(<DataTable columns={mockColumns} data={largeData} pageSize={10} />);

    // Should show first 10 items
    expect(screen.getByText('Item 1')).toBeInTheDocument();
    expect(screen.getByText('Item 10')).toBeInTheDocument();
    expect(screen.queryByText('Item 11')).not.toBeInTheDocument();

    // Click next page
    const nextButton = screen.getByText('Next');
    fireEvent.click(nextButton);

    expect(screen.getByText('Item 11')).toBeInTheDocument();
  });

  it('displays custom rendered cells', () => {
    const columnsWithRender = [
      {
        key: 'name',
        header: 'Name',
        render: (row) => <span data-testid="custom-cell">{row.name.toUpperCase()}</span>,
      },
    ];

    render(<DataTable columns={columnsWithRender} data={mockData} />);

    expect(screen.getByText('ITEM 1')).toBeInTheDocument();
    expect(screen.getByTestId('custom-cell')).toBeInTheDocument();
  });

  it('shows selected row count', () => {
    render(<DataTable columns={mockColumns} data={mockData} onRowSelect={vi.fn()} />);

    const checkboxes = screen.getAllByRole('checkbox');
    fireEvent.click(checkboxes[1]); // Select first row

    expect(screen.getByText(/1 row\(s\) selected/)).toBeInTheDocument();
  });
});
