import React from 'react';
import { render, screen } from '@testing-library/react';
import RestaurantList from '../src/components/RestaurantList';

test('renders restaurant list', () => {
  const restaurants = [
    { id: '1', name: 'Testaurant', address: '1 Food St', contact: '1234567890', hours: '9-9', rating: 4.5, menu: [], created_at: '2024-01-01T00:00:00Z', updated_at: '2024-01-01T00:00:00Z' },
  ];
  render(<RestaurantList restaurants={restaurants} onSelect={jest.fn()} />);
  expect(screen.getByText(/Testaurant/i)).toBeInTheDocument();
});
