import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import CropForm from '../src/components/CropForm';

test('renders crop form and validates required fields', () => {
  const onSubmit = jest.fn();
  render(<CropForm onSubmit={onSubmit} />);
  fireEvent.click(screen.getByText(/Save/i));
  expect(screen.getByText(/Crop type is required/i)).toBeInTheDocument();
  expect(screen.getByText(/Planting date is required/i)).toBeInTheDocument();
  expect(screen.getByText(/Expected harvest date is required/i)).toBeInTheDocument();
});
