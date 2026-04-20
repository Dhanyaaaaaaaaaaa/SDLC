import React from 'react';
import { render, screen } from '@testing-library/react';
import CropList from '../src/components/CropList';

test('renders crop list with crops', () => {
  const crops = [
    { id: '1', crop_type: 'Wheat', planting_date: '2024-01-01', expected_harvest_date: '2024-06-01', growth_stage: 'Seedling', health_status: 'Healthy', notes: '', is_harvested: false, owner_id: 'u1', created_at: '2024-01-01T00:00:00Z', updated_at: '2024-01-01T00:00:00Z' },
    { id: '2', crop_type: 'Corn', planting_date: '2024-02-01', expected_harvest_date: '2024-07-01', growth_stage: 'Mature', health_status: 'Healthy', notes: '', is_harvested: false, owner_id: 'u1', created_at: '2024-02-01T00:00:00Z', updated_at: '2024-02-01T00:00:00Z' },
  ];
  render(<CropList crops={crops} onEdit={jest.fn()} onDelete={jest.fn()} />);
  expect(screen.getByText(/Wheat/i)).toBeInTheDocument();
  expect(screen.getByText(/Corn/i)).toBeInTheDocument();
});
