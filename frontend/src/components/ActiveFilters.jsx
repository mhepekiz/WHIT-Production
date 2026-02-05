import './ActiveFiltersModern.css';

function ActiveFilters({ filters, onFiltersChange, availableFilters }) {
  // Get active filters (exclude default/empty values)
  const getActiveFilters = () => {
    const activeFilters = [];
    
    if (filters.country) {
      activeFilters.push({ key: 'country', value: filters.country, label: filters.country });
    }
    if (filters.state) {
      activeFilters.push({ key: 'state', value: filters.state, label: filters.state });
    }
    if (filters.city) {
      activeFilters.push({ key: 'city', value: filters.city, label: filters.city });
    }
    if (filters.functions) {
      activeFilters.push({ key: 'functions', value: filters.functions, label: filters.functions });
    }
    if (filters.work_environment) {
      activeFilters.push({ key: 'work_environment', value: filters.work_environment, label: filters.work_environment });
    }
    
    return activeFilters;
  };

  const activeFilters = getActiveFilters();

  const handleRemoveFilter = (filterKey) => {
    onFiltersChange({ ...filters, [filterKey]: '' });
  };

  const handleClearAll = () => {
    onFiltersChange({
      search: filters.search, // Keep search
      country: '',
      state: '',
      city: '',
      functions: '',
      work_environment: '',
    });
  };

  if (activeFilters.length === 0) {
    return (
      <div className="active-filters-empty">
        {/* Placeholder for layout consistency */}
      </div>
    );
  }

  return (
    <div className="active-filters-modern">
      <div className="active-filters-chips">
        {activeFilters.map((filter) => (
          <div key={`${filter.key}-${filter.value}`} className="filter-chip-modern">
            <span className="filter-chip-label">{filter.label}</span>
            <button
              className="filter-chip-remove"
              onClick={() => handleRemoveFilter(filter.key)}
              title={`Remove ${filter.label} filter`}
            >
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>
        ))}
        
        <button className="reset-all-btn" onClick={handleClearAll}>
          Reset
        </button>
      </div>
    </div>
  );
}

export default ActiveFilters;