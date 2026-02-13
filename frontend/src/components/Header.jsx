import { Link, useNavigate } from 'react-router-dom';
import { useState, useRef, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useRecruiterAuth } from '../contexts/RecruiterAuthContext';
import MobileMenu from './MobileMenu';
import './Header.css';

function Header() {
  const { isAuthenticated, user, logout } = useAuth();
  const { isAuthenticated: isRecruiterAuth, recruiterUser, logout: recruiterLogout } = useRecruiterAuth();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [registerDropdownOpen, setRegisterDropdownOpen] = useState(false);
  const [loginDropdownOpen, setLoginDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);
  const registerDropdownRef = useRef(null);
  const loginDropdownRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setDropdownOpen(false);
      }
      if (registerDropdownRef.current && !registerDropdownRef.current.contains(event.target)) {
        setRegisterDropdownOpen(false);
      }
      if (loginDropdownRef.current && !loginDropdownRef.current.contains(event.target)) {
        setLoginDropdownOpen(false);
      }
    };

    const handleEscKey = (event) => {
      if (event.key === 'Escape') {
        setDropdownOpen(false);
        setRegisterDropdownOpen(false);
        setLoginDropdownOpen(false);
      }
    };

    const handleScroll = () => {
      setDropdownOpen(false);
      setRegisterDropdownOpen(false);
      setLoginDropdownOpen(false);
    };

    document.addEventListener('mousedown', handleClickOutside);
    document.addEventListener('keydown', handleEscKey); // Fix 8: ESC key support
    window.addEventListener('scroll', handleScroll, true); // Fix 8: Close on scroll
    
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleEscKey);
      window.removeEventListener('scroll', handleScroll, true);
    };
  }, []);

  const handleLogout = () => {
    if (isRecruiterAuth) {
      recruiterLogout();
    } else {
      logout();
    }
    setDropdownOpen(false);
    navigate('/');
  };

  const toggleDropdown = () => {
    setDropdownOpen(!dropdownOpen);
  };

  return (
    <header className="nav">
      <div className="nav__inner">
        {/* Left: Brand */}
        <div className="nav__left">
          <Link to="/" className="nav__brand">
            WhoIsHiringInTech
          </Link>
        </div>

        {/* Center: Primary Navigation */}
        <nav className="nav__center" aria-label="Primary">
          <Link to="/all-companies" className="nav__link">Browse Companies</Link>
          <Link to="/add-company" className="nav__link">Add Company</Link>
        </nav>

        {/* Right: Secondary Navigation */}
        <div className="nav__right">
          <a href="#about" className="nav__link">About</a>
          {isAuthenticated || isRecruiterAuth ? (
            <div className="user-menu" ref={dropdownRef}>
              <button 
                className="nav-link nav-link-dashboard"
                onClick={toggleDropdown}
              >
                Dashboard
                <svg 
                  className={`dropdown-icon ${dropdownOpen ? 'open' : ''}`}
                  width="12" 
                  height="12" 
                  viewBox="0 0 12 12" 
                  fill="none"
                >
                  <path d="M2 4L6 8L10 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                </svg>
              </button>
              {dropdownOpen && (
                <div className="dropdown-menu">
                  {isRecruiterAuth ? (
                    <>
                      <Link 
                        to="/recruiter/dashboard" 
                        className="dropdown-item"
                        onClick={() => setDropdownOpen(false)}
                      >
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                          <path d="M2 8H14M2 4H14M2 12H14" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                        </svg>
                        Dashboard
                      </Link>
                      <Link 
                        to="/recruiter/dashboard/profile" 
                        className="dropdown-item"
                        onClick={() => setDropdownOpen(false)}
                      >
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                          <circle cx="8" cy="5" r="3" stroke="currentColor" strokeWidth="1.5"/>
                          <path d="M2 14C2 11.2386 4.23858 9 7 9H9C11.7614 9 14 11.2386 14 14" stroke="currentColor" strokeWidth="1.5"/>
                        </svg>
                        Profile
                      </Link>
                      <Link 
                        to="/recruiter/dashboard/jobs" 
                        className="dropdown-item"
                        onClick={() => setDropdownOpen(false)}
                      >
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                          <rect x="3" y="4" width="10" height="9" rx="1" stroke="currentColor" strokeWidth="1.5"/>
                          <path d="M6 4V3C6 2.44772 6.44772 2 7 2H9C9.55228 2 10 2.44772 10 3V4" stroke="currentColor" strokeWidth="1.5"/>
                        </svg>
                        Job Openings
                      </Link>
                      <Link 
                        to="/recruiter/dashboard/analytics" 
                        className="dropdown-item"
                        onClick={() => setDropdownOpen(false)}
                      >
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                          <path d="M2 14V10M6 14V6M10 14V8M14 14V4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                        </svg>
                        Analytics
                      </Link>
                      <Link 
                        to="/recruiter/dashboard/candidates" 
                        className="dropdown-item"
                        onClick={() => setDropdownOpen(false)}
                      >
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                          <circle cx="5.5" cy="4.5" r="2.5" stroke="currentColor" strokeWidth="1.5"/>
                          <circle cx="10.5" cy="4.5" r="2.5" stroke="currentColor" strokeWidth="1.5"/>
                          <path d="M1 13C1 10.7909 2.79086 9 5 9H6C8.20914 9 10 10.7909 10 13" stroke="currentColor" strokeWidth="1.5"/>
                          <path d="M6 13C6 10.7909 7.79086 9 10 9H11C13.2091 9 15 10.7909 15 13" stroke="currentColor" strokeWidth="1.5"/>
                        </svg>
                        Search Candidates
                      </Link>
                      <Link 
                        to="/recruiter/dashboard/applications" 
                        className="dropdown-item"
                        onClick={() => setDropdownOpen(false)}
                      >
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                          <path d="M4 2H9L12 5V14H4V2Z" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/>
                          <path d="M9 2V5H12" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/>
                          <path d="M6 8H10M6 10H10" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                        </svg>
                        Applications
                      </Link>
                    </>
                  ) : (
                    <>
                      <Link 
                        to="/dashboard" 
                        className="dropdown-item"
                        onClick={() => setDropdownOpen(false)}
                      >
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                          <path d="M2 8H14M2 4H14M2 12H14" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                        </svg>
                        Dashboard
                      </Link>
                      <Link 
                        to="/dashboard/profile" 
                        className="dropdown-item"
                        onClick={() => setDropdownOpen(false)}
                      >
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                          <circle cx="8" cy="5" r="3" stroke="currentColor" strokeWidth="1.5"/>
                          <path d="M2 14C2 11.2386 4.23858 9 7 9H9C11.7614 9 14 11.2386 14 14" stroke="currentColor" strokeWidth="1.5"/>
                        </svg>
                        Edit Profile
                      </Link>
                      <Link 
                        to="/dashboard/preferences" 
                        className="dropdown-item"
                        onClick={() => setDropdownOpen(false)}
                      >
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                          <rect x="3" y="4" width="10" height="9" rx="1" stroke="currentColor" strokeWidth="1.5"/>
                          <path d="M6 4V3C6 2.44772 6.44772 2 7 2H9C9.55228 2 10 2.44772 10 3V4" stroke="currentColor" strokeWidth="1.5"/>
                        </svg>
                        Job Preferences
                      </Link>
                      <Link 
                        to="/dashboard/resume" 
                        className="dropdown-item"
                        onClick={() => setDropdownOpen(false)}
                      >
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                          <path d="M4 2H9L12 5V14H4V2Z" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/>
                          <path d="M9 2V5H12" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/>
                        </svg>
                        Resume
                      </Link>
                    </>
                  )}
                  <div className="dropdown-divider"></div>
                  <button 
                    className="dropdown-item logout-item"
                    onClick={handleLogout}
                  >
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                      <path d="M6 14H3C2.44772 14 2 13.5523 2 13V3C2 2.44772 2.44772 2 3 2H6" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                      <path d="M11 11L14 8M14 8L11 5M14 8H6" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                    Logout
                  </button>
                </div>
              )}
            </div>
          ) : (
            <>
              <div className="auth-menu" ref={registerDropdownRef}>
                <button 
                  className="nav-link nav-link-register"
                  onClick={() => setRegisterDropdownOpen(!registerDropdownOpen)}
                >
                  Register
                  <svg 
                    className={`dropdown-icon ${registerDropdownOpen ? 'open' : ''}`}
                    width="12" 
                    height="12" 
                    viewBox="0 0 12 12" 
                    fill="none"
                  >
                    <path d="M2 4L6 8L10 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                  </svg>
                </button>
                {registerDropdownOpen && (
                  <div className="dropdown-menu auth-dropdown">
                    <Link 
                      to="/register" 
                      className="dropdown-item"
                      onClick={() => setRegisterDropdownOpen(false)}
                    >
                      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                        <path d="M8 8C10.2091 8 12 6.20914 12 4C12 1.79086 10.2091 0 8 0C5.79086 0 4 1.79086 4 4C4 6.20914 5.79086 8 8 8Z" fill="currentColor"/>
                        <path d="M0 16C0 12.6863 2.68629 10 6 10H10C13.3137 10 16 12.6863 16 16H0Z" fill="currentColor"/>
                      </svg>
                      Register as Job Seeker
                    </Link>
                    <Link 
                      to="/recruiter/register" 
                      className="dropdown-item"
                      onClick={() => setRegisterDropdownOpen(false)}
                    >
                      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                        <path d="M3 4H13V13H3V4Z" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/>
                        <path d="M5 4V3C5 2.44772 5.44772 2 6 2H10C10.5523 2 11 2.44772 11 3V4" stroke="currentColor" strokeWidth="1.5"/>
                        <path d="M8 7V10M6.5 8.5H9.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                      </svg>
                      Register as Recruiter
                    </Link>
                  </div>
                )}
              </div>
              <div className="auth-menu" ref={loginDropdownRef}>
                <button 
                  className="nav-link nav-link-login"
                  onClick={() => setLoginDropdownOpen(!loginDropdownOpen)}
                >
                  Login
                  <svg 
                    className={`dropdown-icon ${loginDropdownOpen ? 'open' : ''}`}
                    width="12" 
                    height="12" 
                    viewBox="0 0 12 12" 
                    fill="none"
                  >
                    <path d="M2 4L6 8L10 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                  </svg>
                </button>
                {loginDropdownOpen && (
                  <div className="dropdown-menu auth-dropdown">
                    <Link 
                      to="/login" 
                      className="dropdown-item"
                      onClick={() => setLoginDropdownOpen(false)}
                    >
                      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                        <path d="M8 8C10.2091 8 12 6.20914 12 4C12 1.79086 10.2091 0 8 0C5.79086 0 4 1.79086 4 4C4 6.20914 5.79086 8 8 8Z" fill="currentColor"/>
                        <path d="M0 16C0 12.6863 2.68629 10 6 10H10C13.3137 10 16 12.6863 16 16H0Z" fill="currentColor"/>
                      </svg>
                      Login as Job Seeker
                    </Link>
                    <Link 
                      to="/recruiter/login" 
                      className="dropdown-item"
                      onClick={() => setLoginDropdownOpen(false)}
                    >
                      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                        <path d="M3 4H13V13H3V4Z" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/>
                        <path d="M5 4V3C5 2.44772 5.44772 2 6 2H10C10.5523 2 11 2.44772 11 3V4" stroke="currentColor" strokeWidth="1.5"/>
                        <path d="M8 7V10M6.5 8.5H9.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                      </svg>
                      Login as Recruiter
                    </Link>
                  </div>
                )}
              </div>
            </>
          )}
        </div>
        
        {/* Mobile Navigation */}
        <MobileMenu />
      </div>
    </header>
  );
}

export default Header;
