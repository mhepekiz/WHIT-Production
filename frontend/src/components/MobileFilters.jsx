import { useState, useEffect } from 'react';
import './MobileFilters.css';

function MobileFilters({ 
  isOpen, 
  onClose, 
  filters, 
  availableFilters, 
  onFilterChange, 
  onApply, 
  onReset 
}) {
  const [localFilters, setLocalFilters] = useState(filters);

  // Update local filters when props change
  useEffect(() => {
    setLocalFilters(filters);
  }, [filters]);

  // Close modal with escape key
  useEffect(() => {
    const handleEscape = (event) => {
      if (event.key === 'Escape' && isOpen) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose]);

  const handleLocalFilterChange = (filterName, value) => {
    setLocalFilters(prev => ({
      ...prev,
      [filterName]: value,
    }));
  };

  const handleApply = () => {
    // Apply all filter changes at once
    Object.keys(localFilters).forEach(key => {
      if (localFilters[key] !== filters[key]) {
        onFilterChange(key, localFilters[key]);
      }
    });
    onApply();
    onClose();
  };

  const handleReset = () => {
    const resetFilters = {
      search: '',
      country: '',
      state: '',
      city: '',
      functions: '',
      work_environment: '',
      engineering_positions: '',
    };
    setLocalFilters(resetFilters);
    onReset();
    onClose();
  };

  const getActiveFilterCount = () => {
    return Object.entries(localFilters).filter(([key, value]) => 
      key !== 'status' && key !== 'search' && value && value !== ''
    ).length;
  };

  if (!isOpen || !availableFilters) return null;

  return (
    <>
      {/* Modal Overlay */}
      <div className="mobile-filters-overlay" onClick={onClose} />
      
      {/* Bottom Sheet */}
      <div className={`mobile-filters-sheet ${isOpen ? 'open' : ''}`}>
        {/* Handle bar */}
        <div className="mobile-filters-handle"></div>
        
        {/* Header */}
        <div className="mobile-filters-header">
          <h2>Filters</h2>
          <button className="mobile-filters-close" onClick={onClose}>
            ✕
          </button>
        </div>

        {/* Filters Content */}
        <div className="mobile-filters-content">
          {/* Country Filter */}
          <div className="mobile-filter-group">
            <label htmlFor="mobile-country">Country</label>
            <select
              id="mobile-country"
              value={localFilters.country || ''}
              onChange={(e) => handleLocalFilterChange('country', e.target.value)}
              className="mobile-filter-select"
            >
              <option value="">All Countries</option>
              {availableFilters.countries?.map((country) => (
                <option key={country} value={country}>
                  {country}
                </option>
              ))}
            </select>
          </div>

          {/* State Filter */}
          <div className="mobile-filter-group">
            <label htmlFor="mobile-state">State</label>
            <select
              id="mobile-state"
              value={localFilters.state || ''}
              onChange={(e) => handleLocalFilterChange('state', e.target.value)}
              className="mobile-filter-select"
            >
              <option value="">All States</option>
              {availableFilters.states?.map((state) => (
                <option key={state} value={state}>
                  {state}
                </option>
              ))}
            </select>
          </div>

          {/* City Filter */}
          <div className="mobile-filter-group">
            <label htmlFor="mobile-city">City</label>
            <select
              id="mobile-city"
              value={localFilters.city || ''}
              onChange={(e) => handleLocalFilterChange('city', e.target.value)}
              className="mobile-filter-select"
            >
              <option value="">All Cities</option>
              {availableFilters.cities?.map((city) => (
                <option key={city} value={city}>
                  {city}
                </option>
              ))}
            </select>
          </div>

          {/* Function Filter */}
          <div className="mobile-filter-group">
            <label htmlFor="mobile-functions">Function</label>
            <select
              id="mobile-functions"
              value={localFilters.functions || ''}
              onChange={(e) => handleLocalFilterChange('functions', e.target.value)}
              className="mobile-filter-select"
            >
              <option value="">All Functions</option>
              {availableFilters.functions?.map((func) => (
                <option key={func.id} value={func.name}>
                  {func.name}
                </option>
              ))}
            </select>
          </div>

          {/* Work Environment Filter */}
          <div className="mobile-filter-group">
            <label htmlFor="mobile-work-environment">Work Environment</label>
            <select
              id="mobile-work-environment"
              value={localFilters.work_environment || ''}
              onChange={(e) => handleLocalFilterChange('work_environment', e.target.value)}
              className="mobile-filter-select"
            >
              <option value="">All Types</option>
              {availableFilters.work_environments?.map((env) => (
                <option key={env} value={env}>
                  {env}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="mobile-filters-actions">
          <button className="mobile-filter-reset" onClick={handleReset}>
            Reset ({getActiveFilterCount()})
          </button>
          <button className="mobile-filter-apply" onClick={handleApply}>
            Apply Filters
          </button>
        </div>
      </div>
    </>
  );
}

export default MobileFilters;