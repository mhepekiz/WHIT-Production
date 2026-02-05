import { useState, useEffect } from 'react';
import './FilterDrawer.css';

function FilterDrawer({ 
  isOpen, 
  onClose, 
  filters, 
  onFiltersChange, 
  availableFilters,
  onApply,
  resultsCount = 0,
  isMobile = false 
}) {
  const [localFilters, setLocalFilters] = useState(filters);

  useEffect(() => {
    setLocalFilters(filters);
  }, [filters]);

  const handleLocalChange = (key, value) => {
    setLocalFilters(prev => ({ ...prev, [key]: value }));
  };

  const handleApply = () => {
    onFiltersChange(localFilters);
    onApply?.();
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
    };
    setLocalFilters(resetFilters);
    onFiltersChange(resetFilters);
    onApply?.();
  };

  const getActiveFilterCount = () => {
    return Object.values(localFilters).filter(value => value && value.toString().trim() !== '').length;
  };

  if (!isOpen) return null;

  return (
    <>
      {/* Backdrop */}
      <div className="filter-drawer-backdrop" onClick={onClose} />
      
      {/* Drawer */}
      <div className={`filter-drawer ${isMobile ? 'mobile' : 'desktop'}`}>
        <div className="filter-drawer-header">
          <h3>Filters</h3>
          <button className="close-btn" onClick={onClose}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        
        <div className="filter-drawer-content">
          {/* Location Filters */}
          <div className="filter-section">
            <h4 className="filter-section-title">Location</h4>
            
            <div className="filter-field">
              <label>Country</label>
              <select
                value={localFilters.country}
                onChange={(e) => handleLocalChange('country', e.target.value)}
                className="filter-select"
              >
                <option value="">All Countries</option>
                {availableFilters?.countries?.map(country => (
                  <option key={country} value={country}>{country}</option>
                ))}
              </select>
            </div>
            
            {localFilters.country && (
              <div className="filter-field">
                <label>State/Region</label>
                <select
                  value={localFilters.state}
                  onChange={(e) => handleLocalChange('state', e.target.value)}
                  className="filter-select"
                >
                  <option value="">All States</option>
                  {availableFilters?.states?.filter(state => 
                    !localFilters.country || state.country === localFilters.country
                  ).map(state => (
                    <option key={state.name} value={state.name}>{state.name}</option>
                  ))}
                </select>
              </div>
            )}
            
            {localFilters.state && (
              <div className="filter-field">
                <label>City</label>
                <select
                  value={localFilters.city}
                  onChange={(e) => handleLocalChange('city', e.target.value)}
                  className="filter-select"
                >
                  <option value="">All Cities</option>
                  {availableFilters?.cities?.filter(city => 
                    (!localFilters.country || city.country === localFilters.country) &&
                    (!localFilters.state || city.state === localFilters.state)
                  ).map(city => (
                    <option key={city.name} value={city.name}>{city.name}</option>
                  ))}
                </select>
              </div>
            )}
          </div>
          
          {/* Function Filters */}
          <div className="filter-section">
            <h4 className="filter-section-title">Functions</h4>
            <div className="filter-field">
              <select
                value={localFilters.functions}
                onChange={(e) => handleLocalChange('functions', e.target.value)}
                className="filter-select"
              >
                <option value="">All Functions</option>
                {availableFilters?.functions?.map(func => (
                  <option key={func} value={func}>{func}</option>
                ))}
              </select>
            </div>
          </div>
          
          {/* Work Environment Filters */}
          <div className="filter-section">
            <h4 className="filter-section-title">Work Environment</h4>
            <div className="filter-field">
              <select
                value={localFilters.work_environment}
                onChange={(e) => handleLocalChange('work_environment', e.target.value)}
                className="filter-select"
              >
                <option value="">All Types</option>
                {availableFilters?.work_environments?.map(env => (
                  <option key={env} value={env}>{env}</option>
                ))}
              </select>
            </div>
          </div>
        </div>
        
        {/* Drawer Footer */}
        <div className="filter-drawer-footer">
          <button className="reset-btn" onClick={handleReset}>
            Reset
          </button>
          <button className="apply-btn btn-primary" onClick={handleApply}>
            Show {resultsCount} companies
          </button>
        </div>
      </div>
    </>
  );
}

export default FilterDrawer;