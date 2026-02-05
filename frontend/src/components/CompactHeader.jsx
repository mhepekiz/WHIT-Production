import { Link } from 'react-router-dom';
import { useState } from 'react';
import SearchBar from './SearchBar';
import ActiveFilters from './ActiveFilters';
import './CompactHeader.css';

function CompactHeader({ 
  filters, 
  onFiltersChange, 
  onFiltersToggle, 
  availableFilters, 
  filterCount,
  pagination 
}) {
  return (
    <div className="compact-header">
      {/* Clean Top Navigation - Wellfound Style */}
      <div className="header-row-1">
        <Link to="/" className="site-title">
          WHIT
        </Link>
        <div className="auth-buttons">
          <Link to="/login" className="login-link">
            Log in
          </Link>
          <Link to="/register" className="register-btn">
            Sign up
          </Link>
        </div>
      </div>

      {/* Hero Section - Wellfound Style */}
      <div className="hero-section">
        <h1 className="hero-title">Find your next role</h1>
        <p className="hero-subtitle">
          Discover opportunities at startups and tech companies. 
          Connect directly with founders and hiring teams.
        </p>
        
        {/* Search Section - Centered */}
        <div className="search-container">
          <SearchBar 
            value={filters.search}
            onChange={(value) => onFiltersChange({ ...filters, search: value })}
            placeholder="Search companies, roles, or skills..."
            className="search-input"
          />
          <button 
            className="filter-toggle"
            onClick={onFiltersToggle}
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polygon points="22,3 2,3 10,12.46 10,19 14,21 14,12.46"/>
            </svg>
            Filters {filterCount > 0 && `(${filterCount})`}
          </button>
        </div>
      </div>

      {/* Active Filters - Below Hero */}
      {(filters.country || filters.state || filters.city || filters.functions || filters.work_environment) && (
        <div className="active-filters-section">
          <div className="active-filters-container">
            <ActiveFilters 
              filters={filters}
              onFiltersChange={onFiltersChange}
              availableFilters={availableFilters}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default CompactHeader;