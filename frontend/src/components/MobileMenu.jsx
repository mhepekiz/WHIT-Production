import { useState, useRef, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useRecruiterAuth } from '../contexts/RecruiterAuthContext';
import './MobileMenu.css';

function MobileMenu() {
  const [isOpen, setIsOpen] = useState(false);
  const [loginDropdownOpen, setLoginDropdownOpen] = useState(false);
  const [registerDropdownOpen, setRegisterDropdownOpen] = useState(false);
  const menuRef = useRef(null);
  const navigate = useNavigate();
  const { isAuthenticated, user, logout } = useAuth();
  const { isAuthenticated: isRecruiterAuth, recruiterUser, logout: recruiterLogout } = useRecruiterAuth();

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setIsOpen(false);
        setLoginDropdownOpen(false);
        setRegisterDropdownOpen(false);
      }
    };

    const handleEscape = (event) => {
      if (event.key === 'Escape') {
        setIsOpen(false);
        setLoginDropdownOpen(false);
        setRegisterDropdownOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      document.addEventListener('keydown', handleEscape);
      document.body.style.overflow = 'hidden'; // Prevent scrolling when menu is open
    } else {
      document.body.style.overflow = 'unset';
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
    setLoginDropdownOpen(false);
    setRegisterDropdownOpen(false);
  };

  const closeMenu = () => {
    setIsOpen(false);
    setLoginDropdownOpen(false);
    setRegisterDropdownOpen(false);
  };

  const handleLogout = () => {
    if (isRecruiterAuth) {
      recruiterLogout();
    } else {
      logout();
    }
    closeMenu();
    navigate('/');
  };

  const toggleLoginDropdown = (e) => {
    e.preventDefault();
    setLoginDropdownOpen(!loginDropdownOpen);
    setRegisterDropdownOpen(false);
  };

  const toggleRegisterDropdown = (e) => {
    e.preventDefault();
    setRegisterDropdownOpen(!registerDropdownOpen);
    setLoginDropdownOpen(false);
  };

  return (
    <>
      {/* Hamburger Button */}
      <button 
        className={`mobile-menu-toggle ${isOpen ? 'open' : ''}`}
        onClick={toggleMenu}
        aria-label="Toggle menu"
      >
        <span></span>
        <span></span>
        <span></span>
      </button>

      {/* Menu Overlay */}
      {isOpen && <div className="mobile-menu-overlay" onClick={closeMenu} />}

      {/* Side Menu */}
      <div ref={menuRef} className={`mobile-menu ${isOpen ? 'open' : ''}`}>
        <div className="mobile-menu-header">
          <h2>Menu</h2>
          <button className="mobile-menu-close" onClick={closeMenu}>
            ✕
          </button>
        </div>

        <nav className="mobile-menu-nav">
          <Link to="/companies" className="mobile-menu-link" onClick={closeMenu}>
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <circle cx="10" cy="10" r="8" stroke="currentColor" strokeWidth="1.5"/>
              <path d="M6 9L10 13L14 9" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
            </svg>
            Browse Companies
          </Link>

          <Link to="/add-company" className="mobile-menu-link" onClick={closeMenu}>
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <circle cx="10" cy="10" r="8" stroke="currentColor" strokeWidth="1.5"/>
              <path d="M10 6V14M6 10H14" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
            </svg>
            Add Company
          </Link>

          <a href="#about" className="mobile-menu-link" onClick={closeMenu}>
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <circle cx="10" cy="10" r="8" stroke="currentColor" strokeWidth="1.5"/>
              <path d="M10 7.5C10 6.11929 8.88071 5 7.5 5C6.11929 5 5 6.11929 5 7.5C5 8.88071 6.11929 10 7.5 10C8.88071 10 10 8.88071 10 7.5Z" stroke="currentColor" strokeWidth="1.5"/>
              <path d="M15 13.5C15 12.1193 13.8807 11 12.5 11C11.1193 11 10 12.1193 10 13.5C10 14.8807 11.1193 16 12.5 16C13.8807 16 15 14.8807 15 13.5Z" stroke="currentColor" strokeWidth="1.5"/>
            </svg>
            About
          </a>

          <div className="mobile-menu-divider"></div>

          {/* Authentication Section */}
          {isAuthenticated || isRecruiterAuth ? (
            <div className="mobile-menu-auth-section">
              <div className="mobile-menu-user">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <circle cx="10" cy="7" r="4" stroke="currentColor" strokeWidth="1.5"/>
                  <path d="M3 18C3 14.134 6.134 11 10 11S17 14.134 17 18" stroke="currentColor" strokeWidth="1.5"/>
                </svg>
                {isRecruiterAuth ? recruiterUser?.email : user?.email}
              </div>
              
              {isRecruiterAuth ? (
                <>
                  <Link to="/recruiter/dashboard" className="mobile-menu-link" onClick={closeMenu}>
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                      <rect x="3" y="3" width="14" height="14" rx="2" stroke="currentColor" strokeWidth="1.5"/>
                      <path d="M8 7H12M8 11H12M8 15H10" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                    </svg>
                    Dashboard
                  </Link>
                  <Link to="/recruiter/dashboard/profile" className="mobile-menu-link" onClick={closeMenu}>
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                      <circle cx="10" cy="7" r="4" stroke="currentColor" strokeWidth="1.5"/>
                      <path d="M3 18C3 14.134 6.134 11 10 11S17 14.134 17 18" stroke="currentColor" strokeWidth="1.5"/>
                    </svg>
                    Profile
                  </Link>
                </>
              ) : (
                <>
                  <Link to="/dashboard" className="mobile-menu-link" onClick={closeMenu}>
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                      <rect x="3" y="3" width="14" height="14" rx="2" stroke="currentColor" strokeWidth="1.5"/>
                      <path d="M8 7H12M8 11H12M8 15H10" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                    </svg>
                    Dashboard
                  </Link>
                  <Link to="/dashboard/profile" className="mobile-menu-link" onClick={closeMenu}>
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                      <circle cx="10" cy="7" r="4" stroke="currentColor" strokeWidth="1.5"/>
                      <path d="M3 18C3 14.134 6.134 11 10 11S17 14.134 17 18" stroke="currentColor" strokeWidth="1.5"/>
                    </svg>
                    Profile
                  </Link>
                  <Link to="/dashboard/preferences" className="mobile-menu-link" onClick={closeMenu}>
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                      <circle cx="10" cy="10" r="3" stroke="currentColor" strokeWidth="1.5"/>
                      <path d="M19 10C19 10 16 6 10 6S1 10 1 10S4 14 10 14S19 10 19 10Z" stroke="currentColor" strokeWidth="1.5"/>
                    </svg>
                    Job Preferences
                  </Link>
                </>
              )}
              
              <button className="mobile-menu-link logout-link" onClick={handleLogout}>
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path d="M7 17H4C3.44772 17 3 16.5523 3 16V4C3 3.44772 3.44772 3 4 3H7M13 13L17 10L13 7M17 10H7" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                Sign Out
              </button>
            </div>
          ) : (
            <div className="mobile-menu-auth-section">
              {/* Login Dropdown */}
              <div className="mobile-menu-dropdown">
                <button className="mobile-menu-link" onClick={toggleLoginDropdown}>
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M13 17H16C16.5523 17 17 16.5523 17 16V4C17 3.44772 16.5523 3 16 3H13M7 13L3 10L7 7M3 10H13" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                  Login
                  <svg className={`dropdown-arrow ${loginDropdownOpen ? 'open' : ''}`} width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <path d="M4 6L8 10L12 6" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                  </svg>
                </button>
                {loginDropdownOpen && (
                  <div className="mobile-submenu">
                    <Link to="/login" className="mobile-submenu-link" onClick={closeMenu}>
                      Job Seeker Login
                    </Link>
                    <Link to="/recruiter/login" className="mobile-submenu-link" onClick={closeMenu}>
                      Recruiter Login
                    </Link>
                  </div>
                )}
              </div>

              {/* Register Dropdown */}
              <div className="mobile-menu-dropdown">
                <button className="mobile-menu-link" onClick={toggleRegisterDropdown}>
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <circle cx="10" cy="7" r="4" stroke="currentColor" strokeWidth="1.5"/>
                    <path d="M3 18C3 14.134 6.134 11 10 11S17 14.134 17 18" stroke="currentColor" strokeWidth="1.5"/>
                  </svg>
                  Register
                  <svg className={`dropdown-arrow ${registerDropdownOpen ? 'open' : ''}`} width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <path d="M4 6L8 10L12 6" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                  </svg>
                </button>
                {registerDropdownOpen && (
                  <div className="mobile-submenu">
                    <Link to="/register" className="mobile-submenu-link" onClick={closeMenu}>
                      Job Seeker Register
                    </Link>
                    <Link to="/recruiter/register" className="mobile-submenu-link" onClick={closeMenu}>
                      Recruiter Register
                    </Link>
                  </div>
                )}
              </div>
            </div>
          )}
        </nav>
      </div>
    </>
  );
}

export default MobileMenu;