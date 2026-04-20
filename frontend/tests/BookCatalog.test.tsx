import React from 'react';
import { render, screen } from '@testing-library/react';
import BookCatalog from '../src/components/BookCatalog';

test('renders book catalog with books', () => {
  const books = [
    { id: '1', title: 'Book 1', author: 'Author 1', price: 10, description: '', created_at: '2024-01-01T00:00:00Z', updated_at: '2024-01-01T00:00:00Z' },
    { id: '2', title: 'Book 2', author: 'Author 2', price: 20, description: '', created_at: '2024-01-01T00:00:00Z', updated_at: '2024-01-01T00:00:00Z' },
  ];
  render(<BookCatalog books={books} onEdit={jest.fn()} onDelete={jest.fn()} />);
  expect(screen.getByText(/Book 1/i)).toBeInTheDocument();
  expect(screen.getByText(/Book 2/i)).toBeInTheDocument();
});
