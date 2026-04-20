import React from 'react';
import { render, screen } from '@testing-library/react';
import Cart from '../src/components/Cart';

test('renders cart with items', () => {
  const cart = {
    user_id: 'u1',
    items: [
      { book_id: '1', quantity: 2 },
      { book_id: '2', quantity: 1 },
    ],
  };
  const books = [
    { id: '1', title: 'Book 1', author: 'Author 1', price: 10, description: '', created_at: '', updated_at: '' },
    { id: '2', title: 'Book 2', author: 'Author 2', price: 20, description: '', created_at: '', updated_at: '' },
  ];
  render(<Cart cart={cart} books={books} onRemove={jest.fn()} onCheckout={jest.fn()} />);
  expect(screen.getByText(/Book 1/i)).toBeInTheDocument();
  expect(screen.getByText(/Book 2/i)).toBeInTheDocument();
});
