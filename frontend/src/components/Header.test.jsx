import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { vi } from 'vitest';
import Header from './Header';

// Mock the context providers
vi.mock('../context/AuthContext', () => ({
  useAuth: () => ({
    isAuthenticated: false,
    user: null,
    logout: vi.fn(),
  }),
}));

vi.mock('../contexts/RecruiterAuthContext', () => ({
  useRecruiterAuth: () => ({
    isAuthenticated: false,
    recruiterUser: null,
    logout: vi.fn(),
  }),
}));

vi.mock('./MobileMenu', () => {
  return function MobileMenu() {
    return <div data-testid="mobile-menu">Mobile Menu</div>;
  };
});

const HeaderWithRouter = () => (
  <BrowserRouter>
    <Header />
  </BrowserRouter>
);

describe('Header Component', () => {
  test('renders navbar with correct layout structure', () => {
    render(<HeaderWithRouter />);
    
    // Check that brand logo is present
    expect(screen.getByText('WhoIsHiringInTech')).toBeInTheDocument();
    
    // Check main navigation links are present
    expect(screen.getByText('BROWSE COMPANIES')).toBeInTheDocument();
    expect(screen.getByText('ADD COMPANY')).toBeInTheDocument();
    
    // Check account actions are present on right
    expect(screen.getByText('ABOUT')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Register options' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Login options' })).toBeInTheDocument();
  });

  test('navbar has correct flex layout structure', () => {
    render(<HeaderWithRouter />);
    
    const navInner = document.querySelector('.nav__inner');
    const navLeft = document.querySelector('.nav__left');
    const navRight = document.querySelector('.nav__right');
    
    expect(navInner).toHaveStyle({ display: 'flex', justifyContent: 'space-between' });
    expect(navLeft).toBeInTheDocument();
    expect(navRight).toBeInTheDocument();
  });

  test('REGISTER dropdown opens and shows menu items', async () => {
    render(<HeaderWithRouter />);
    
    const registerButton = screen.getByRole('button', { name: 'Register options' });
    
    // Initially dropdown should not be visible
    expect(screen.queryByText('Register as Job Seeker')).not.toBeInTheDocument();
    
    // Click the register button
    fireEvent.click(registerButton);
    
    // Dropdown menu should appear
    await waitFor(() => {
      expect(screen.getByText('Register as Job Seeker')).toBeInTheDocument();
      expect(screen.getByText('Register as Recruiter')).toBeInTheDocument();
    });
    
    // Check ARIA attributes
    expect(registerButton).toHaveAttribute('aria-expanded', 'true');
    expect(registerButton).toHaveAttribute('aria-haspopup', 'menu');
  });

  test('LOGIN dropdown opens and shows menu items', async () => {
    render(<HeaderWithRouter />);
    
    const loginButton = screen.getByRole('button', { name: 'Login options' });
    
    // Initially dropdown should not be visible
    expect(screen.queryByText('Login as Job Seeker')).not.toBeInTheDocument();
    
    // Click the login button
    fireEvent.click(loginButton);
    
    // Dropdown menu should appear
    await waitFor(() => {
      expect(screen.getByText('Login as Job Seeker')).toBeInTheDocument();
      expect(screen.getByText('Login as Recruiter')).toBeInTheDocument();
    });
    
    // Check ARIA attributes
    expect(loginButton).toHaveAttribute('aria-expanded', 'true');
    expect(loginButton).toHaveAttribute('aria-haspopup', 'menu');
  });

  test('clicking outside closes dropdown menu', async () => {
    render(<HeaderWithRouter />);
    
    const registerButton = screen.getByRole('button', { name: 'Register options' });
    
    // Open dropdown
    fireEvent.click(registerButton);
    
    await waitFor(() => {
      expect(screen.getByText('Register as Job Seeker')).toBeInTheDocument();
    });
    
    // Click outside
    fireEvent.mouseDown(document.body);
    
    await waitFor(() => {
      expect(screen.queryByText('Register as Job Seeker')).not.toBeInTheDocument();
    });
    
    expect(registerButton).toHaveAttribute('aria-expanded', 'false');
  });

  test('ESC key closes dropdown menu', async () => {
    render(<HeaderWithRouter />);
    
    const registerButton = screen.getByRole('button', { name: 'Register options' });
    
    // Open dropdown
    fireEvent.click(registerButton);
    
    await waitFor(() => {
      expect(screen.getByText('Register as Job Seeker')).toBeInTheDocument();
    });
    
    // Press ESC key
    fireEvent.keyDown(document, { key: 'Escape' });
    
    await waitFor(() => {
      expect(screen.queryByText('Register as Job Seeker')).not.toBeInTheDocument();
    });
    
    expect(registerButton).toHaveAttribute('aria-expanded', 'false');
  });

  test('clicking dropdown menu item closes dropdown', async () => {
    render(<HeaderWithRouter />);
    
    const registerButton = screen.getByRole('button', { name: 'Register options' });
    
    // Open dropdown
    fireEvent.click(registerButton);
    
    await waitFor(() => {
      expect(screen.getByText('Register as Job Seeker')).toBeInTheDocument();
    });
    
    // Click on menu item
    const jobSeekerLink = screen.getByText('Register as Job Seeker');
    fireEvent.click(jobSeekerLink);
    
    // Dropdown should close
    await waitFor(() => {
      expect(screen.queryByText('Register as Job Seeker')).not.toBeInTheDocument();
    });
  });
});