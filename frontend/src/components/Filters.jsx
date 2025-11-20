import './Filters.css';

function Filters({ filters, availableFilters, onFilterChange, onReset }) {
  return (
    <div className="filters-container">
      <div className="filters-header">
        <h3>Filters</h3>
        <button className="reset-btn" onClick={onReset}>
          Reset All
        </button>
      </div>

      <div className="filters-grid">
        <div className="filter-group">
          <label htmlFor="status">Status</label>
          <select
            id="status"
            value={filters.status}
            onChange={(e) => onFilterChange('status', e.target.value)}
            className="filter-select"
          >
            <option value="">All</option>
            <option value="Active">Active</option>
            <option value="Inactive">Inactive</option>
          </select>
        </div>

        <div className="filter-group">
          <label htmlFor="country">Country</label>
          <select
            id="country"
            value={filters.country}
            onChange={(e) => onFilterChange('country', e.target.value)}
            className="filter-select"
          >
            <option value="">All Countries</option>
            {availableFilters.countries.map((country) => (
              <option key={country} value={country}>
                {country}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label htmlFor="state">State</label>
          <select
            id="state"
            value={filters.state}
            onChange={(e) => onFilterChange('state', e.target.value)}
            className="filter-select"
          >
            <option value="">All States</option>
            {availableFilters.states.map((state) => (
              <option key={state} value={state}>
                {state}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label htmlFor="city">City</label>
          <select
            id="city"
            value={filters.city}
            onChange={(e) => onFilterChange('city', e.target.value)}
            className="filter-select"
          >
            <option value="">All Cities</option>
            {availableFilters.cities.map((city) => (
              <option key={city} value={city}>
                {city}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label htmlFor="functions">Function</label>
          <select
            id="functions"
            value={filters.functions}
            onChange={(e) => onFilterChange('functions', e.target.value)}
            className="filter-select"
          >
            <option value="">All Functions</option>
            {availableFilters.functions.map((func) => (
              <option key={func.id} value={func.name}>
                {func.name}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label htmlFor="work_environment">Work Environment</label>
          <select
            id="work_environment"
            value={filters.work_environment}
            onChange={(e) => onFilterChange('work_environment', e.target.value)}
            className="filter-select"
          >
            <option value="">All Types</option>
            {availableFilters.work_environments.map((env) => (
              <option key={env} value={env}>
                {env}
              </option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );
}

export default Filters;
