import React from 'react';
import { Spinner } from 'react-bootstrap';

interface LoadingSpinnerProps {
  size?: 'sm' | undefined;
  variant?: string;
  className?: string;
  text?: string;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = undefined,
  variant = 'primary',
  className = '',
  text = 'Loading...'
}) => {
  return (
    <div className={`d-flex align-items-center justify-content-center ${className}`}>
      <Spinner
        animation="border"
        size={size}
        variant={variant}
        className="me-2"
      />
      <span className="text-muted">{text}</span>
    </div>
  );
};

export default LoadingSpinner; 