import { useState, useEffect, useCallback } from 'react';
import JobCard from '../components/JobCard';
import { getApiUrl } from '../services/api';
import { useAuth } from '../context/AuthContext';
import './JobBoard.css';

function JobBoard() {
  const { token } = useAuth();
  const [jobs, setJobs] = useState([]);
  const [filters, setFilters] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Pagination state
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalCount, setTotalCount] = useState(0);

  // Preferences
  const [showAllJobs, setShowAllJobs] = useState(false);
  const [hasPreferences, setHasPreferences] = useState(false);
  const [tooltipVisible, setTooltipVisible] = useState(false);

  // Filter state
  const [search, setSearch] = useState('');
  const [employmentType, setEmploymentType] = useState('');
  const [experienceLevel, setExperienceLevel] = useState('');
  const [location, setLocation] = useState('');
  const [remoteOnly, setRemoteOnly] = useState(false);
  const [ordering, setOrdering] = useState('-published_at');

  // Debounced search
  const [searchDebounced, setSearchDebounced] = useState('');
  useEffect(() => {
    const timer = setTimeout(() => setSearchDebounced(search), 350);
    return () => clearTimeout(timer);
  }, [search]);

  // Fetch filter options + user preferences
  useEffect(() => {
    const fetchFilters = async () => {
      try {
        const res = await fetch(getApiUrl('recruiters/job-board/filters/'), {
          headers: { 'Authorization': `Token ${token}` }
        });
        if (res.ok) {
          const data = await res.json();
          setFilters(data);
        }
      } catch (err) {
        console.error('Failed to fetch filters:', err);
      }
    };
    const fetchPreferences = async () => {
      try {
        const res = await fetch(getApiUrl('accounts/job-preferences/me/'), {
          headers: { 'Authorization': `Token ${token}` }
        });
        if (res.ok) {
          const data = await res.json();
          const hasFunctions = data.desired_functions && data.desired_functions.length > 0;
          const hasEnvs = data.work_environments && data.work_environments.length > 0;
          setHasPreferences(hasFunctions || hasEnvs);
        }
      } catch (err) {
        console.error('Failed to fetch preferences:', err);
      }
    };
    fetchFilters();
    fetchPreferences();
  }, []);

  // Fetch jobs
  const fetchJobs = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams();
      if (searchDebounced) params.set('search', searchDebounced);
      if (employmentType) params.set('employment_type', employmentType);
      if (experienceLevel) params.set('experience_level', experienceLevel);
      if (location) params.set('location', location);
      if (remoteOnly) params.set('remote', 'true');
      if (ordering) params.set('ordering', ordering);
      if (hasPreferences && !showAllJobs) params.set('preferences', 'true');
      params.set('page', page);

      const url = `${getApiUrl('recruiters/job-board/')}?${params.toString()}`;
      const res = await fetch(url, {
        headers: { 'Authorization': `Token ${token}` }
      });
      if (!res.ok) throw new Error('Failed to fetch jobs');
      const data = await res.json();
      // DRF can return paginated or list
      if (data.results) {
        setJobs(data.results);
        setTotalPages(data.total_pages || 1);
        setTotalCount(data.count || data.results.length);
      } else {
        setJobs(Array.isArray(data) ? data : []);
        setTotalPages(1);
        setTotalCount(Array.isArray(data) ? data.length : 0);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [searchDebounced, employmentType, experienceLevel, location, remoteOnly, ordering, page, showAllJobs, hasPreferences]);

  useEffect(() => {
    fetchJobs();
  }, [fetchJobs]);

  const clearFilters = () => {
    setSearch('');
    setEmploymentType('');
    setExperienceLevel('');
    setLocation('');
    setRemoteOnly(false);
    setOrdering('-published_at');
    setPage(1);
  };

  // Reset page when filters change
  useEffect(() => {
    setPage(1);
  }, [searchDebounced, employmentType, experienceLevel, location, remoteOnly, ordering, showAllJobs]);

  const hasActiveFilters = search || employmentType || experienceLevel || location || remoteOnly;

  return (
    <div className="job-board">
      {/* Hero */}
      <div className="job-board-hero">
        <h1 className="job-board-title">Job Openings</h1>
        <p className="job-board-subtitle">
          Browse {filters?.total_jobs || ''} open positions from companies hiring in tech
        </p>
      </div>

      {/* Filters Bar */}
      <div className="job-board-filters">
        {hasPreferences && (
          <div className="job-board-pref-row">
            <label className="job-board-pref-toggle">
              <input
                type="checkbox"
                checked={showAllJobs}
                onChange={(e) => setShowAllJobs(e.target.checked)}
              />
              <span className="job-board-pref-label">Show me all jobs</span>
            </label>
            <div
              className="job-board-pref-tooltip-wrapper"
              onMouseEnter={() => setTooltipVisible(true)}
              onMouseLeave={() => setTooltipVisible(false)}
            >
              <svg className="job-board-pref-info-icon" width="16" height="16" viewBox="0 0 16 16" fill="none">
                <circle cx="8" cy="8" r="7" stroke="currentColor" strokeWidth="1.5"/>
                <path d="M8 7V11" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                <circle cx="8" cy="5" r="0.75" fill="currentColor"/>
              </svg>
              {tooltipVisible && (
                <div className="job-board-pref-tooltip">
                  When unchecked, we show jobs matching your preferred job functions and work environment. Check this to browse all available openings.
                </div>
              )}
            </div>
            {!showAllJobs && (
              <span className="job-board-pref-active-badge">Showing preferred jobs</span>
            )}
          </div>
        )}
        <div className="job-board-search-row">
          <div className="job-board-search-wrapper">
            <svg className="job-board-search-icon" width="18" height="18" viewBox="0 0 18 18" fill="none">
              <circle cx="8" cy="8" r="6" stroke="currentColor" strokeWidth="1.5"/>
              <path d="M13 13L16 16" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
            </svg>
            <input
              type="text"
              className="job-board-search"
              placeholder="Search jobs, companies, skills..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
        </div>

        <div className="job-board-filter-row">
          <select
            className="job-board-select"
            value={employmentType}
            onChange={(e) => setEmploymentType(e.target.value)}
          >
            <option value="">All Types</option>
            {filters?.employment_types?.map((t) => (
              <option key={t.value} value={t.value}>{t.label}</option>
            ))}
          </select>

          <select
            className="job-board-select"
            value={experienceLevel}
            onChange={(e) => setExperienceLevel(e.target.value)}
          >
            <option value="">All Levels</option>
            {filters?.experience_levels?.map((l) => (
              <option key={l.value} value={l.value}>{l.label}</option>
            ))}
          </select>

          <input
            type="text"
            className="job-board-select job-board-location-input"
            placeholder="Location..."
            value={location}
            onChange={(e) => setLocation(e.target.value)}
          />

          <label className="job-board-toggle">
            <input
              type="checkbox"
              checked={remoteOnly}
              onChange={(e) => setRemoteOnly(e.target.checked)}
            />
            <span className="job-board-toggle-label">Remote Only</span>
          </label>

          <select
            className="job-board-select"
            value={ordering}
            onChange={(e) => setOrdering(e.target.value)}
          >
            <option value="-published_at">Newest First</option>
            <option value="published_at">Oldest First</option>
            <option value="title">Title A-Z</option>
            <option value="-title">Title Z-A</option>
            <option value="-salary_min">Highest Salary</option>
          </select>

          {hasActiveFilters && (
            <button className="job-board-clear-btn" onClick={clearFilters}>
              Clear Filters
            </button>
          )}
        </div>
      </div>

      {/* Results */}
      <div className="job-board-results">
        {loading ? (
          <div className="job-board-loading">
            <div className="job-board-spinner" />
            <p>Loading jobs...</p>
          </div>
        ) : error ? (
          <div className="job-board-error">
            <p>Something went wrong. Please try again.</p>
            <button onClick={fetchJobs} className="job-board-retry-btn">Retry</button>
          </div>
        ) : jobs.length === 0 ? (
          <div className="job-board-empty">
            <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
              <rect x="8" y="12" width="32" height="28" rx="3" stroke="currentColor" strokeWidth="2" opacity="0.3"/>
              <path d="M16 12V9C16 7.34 17.34 6 19 6H29C30.66 6 32 7.34 32 9V12" stroke="currentColor" strokeWidth="2" opacity="0.3"/>
              <path d="M18 24H30M18 30H26" stroke="currentColor" strokeWidth="2" strokeLinecap="round" opacity="0.3"/>
            </svg>
            <h3>No jobs found</h3>
            <p>Try adjusting your filters or search terms</p>
            {hasActiveFilters && (
              <button className="job-board-clear-btn" onClick={clearFilters}>
                Clear All Filters
              </button>
            )}
          </div>
        ) : (
          <>
            <div className="job-board-count">
              {totalCount} job{totalCount !== 1 ? 's' : ''} found
              {totalPages > 1 && <span className="job-board-page-info"> — Page {page} of {totalPages}</span>}
            </div>
            <div className="job-board-grid">
              {jobs.map((job) => (
                <JobCard key={job.id} job={job} />
              ))}
            </div>
            {totalPages > 1 && (
              <div className="job-board-pagination">
                <button
                  className="job-board-page-btn"
                  onClick={() => { setPage(p => p - 1); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
                  disabled={page <= 1}
                >
                  ← Previous
                </button>
                <div className="job-board-page-numbers">
                  {Array.from({ length: totalPages }, (_, i) => i + 1)
                    .filter(p => p === 1 || p === totalPages || Math.abs(p - page) <= 2)
                    .reduce((acc, p, idx, arr) => {
                      if (idx > 0 && p - arr[idx - 1] > 1) acc.push('...');
                      acc.push(p);
                      return acc;
                    }, [])
                    .map((p, idx) =>
                      p === '...' ? (
                        <span key={`dots-${idx}`} className="job-board-page-dots">...</span>
                      ) : (
                        <button
                          key={p}
                          className={`job-board-page-num ${p === page ? 'active' : ''}`}
                          onClick={() => { setPage(p); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
                        >
                          {p}
                        </button>
                      )
                    )}
                </div>
                <button
                  className="job-board-page-btn"
                  onClick={() => { setPage(p => p + 1); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
                  disabled={page >= totalPages}
                >
                  Next →
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default JobBoard;
