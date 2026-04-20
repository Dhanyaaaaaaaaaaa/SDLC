import React from 'react';
import { render, screen } from '@testing-library/react';
import OrderHistory from '../src/components/OrderHistory';

test('renders order history', () => {
  const orders = [
    { id: '1', user_id: 'u1', items: [{ book_id: '1', quantity: 1 }], total: 10, status: 'confirmed', created_at: '2024-01-01T00:00:00Z' },
  ];
  render(<OrderHistory orders={orders} />);
  expect(screen.getByText(/Order #1/i)).toBeInTheDocument();
  expect(screen.getByText(/confirmed/i)).toBeInTheDocument();
});
