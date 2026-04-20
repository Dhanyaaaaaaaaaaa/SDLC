import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../src/App';

test('renders main app and navigation', () => {
  render(<App />);
  expect(screen.getByText(/Dashboard/i)).toBeInTheDocument();
  expect(screen.getByText(/Crops/i)).toBeInTheDocument();
  expect(screen.getByText(/Tasks/i)).toBeInTheDocument();
  expect(screen.getByText(/Books/i)).toBeInTheDocument();
  expect(screen.getByText(/Restaurants/i)).toBeInTheDocument();
});
