import { useState, useEffect } from 'react';
import DOMPurify from 'dompurify';
import { companyService } from '../services/api';
import CompanyTable from '../components/CompanyTable';
import Filters from '../components/Filters';
import SearchBar from '../components/SearchBar';
import './CompanyList.css';

function CompanyBrowse() {
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
  const [companiesPerPage, setCompaniesPerPage] = useState(30);
  const [companiesPerGroup, setCompaniesPerGroup] = useState(10);
  const [adSlots, setAdSlots] = useState({
    slot1: null,
    slot2: null,
  });
  const [filtersVisible, setFiltersVisible] = useState(true);

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
        const response = await fetch(`${import.meta.env.VITE_API_URL || '/api'}/ad-slots/active/`);
        const data = await response.json();
        
        const slotsObject = {};
        data.forEach(slot => {
          if (slot.slot_id) {
            slotsObject[slot.slot_id] = {
              type: slot.ad_type || 'image',
              image_url: slot.banner_image,
              mobile_image_url: slot.mobile_banner_image,
              link: slot.link,
              alt_text: slot.banner_alt_text || 'Advertisement',
              code: slot.custom_code,
              open_in_new_tab: slot.open_in_new_tab || true,
            };
          }
        });
        
        setAdSlots(slotsObject);
      } catch (err) {
        console.error('Failed to fetch ad slots:', err);
      }
    };

    const fetchSiteSettings = async () => {
      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL || '/api'}/site-settings/current/`);
        if (response.ok) {
          const data = await response.json();
          if (data.companies_per_page) setCompaniesPerPage(data.companies_per_page);
          if (data.companies_per_group) setCompaniesPerGroup(data.companies_per_group);
          if (data.label_size) {
            setLabelSize(data.label_size);
            const sizeMap = {
              'small': { padding: '4px 8px', fontSize: '0.65rem' },
              'medium': { padding: '6px 12px', fontSize: '0.75rem' },
              'large': { padding: '8px 16px', fontSize: '0.85rem' },
              'extra-large': { padding: '10px 20px', fontSize: '0.95rem' }
            };
            setButtonStyles(sizeMap[data.label_size] || sizeMap['medium']);
          }
        }
      } catch (err) {
        console.error('Failed to fetch site settings:', err);
      }
    };

    fetchFilters();
    fetchAdSlots();
    fetchSiteSettings();
  }, []);

  // Fetch companies when filters or page changes
  useEffect(() => {
    const fetchCompanies = async () => {
      setLoading(true);
      try {
        const params = new URLSearchParams();
        
        // Add all filters to params
        Object.entries(filters).forEach(([key, value]) => {
          if (value && value !== '') {
            params.append(key, value);
          }
        });
        
        // Add pagination
        params.append('page', pagination.currentPage.toString());
        params.append('page_size', companiesPerPage.toString());
        
        const data = await companyService.getCompanies(params);
        setCompanies(data.results || data);
        setPagination({
          count: data.count || 0,
          next: data.next || null,
          previous: data.previous || null,
          currentPage: pagination.currentPage,
        });
      } catch (err) {
        setError('Failed to fetch companies. Please try again.');
        console.error('Error fetching companies:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchCompanies();
  }, [filters, pagination.currentPage, companiesPerPage]);

  const handleFilterChange = (filterType, value) => {
    setFilters(prev => ({
      ...prev,
      [filterType]: value
    }));
    setPagination(prev => ({ ...prev, currentPage: 1 }));
  };

  const handleSearch = (searchTerm) => {
    setFilters(prev => ({
      ...prev,
      search: searchTerm
    }));
    setPagination(prev => ({ ...prev, currentPage: 1 }));
  };

  const handlePageChange = (page) => {
    if (page >= 1 && page <= Math.ceil(pagination.count / companiesPerPage)) {
      setPagination(prev => ({ ...prev, currentPage: page }));
      // Scroll to top when changing pages
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const resetFilters = () => {
    setFilters({
      search: '',
      country: '',
      state: '',
      city: '',
      functions: '',
      work_environment: '',
      status: 'Active',
    });
    setPagination(prev => ({ ...prev, currentPage: 1 }));
  };

  return (
    <div className="company-list-page">
      <div className="page-header">
        <h1 className="page-title">All Companies</h1>
        <p className="page-subtitle">Browse all {pagination.count} hiring companies</p>
      </div>

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
          {/* Results summary */}
          {companies.length > 0 && (
            <div className="results-summary">
              <p>Showing {((pagination.currentPage - 1) * companiesPerPage) + 1}-{Math.min(pagination.currentPage * companiesPerPage, pagination.count)} of {pagination.count} companies</p>
            </div>
          )}

          {/* Render companies in groups with ad slots between them */}
          {(() => {
            const groups = [];
            const numGroups = Math.ceil(companies.length / companiesPerGroup);
            for (let i = 0; i < numGroups; i++) {
              const start = i * companiesPerGroup;
              const end = start + companiesPerGroup;
              groups.push(
                <div key={`group-${i}`}>
                  <CompanyTable companies={companies.slice(start, end)} buttonStyles={buttonStyles} />
                  {/* Show ad slot after first group */}
                  {i === 0 && adSlots.slot1 && (
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
                      ) : adSlots.slot1.code ? (
                        <div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(adSlots.slot1.code) }} />
                      ) : null}
                    </div>
                  )}
                  {/* Show ad slot after second group */}}
                  {i === 1 && adSlots.slot2 && (
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
                      ) : adSlots.slot2.code ? (
                        <div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(adSlots.slot2.code) }} />
                      ) : null}
                    </div>
                  )}
                </div>
              );
            }
            return groups;
          })()}

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
              Page {pagination.currentPage} of {Math.ceil(pagination.count / companiesPerPage)}
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

export default CompanyBrowse;