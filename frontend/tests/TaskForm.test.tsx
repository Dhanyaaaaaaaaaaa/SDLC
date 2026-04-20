import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import TaskForm from '../src/components/TaskForm';

test('renders task form and validates required fields', () => {
  const onSubmit = jest.fn();
  render(<TaskForm onSubmit={onSubmit} cropOptions={[{ id: '1', crop_type: 'Wheat' }]} />);
  fireEvent.click(screen.getByText(/Save/i));
  expect(screen.getByText(/Title is required/i)).toBeInTheDocument();
  expect(screen.getByText(/Due date is required/i)).toBeInTheDocument();
});
