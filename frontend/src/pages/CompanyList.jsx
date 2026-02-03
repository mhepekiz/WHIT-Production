import { useState, useEffect } from 'react';
import { companyService } from '../services/api';
import CompanyTable from '../components/CompanyTable';
import Filters from '../components/Filters';
import SearchBar from '../components/SearchBar';
import Stats from '../components/Stats';
import './CompanyList.css';

function CompanyList() {
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
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
        const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
        const response = await fetch(`${API_BASE_URL}/ad-slots/active/`);
        if (response.ok) {
          const data = await response.json();
          console.log('Ad slots data:', data);
          setAdSlots(data);
        }
      } catch (err) {
        console.error('Failed to fetch ad slots:', err);
      }
    };

    const fetchSiteSettings = async () => {
      try {
        const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
        const response = await fetch(`${API_BASE_URL}/site-settings/current/`);
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
          
          console.log('Applied sizes:', sizes);
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
        params.page_size = 30;

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
      <div className="search-section">
        <SearchBar onSearch={handleSearch} initialValue={filters.search} />
      </div>

      {availableFilters && (
        <Filters
          filters={filters}
          availableFilters={availableFilters}
          onFilterChange={handleFilterChange}
          onReset={resetFilters}
        />
      )}

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
          {/* First group of 10 companies */}
          <CompanyTable companies={companies.slice(0, 10)} buttonStyles={buttonStyles} />

          {/* First Ad Slot */}
          {adSlots.slot1 && (
            <div className="ad-slot">
              {adSlots.slot1.type === 'image' ? (
                <a 
                  href={adSlots.slot1.link} 
                  target={adSlots.slot1.open_in_new_tab ? '_blank' : '_self'}
                  rel={adSlots.slot1.open_in_new_tab ? 'noopener noreferrer' : ''}
                  className="ad-banner-link"
                >
                  <img 
                    src={adSlots.slot1.image_url} 
                    alt={adSlots.slot1.alt_text}
                    className="ad-banner-image"
                  />
                </a>
              ) : (
                <div dangerouslySetInnerHTML={{ __html: adSlots.slot1.code }} />
              )}
            </div>
          )}

          {/* Second group of 10 companies */}
          {companies.length > 10 && (
            <CompanyTable companies={companies.slice(10, 20)} buttonStyles={buttonStyles} />
          )}

          {/* Second Ad Slot */}
          {companies.length > 10 && adSlots.slot2 && (
            <div className="ad-slot">
              {adSlots.slot2.type === 'image' ? (
                <a 
                  href={adSlots.slot2.link} 
                  target={adSlots.slot2.open_in_new_tab ? '_blank' : '_self'}
                  rel={adSlots.slot2.open_in_new_tab ? 'noopener noreferrer' : ''}
                  className="ad-banner-link"
                >
                  <img 
                    src={adSlots.slot2.image_url} 
                    alt={adSlots.slot2.alt_text}
                    className="ad-banner-image"
                  />
                </a>
              ) : (
                <div dangerouslySetInnerHTML={{ __html: adSlots.slot2.code }} />
              )}
            </div>
          )}

          {/* Third group of 10 companies */}
          {companies.length > 20 && (
            <CompanyTable companies={companies.slice(20, 30)} buttonStyles={buttonStyles} />
          )}

          {/* Pagination */}
          <div className="pagination">
            <button
              onClick={() => handlePageChange(pagination.currentPage - 1)}
              disabled={!pagination.previous}
              className="pagination-btn"
            >
              Previous
            </button>
            <span className="pagination-info">
              Page {pagination.currentPage} of {Math.ceil(pagination.count / 30)}
            </span>
            <button
              onClick={() => handlePageChange(pagination.currentPage + 1)}
              disabled={!pagination.next}
              className="pagination-btn"
            >
              Next
            </button>
          </div>
        </>
      )}
    </div>
  );
}

export default CompanyList;
