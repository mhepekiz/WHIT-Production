import { useState, useEffect } from 'react';
import { useOutletContext } from 'react-router-dom';
import { searchCandidates, getCandidateSearches } from '../services/recruiterApi';
import './CandidateSearch.css';

function CandidateSearch() {
  const [candidates, setCandidates] = useState([]);
  const [searchHistory, setSearchHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [searchParams, setSearchParams] = useState({
    query: '',
    skills: '',
    location: '',
    experience_level: '',
    employment_type: '',
    remote_only: false,
    actively_looking: false,
  });
  const [usage, setUsage] = useState(null);
  const [savedTemplates, setSavedTemplates] = useState([]);
  const [showSaveModal, setShowSaveModal] = useState(false);
  const [templateName, setTemplateName] = useState('');
  const [showTemplatesDropdown, setShowTemplatesDropdown] = useState(false);

  let context = {};
  try {
    context = useOutletContext();
  } catch (e) {
    console.log('No outlet context available');
  }

  const { profile } = context || {};

  useEffect(() => {
    fetchSearchHistory();
    loadSavedTemplates();
  }, []);

  const fetchSearchHistory = async () => {
    try {
      const data = await getCandidateSearches();
      setSearchHistory(data.results || data || []);
    } catch (err) {
      console.error('Failed to fetch search history:', err);
    }
  };

  const loadSavedTemplates = () => {
    const saved = localStorage.getItem('searchTemplates');
    if (saved) {
      setSavedTemplates(JSON.parse(saved));
    }
  };

  const saveSearchTemplate = () => {
    if (!templateName.trim()) {
      alert('Please enter a template name');
      return;
    }

    const newTemplate = {
      id: Date.now(),
      name: templateName,
      params: { ...searchParams },
      createdAt: new Date().toISOString(),
    };

    const updatedTemplates = [...savedTemplates, newTemplate];
    setSavedTemplates(updatedTemplates);
    localStorage.setItem('searchTemplates', JSON.stringify(updatedTemplates));
    
    setShowSaveModal(false);
    setTemplateName('');
  };

  const loadTemplate = (template) => {
    setSearchParams(template.params);
    setShowTemplatesDropdown(false);
  };

  const deleteTemplate = (templateId) => {
    const updatedTemplates = savedTemplates.filter(t => t.id !== templateId);
    setSavedTemplates(updatedTemplates);
    localStorage.setItem('searchTemplates', JSON.stringify(updatedTemplates));
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const searchData = {
        ...searchParams,
        skills: searchParams.skills ? searchParams.skills.split(',').map(s => s.trim()) : [],
      };

      const data = await searchCandidates(searchData);
      setCandidates(data.results || []);
      setUsage(data.usage);
      fetchSearchHistory(); // Refresh search history
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to search candidates');
      console.error('Search error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setSearchParams(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleClearSearch = () => {
    setSearchParams({
      query: '',
      skills: '',
      location: '',
      experience_level: '',
      employment_type: '',
      remote_only: false,
      actively_looking: false,
    });
    setCandidates([]);
    setUsage(null);
  };

  const hasActiveFilters = () => {
    return searchParams.query || searchParams.skills || searchParams.location ||
           searchParams.experience_level || searchParams.employment_type ||
           searchParams.remote_only || searchParams.actively_looking;
  };

  return (
    <div className="candidate-search-container">
      <div className="page-header">
        <div className="header-content">
          <h2>Search Candidates</h2>
          <p>Find qualified candidates based on their preferences and experience</p>
        </div>
        {usage && (
          <div className="usage-info">
            <div className="usage-stats">
              <span className="usage-label">Searches Used:</span>
              <span className="usage-value">{usage.used} / {usage.limit === 0 ? '∞' : usage.limit}</span>
            </div>
          </div>
        )}
      </div>

      {error && (
        <div className="alert alert-error">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <circle cx="10" cy="10" r="8" stroke="currentColor" strokeWidth="2"/>
            <path d="M10 6V10" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
            <circle cx="10" cy="14" r="1" fill="currentColor"/>
          </svg>
          {error}
        </div>
      )}

      <div className="search-layout">
        {/* Search Filters */}
        <div className="search-sidebar">
          <div className="search-form-card">
            <h3>Search Filters</h3>
            <form onSubmit={handleSearch}>
              <div className="form-group">
                <label htmlFor="query">Keywords</label>
                <input
                  type="text"
                  id="query"
                  name="query"
                  value={searchParams.query}
                  onChange={handleInputChange}
                  placeholder="Name, title, bio..."
                />
              </div>

              <div className="form-group">
                <label htmlFor="skills">Skills</label>
                <input
                  type="text"
                  id="skills"
                  name="skills"
                  value={searchParams.skills}
                  onChange={handleInputChange}
                  placeholder="React, Python, Marketing... (comma-separated)"
                />
              </div>

              <div className="form-group">
                <label htmlFor="location">Location</label>
                <input
                  type="text"
                  id="location"
                  name="location"
                  value={searchParams.location}
                  onChange={handleInputChange}
                  placeholder="City, State, or Country"
                />
              </div>

              <div className="form-group">
                <label htmlFor="experience_level">Experience Level</label>
                <select
                  id="experience_level"
                  name="experience_level"
                  value={searchParams.experience_level}
                  onChange={handleInputChange}
                >
                  <option value="">All Levels</option>
                  <option value="entry">Entry Level (0-2 years)</option>
                  <option value="mid">Mid Level (3-5 years)</option>
                  <option value="senior">Senior (6-10 years)</option>
                  <option value="lead">Lead/Principal (10+ years)</option>
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="employment_type">Employment Type</label>
                <select
                  id="employment_type"
                  name="employment_type"
                  value={searchParams.employment_type}
                  onChange={handleInputChange}
                >
                  <option value="">All Types</option>
                  <option value="full-time">Full Time</option>
                  <option value="part-time">Part Time</option>
                  <option value="contract">Contract</option>
                  <option value="internship">Internship</option>
                </select>
              </div>

              <div className="checkbox-group">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    name="remote_only"
                    checked={searchParams.remote_only}
                    onChange={handleInputChange}
                  />
                  <span>Remote Only</span>
                </label>

                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    name="actively_looking"
                    checked={searchParams.actively_looking}
                    onChange={handleInputChange}
                  />
                  <span>Actively Looking</span>
                </label>
              </div>

              <div className="form-actions">
                <button type="submit" className="btn btn-primary" disabled={loading}>
                  {loading ? (
                    <>
                      <span className="spinner"></span>
                      Searching...
                    </>
                  ) : (
                    <>
                      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                        <circle cx="7" cy="7" r="5" stroke="currentColor" strokeWidth="2"/>
                        <path d="M11 11L14 14" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                      </svg>
                      Search Candidates
                    </>
                  )}
                </button>
                
                {hasActiveFilters() && (
                  <button type="button" className="btn btn-save" onClick={() => setShowSaveModal(true)}>
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                      <path d="M12 1H4C2.89543 1 2 1.89543 2 3V13C2 14.1046 2.89543 15 4 15H12C13.1046 15 14 14.1046 14 13V3C14 1.89543 13.1046 1 12 1Z" stroke="currentColor" strokeWidth="1.5"/>
                      <path d="M5 5H11M5 8H11M5 11H8" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                    </svg>
                    Save Template
                  </button>
                )}
                
                {savedTemplates.length > 0 && (
                  <div className="templates-dropdown">
                    <button 
                      type="button" 
                      className="btn btn-template" 
                      onClick={() => setShowTemplatesDropdown(!showTemplatesDropdown)}
                    >
                      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                        <rect x="2" y="3" width="5" height="4" rx="1" stroke="currentColor" strokeWidth="1.5"/>
                        <rect x="9" y="3" width="5" height="4" rx="1" stroke="currentColor" strokeWidth="1.5"/>
                        <rect x="2" y="9" width="5" height="4" rx="1" stroke="currentColor" strokeWidth="1.5"/>
                        <rect x="9" y="9" width="5" height="4" rx="1" stroke="currentColor" strokeWidth="1.5"/>
                      </svg>
                      Templates ({savedTemplates.length})
                    </button>
                      {showTemplatesDropdown && (
                        <div className="templates-menu">
                          {savedTemplates.map(template => (
                            <div key={template.id} className="template-item">
                              <button 
                                type="button" 
                                onClick={() => loadTemplate(template)}
                                className="template-load"
                              >
                                <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                                  <path d="M5 7L7 9L12 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                                </svg>
                                {template.name}
                              </button>
                              <button 
                                type="button"
                                onClick={() => deleteTemplate(template.id)}
                                className="template-delete"
                              >
                                <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                                  <path d="M3 3L11 11M11 3L3 11" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                                </svg>
                              </button>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                
                {hasActiveFilters() && (
                  <button type="button" className="btn btn-secondary" onClick={handleClearSearch}>
                    Clear Filters
                  </button>
                )}
              </div>
            </form>
          </div>

          {/* Search History */}
          {searchHistory.length > 0 && (
            <div className="search-history-card">
              <h3>Recent Searches</h3>
              <div className="history-list">
                {searchHistory.slice(0, 5).map((search, index) => (
                  <div key={index} className="history-item">
                    <div className="history-query">
                      {search.search_query || 'General search'}
                    </div>
                    <div className="history-date">
                      {new Date(search.searched_at).toLocaleDateString()}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Search Results */}
        <div className="search-results">
          {loading ? (
            <div className="loading">Searching candidates...</div>
          ) : candidates.length > 0 ? (
            <>
              <div className="results-header">
                <h3>{candidates.length} Candidate{candidates.length !== 1 ? 's' : ''} Found</h3>
              </div>
              <div className="candidates-grid">
                {candidates.map((candidate) => (
                  <div key={candidate.id} className="candidate-card">
                    <div className="candidate-header">
                      <div className="candidate-avatar">
                        {candidate.name.split(' ').map(n => n[0]).join('').toUpperCase()}
                      </div>
                      <div className="candidate-info">
                        <h4>{candidate.name}</h4>
                        {candidate.current_title && (
                          <p className="candidate-title">{candidate.current_title}</p>
                        )}
                        {candidate.location && (
                          <p className="candidate-location">
                            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                              <path d="M7 7C7.82843 7 8.5 6.32843 8.5 5.5C8.5 4.67157 7.82843 4 7 4C6.17157 4 5.5 4.67157 5.5 5.5C5.5 6.32843 6.17157 7 7 7Z" stroke="currentColor" strokeWidth="1.5"/>
                              <path d="M11 5.5C11 9 7 12 7 12C7 12 3 9 3 5.5C3 3.567 4.567 2 7 2C9.433 2 11 3.567 11 5.5Z" stroke="currentColor" strokeWidth="1.5"/>
                            </svg>
                            {candidate.location}
                          </p>
                        )}
                      </div>
                    </div>

                    {candidate.bio && (
                      <div className="candidate-bio">
                        <p>{candidate.bio.length > 150 ? candidate.bio.substring(0, 150) + '...' : candidate.bio}</p>
                      </div>
                    )}

                    <div className="candidate-details">
                      {candidate.years_of_experience !== undefined && (
                        <div className="detail-item">
                          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                            <rect x="3" y="4" width="10" height="9" rx="1" stroke="currentColor" strokeWidth="1.5"/>
                            <path d="M6 4V3C6 2.44772 6.44772 2 7 2H9C9.55228 2 10 2.44772 10 3V4" stroke="currentColor" strokeWidth="1.5"/>
                          </svg>
                          <span>{candidate.years_of_experience} years exp.</span>
                        </div>
                      )}
                      {candidate.employment_types && (
                        <div className="detail-item">
                          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                            <circle cx="8" cy="8" r="6" stroke="currentColor" strokeWidth="1.5"/>
                            <path d="M8 4V8L11 10" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                          </svg>
                          <span>{candidate.employment_types}</span>
                        </div>
                      )}
                      {candidate.remote_only && (
                        <div className="detail-item remote-badge">
                          <span>Remote Only</span>
                        </div>
                      )}
                      {candidate.actively_looking && (
                        <div className="detail-item active-badge">
                          <span>🟢 Actively Looking</span>
                        </div>
                      )}
                    </div>

                    {candidate.desired_functions && candidate.desired_functions.length > 0 && (
                      <div className="candidate-skills">
                        {candidate.desired_functions.slice(0, 5).map((func, idx) => (
                          <span key={idx} className="skill-tag">{func}</span>
                        ))}
                        {candidate.desired_functions.length > 5 && (
                          <span className="skill-tag more">+{candidate.desired_functions.length - 5} more</span>
                        )}
                      </div>
                    )}

                    <div className="candidate-actions">
                      {candidate.email && (
                        <a href={`mailto:${candidate.email}`} className="btn btn-primary btn-small">
                          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                            <rect x="2" y="3" width="10" height="8" rx="1" stroke="currentColor" strokeWidth="1.5"/>
                            <path d="M2 4L7 8L12 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                          </svg>
                          Contact
                        </a>
                      )}
                      {candidate.linkedin_url && (
                        <a href={candidate.linkedin_url} target="_blank" rel="noopener noreferrer" className="btn btn-secondary btn-small">
                          LinkedIn
                        </a>
                      )}
                      {!candidate.email && !candidate.linkedin_url && (
                        <button className="btn btn-secondary btn-small" disabled>
                          Upgrade to Contact
                        </button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </>
          ) : hasActiveFilters() ? (
            <div className="empty-state">
              <svg width="64" height="64" viewBox="0 0 64 64" fill="none">
                <circle cx="28" cy="28" r="20" stroke="currentColor" strokeWidth="4"/>
                <path d="M44 44L56 56" stroke="currentColor" strokeWidth="4" strokeLinecap="round"/>
              </svg>
              <h3>No candidates found</h3>
              <p>Try adjusting your search filters to find more candidates</p>
            </div>
          ) : (
            <div className="empty-state">
              <svg width="64" height="64" viewBox="0 0 64 64" fill="none">
                <circle cx="32" cy="20" r="12" stroke="currentColor" strokeWidth="4"/>
                <path d="M8 56C8 43.8497 17.8497 34 30 34H34C46.1503 34 56 43.8497 56 56" stroke="currentColor" strokeWidth="4"/>
              </svg>
              <h3>Start Your Candidate Search</h3>
              <p>Use the filters on the left to search for qualified candidates</p>
            </div>
          )}
        </div>
      </div>

      {/* Save Template Modal */}
      {showSaveModal && (
        <div className="modal-overlay" onClick={() => setShowSaveModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Save Search Template</h3>
              <button className="modal-close" onClick={() => setShowSaveModal(false)}>
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path d="M5 5L15 15M15 5L5 15" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                </svg>
              </button>
            </div>
            <div className="modal-body">
              <p>Save your current search filters as a template for quick access later.</p>
              <div className="form-group">
                <label htmlFor="templateName">Template Name</label>
                <input
                  type="text"
                  id="templateName"
                  value={templateName}
                  onChange={(e) => setTemplateName(e.target.value)}
                  placeholder="e.g., Senior Engineers in SF"
                  autoFocus
                />
              </div>
              <div className="template-preview">
                <h4>Current Filters:</h4>
                <div className="filter-tags">
                  {searchParams.query && <span className="filter-tag">Query: {searchParams.query}</span>}
                  {searchParams.skills && <span className="filter-tag">Skills: {searchParams.skills}</span>}
                  {searchParams.location && <span className="filter-tag">Location: {searchParams.location}</span>}
                  {searchParams.experience_level && <span className="filter-tag">Experience: {searchParams.experience_level}</span>}
                  {searchParams.employment_type && <span className="filter-tag">Type: {searchParams.employment_type}</span>}
                  {searchParams.remote_only && <span className="filter-tag">Remote Only</span>}
                  {searchParams.actively_looking && <span className="filter-tag">Actively Looking</span>}
                </div>
              </div>
            </div>
            <div className="modal-footer">
              <button className="btn btn-secondary" onClick={() => setShowSaveModal(false)}>
                Cancel
              </button>
              <button className="btn btn-primary" onClick={saveSearchTemplate}>
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <path d="M12 1H4C2.89543 1 2 1.89543 2 3V13C2 14.1046 2.89543 15 4 15H12C13.1046 15 14 14.1046 14 13V3C14 1.89543 13.1046 1 12 1Z" stroke="currentColor" strokeWidth="1.5"/>
                  <path d="M5 5H11M5 8H11M5 11H8" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                </svg>
                Save Template
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default CandidateSearch;
