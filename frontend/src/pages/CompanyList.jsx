import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { companyService } from '../services/api';
import CompanyTable from '../components/CompanyTable';
import Filters from '../components/Filters';
import SearchBar from '../components/SearchBar';
import Stats from '../components/Stats';
import HomepageSections from '../components/HomepageSections';
import useHomepageSections from '../hooks/useHomepageSections';
import './CompanyList.css';

function CompanyList() {
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { sections: homepageSections, loading: sectionsLoading } = useHomepageSections();
  const [filters, setFilters] = useState({
    search: '',
    country: '',
    state: '',
    city: '',
    functions: '',
    work_environment: '',
    status: 'Active',
  });
  const [availableFilters, setAvailableFilters] = useState(null);
  const [pagination, setPagination] = useState({
    count: 0,
    next: null,
    previous: null,
    currentPage: 1,
  });
  const [labelSize, setLabelSize] = useState('medium');
  const [buttonStyles, setButtonStyles] = useState({ padding: '6px 12px', fontSize: '0.75rem' });
  const [adSlots, setAdSlots] = useState({
    slot1: null,
    slot2: null,
  });
  const [filtersVisible, setFiltersVisible] = useState(false);

  // Fetch available filter options and ad slots
  useEffect(() => {
    const fetchFilters = async () => {
      try {
        const data = await companyService.getFilters();
        setAvailableFilters(data);
      } catch (err) {
        console.error('Failed to fetch filters:', err);
      }
    };

    const fetchAdSlots = async () => {
      try {
        const API_URL = import.meta.env.VITE_API_URL || 'https://staging.whoishiringintech.com/api';
        const response = await fetch(`${API_URL}/ad-slots/active/`);
        if (response.ok) {
          const data = await response.json();
          console.log('Ad slots data:', data);
          setAdSlots(data);
        }
      } catch (err) {
        console.error('Failed to fetch ad slots:', err);
        // Set empty ad slots instead of failing
        setAdSlots({ slot1: null, slot2: null });
      }
    };

    const fetchSiteSettings = async () => {
      try {
        const API_URL = import.meta.env.VITE_API_URL || 'https://staging.whoishiringintech.com/api';
        const response = await fetch(`${API_URL}/site-settings/current/`);
        if (response.ok) {
          const data = await response.json();
          console.log('Site settings loaded:', data);
          setLabelSize(data.label_size);
          document.documentElement.setAttribute('data-label-size', data.label_size);
          
          // Set button styles based on size
          const sizeMap = {
            'small': { padding: '4px 8px', fontSize: '0.65rem' },
            'medium': { padding: '6px 12px', fontSize: '0.75rem' },
            'large': { padding: '8px 16px', fontSize: '0.85rem' },
            'extra-large': { padding: '10px 20px', fontSize: '0.95rem' }
          };
          
          const styles = sizeMap[data.label_size] || sizeMap['medium'];
          console.log('Setting button styles:', styles);
          setButtonStyles(styles);
          
          console.log('Applied styles:', styles);
        }
      } catch (err) {
        console.error('Failed to fetch site settings:', err);
      }
    };

    fetchFilters();
    fetchAdSlots();
    fetchSiteSettings();
  }, []);

  // Fetch companies with filters
  useEffect(() => {
    const fetchCompanies = async () => {
      setLoading(true);
      try {
        // Build query params
        const params = {};
        if (filters.search) params.search = filters.search;
        if (filters.country) params.country = filters.country;
        if (filters.state) params.state = filters.state;
        if (filters.city) params.city = filters.city;
        if (filters.functions) params.functions = filters.functions;
        if (filters.work_environment) params.work_environment = filters.work_environment;
        if (filters.engineering_positions) params.engineering_positions = filters.engineering_positions;
        if (filters.status) params.status = filters.status;
        params.page = pagination.currentPage;
        params.page_size = 12;

        const data = await companyService.getCompanies(params);
        console.log('Companies API response:', data);
        setCompanies(data.results);
        setPagination({
          count: data.count,
          next: data.next,
          previous: data.previous,
          currentPage: pagination.currentPage,
        });
        setError(null);
      } catch (err) {
        console.error('Failed to fetch companies:', err);
        setError('Failed to load companies. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchCompanies();
  }, [filters, pagination.currentPage]);

  const handleFilterChange = (filterName, value) => {
    setFilters(prev => ({
      ...prev,
      [filterName]: value,
    }));
    setPagination(prev => ({ ...prev, currentPage: 1 }));
  };

  const handleSearch = (searchTerm) => {
    handleFilterChange('search', searchTerm);
  };

  const handlePageChange = (newPage) => {
    setPagination(prev => ({ ...prev, currentPage: newPage }));
    window.scrollTo(0, 0);
  };

  const resetFilters = () => {
    setFilters({
      search: '',
      country: '',
      state: '',
      city: '',
      functions: '',
      work_environment: '',
      engineering_positions: '',
      status: 'Active',
    });
    setPagination(prev => ({ ...prev, currentPage: 1 }));
  };

  return (
    <div className="company-list-page">
      <div className="top-bar">
        <div className="search-section">
          <SearchBar onSearch={handleSearch} initialValue={filters.search} />
        </div>
        <button 
          className="filters-toggle-btn"
          onClick={() => setFiltersVisible(!filtersVisible)}
          aria-label="Toggle filters"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>
          </svg>
          Filters
          <svg 
            className={`chevron ${filtersVisible ? 'open' : ''}`}
            width="16" height="16" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            strokeWidth="2"
          >
            <polyline points="6 9 12 15 18 9"></polyline>
          </svg>
        </button>
      </div>

      <div className={`filters-wrapper ${filtersVisible ? 'visible' : ''}`}>
        {availableFilters && (
          <Filters
            filters={filters}
            availableFilters={availableFilters}
            onFilterChange={handleFilterChange}
            onReset={resetFilters}
          />
        )}
      </div>

      {error && (
        <div className="error-message">
          <p>{error}</p>
        </div>
      )}

      {loading ? (
        <div className="loading">
          <div className="loading-spinner"></div>
          <p>Loading companies...</p>
        </div>
      ) : (
        <>
          <div className="homepage-preview">
            <div className="preview-header">
              <h2 className="preview-title">Recently Updated Companies</h2>
              <p className="preview-subtitle">Discover companies actively hiring in tech</p>
            </div>
            
            {/* Show first 10 companies */}
            <CompanyTable companies={companies.slice(0, 10)} buttonStyles={buttonStyles} />
            
            {/* View All Companies CTA */}
            <div className="view-all-section">
              <Link to="/companies" className="view-all-btn">
                <span>View All {pagination.count} Companies</span>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <polyline points="9 18 15 12 9 6"></polyline>
                </svg>
              </Link>
            </div>
          </div>

          {/* Homepage Sections */}
          {!sectionsLoading && homepageSections && (
            <HomepageSections sections={homepageSections} />
          )}
        </>
      )}
    </div>
  );
}

export default CompanyList;
