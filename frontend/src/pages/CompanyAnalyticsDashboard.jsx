import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useRecruiterAuth } from '../contexts/RecruiterAuthContext';
import { 
  getAccessibleCompanies, 
  getCompanyStatistics, 
  getDashboardOverview,
  exportCompanyData 
} from '../services/recruiterApi';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { 
  faBuilding, 
  faChartBar, 
  faBullseye, 
  faFileAlt,
  faFileExport
} from '@fortawesome/free-solid-svg-icons';
import './CompanyAnalyticsDashboard.css';

function CompanyAnalyticsDashboard() {
  const navigate = useNavigate();
  const { isAuthenticated } = useRecruiterAuth();
  const [companies, setCompanies] = useState([]);
  const [selectedCompany, setSelectedCompany] = useState(null);
  const [statistics, setStatistics] = useState(null);
  const [overview, setOverview] = useState(null);
  const [dateRange, setDateRange] = useState(30);
  const [loading, setLoading] = useState(true);
  const [statsLoading, setStatsLoading] = useState(false);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/recruiter/login');
      return;
    }
    
    fetchInitialData();
  }, [isAuthenticated, navigate]);

  useEffect(() => {
    if (selectedCompany) {
      fetchCompanyStatistics();
    }
  }, [selectedCompany, dateRange]);

  const fetchInitialData = async () => {
    try {
      setLoading(true);
      console.log('🔄 Fetching initial data...');
      const [companiesData, overviewData] = await Promise.all([
        getAccessibleCompanies(),
        getDashboardOverview()
      ]);
      
      console.log('📊 Companies data received:', companiesData);
      console.log('📈 Overview data received:', overviewData);
      
      setCompanies(companiesData);
      setOverview(overviewData);
      
      // Auto-select first company if available
      const firstCompanyWithStats = companiesData.find(c => c.access_info?.can_see_sponsored_stats);
      if (firstCompanyWithStats) {
        console.log('🎯 Auto-selecting first company:', firstCompanyWithStats.name);
        setSelectedCompany(firstCompanyWithStats);
      } else {
        console.log('⚠️ No companies with stats access found');
      }
    } catch (error) {
      console.error('❌ Error fetching initial data:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchCompanyStatistics = async () => {
    if (!selectedCompany?.access_info?.can_see_sponsored_stats) return;
    
    try {
      setStatsLoading(true);
      const statsData = await getCompanyStatistics(selectedCompany.id, dateRange);
      setStatistics(statsData);
    } catch (error) {
      console.error('Error fetching company statistics:', error);
    } finally {
      setStatsLoading(false);
    }
  };

  const handleExportData = async (companyId) => {
    try {
      await exportCompanyData(companyId, dateRange);
    } catch (error) {
      console.error('Error exporting data:', error);
    }
  };

  const formatNumber = (num) => {
    if (num === null || num === undefined) return '0';
    return num.toLocaleString();
  };

  const formatPercentage = (num) => {
    if (num === null || num === undefined) return '0.00%';
    return `${parseFloat(num).toFixed(2)}%`;
  };

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="spinner"></div>
        <p>Loading dashboard...</p>
      </div>
    );
  }

  const companiesWithStats = companies.filter(c => c.access_info?.can_see_sponsored_stats);

  return (
    <div className="company-analytics-dashboard">
      <div className="dashboard-header">
        <h1>Company Analytics Dashboard</h1>
        <p>Monitor performance of sponsored company listings</p>
      </div>

      {/* Overview Cards */}
      {overview && (
        <div className="overview-cards">
          <div className="overview-card">
            <div className="card-icon">
              <FontAwesomeIcon icon={faBuilding} />
            </div>
            <div className="card-content">
              <h3>{overview.accessible_companies}</h3>
              <p>Accessible Companies</p>
            </div>
          </div>
          <div className="overview-card">
            <div className="card-icon">
              <FontAwesomeIcon icon={faChartBar} />
            </div>
            <div className="card-content">
              <h3>{formatNumber(overview.recent_stats?.total_views || 0)}</h3>
              <p>Views (Last 7 Days)</p>
            </div>
          </div>
          <div className="overview-card">
            <div className="card-icon">
              <FontAwesomeIcon icon={faBullseye} />
            </div>
            <div className="card-content">
              <h3>{formatNumber(overview.recent_stats?.total_clicks || 0)}</h3>
              <p>Clicks (Last 7 Days)</p>
            </div>
          </div>
          <div className="overview-card">
            <div className="card-icon">
              <FontAwesomeIcon icon={faFileAlt} />
            </div>
            <div className="card-content">
              <h3>{formatNumber(overview.recent_stats?.total_applications || 0)}</h3>
              <p>Applications (Last 7 Days)</p>
            </div>
          </div>
        </div>
      )}

      {companiesWithStats.length === 0 ? (
        <div className="no-companies-message">
          <h3>No Companies with Analytics Access</h3>
          <p>You don't have analytics access to any companies yet. Contact your administrator to get access.</p>
        </div>
      ) : (
        <div className="analytics-content">
          {/* Company Selection */}
          <div className="company-selection">
            <h2>Select Company</h2>
            <div className="company-grid">
              {companiesWithStats.map((company) => (
                <div
                  key={company.id}
                  className={`company-card ${selectedCompany?.id === company.id ? 'selected' : ''}`}
                >
                  <div className="company-info">
                    <h3>{company.name}</h3>
                    <p>{company.access_info.permissions_summary}</p>
                  </div>
                  <div className="access-level">
                    <span className={`access-badge ${company.access_info.access_level}`}>
                      {company.access_info.access_level}
                    </span>
                    <button 
                      type="button"
                      className="view-analytics-btn"
                      onClick={(e) => {
                        e.preventDefault();
                        e.stopPropagation();
                        console.log('🔍 VIEW button clicked for company:', company.name);
                        console.log('📊 Company data:', company);
                        console.log('✅ Setting selected company...');
                        setSelectedCompany(company);
                        console.log('🎯 Selected company set!');
                      }}
                    >
                      VIEW
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Statistics Section */}
          {selectedCompany && (
            <div className="statistics-section">
              <div className="statistics-header">
                <h2>Analytics for {selectedCompany.name}</h2>
                <div className="controls">
                  <select 
                    value={dateRange} 
                    onChange={(e) => setDateRange(parseInt(e.target.value))}
                    className="date-range-select"
                  >
                    <option value={7}>Last 7 days</option>
                    <option value={30}>Last 30 days</option>
                    <option value={90}>Last 90 days</option>
                  </select>
                  {selectedCompany.access_info.can_export_data && (
                    <button 
                      onClick={() => handleExportData(selectedCompany.id)}
                      className="export-btn"
                    >
                      <FontAwesomeIcon icon={faFileExport} /> Export Data
                    </button>
                  )}
                </div>
              </div>

              {statsLoading ? (
                <div className="stats-loading">
                  <div className="spinner"></div>
                  <p>Loading statistics...</p>
                </div>
              ) : statistics ? (
                <div className="statistics-content">
                  {/* Summary Cards */}
                  <div className="stats-summary">
                    <div className="stat-card">
                      <h4>Total Page Views</h4>
                      <p className="stat-number">{formatNumber(statistics.totals.total_page_views)}</p>
                    </div>
                    <div className="stat-card">
                      <h4>Unique Visitors</h4>
                      <p className="stat-number">{formatNumber(statistics.totals.total_unique_visitors)}</p>
                    </div>
                    <div className="stat-card">
                      <h4>Job Page Clicks</h4>
                      <p className="stat-number">{formatNumber(statistics.totals.total_job_page_clicks)}</p>
                    </div>
                    <div className="stat-card">
                      <h4>Profile Views</h4>
                      <p className="stat-number">{formatNumber(statistics.totals.total_profile_views)}</p>
                    </div>
                    <div className="stat-card">
                      <h4>Application Clicks</h4>
                      <p className="stat-number">{formatNumber(statistics.totals.total_application_clicks)}</p>
                    </div>
                    <div className="stat-card">
                      <h4>Contact Clicks</h4>
                      <p className="stat-number">{formatNumber(statistics.totals.total_contact_clicks)}</p>
                    </div>
                    <div className="stat-card">
                      <h4>Avg Click-Through Rate</h4>
                      <p className="stat-number">{formatPercentage(statistics.totals.avg_click_through_rate)}</p>
                    </div>
                    <div className="stat-card">
                      <h4>Avg Engagement Rate</h4>
                      <p className="stat-number">{formatPercentage(statistics.totals.avg_engagement_rate)}</p>
                    </div>
                  </div>

                  {/* Daily Stats Table */}
                  {statistics.daily_stats && statistics.daily_stats.length > 0 && (
                    <div className="daily-stats">
                      <h3>Daily Breakdown</h3>
                      <div className="table-container">
                        <table className="stats-table">
                          <thead>
                            <tr>
                              <th>Date</th>
                              <th>Page Views</th>
                              <th>Unique Visitors</th>
                              <th>Job Clicks</th>
                              <th>Profile Views</th>
                              <th>Applications</th>
                              <th>CTR</th>
                              <th>Engagement</th>
                            </tr>
                          </thead>
                          <tbody>
                            {statistics.daily_stats.map((stat, index) => (
                              <tr key={index}>
                                <td>{new Date(stat.date).toLocaleDateString()}</td>
                                <td>{formatNumber(stat.page_views)}</td>
                                <td>{formatNumber(stat.unique_visitors)}</td>
                                <td>{formatNumber(stat.job_page_clicks)}</td>
                                <td>{formatNumber(stat.profile_views)}</td>
                                <td>{formatNumber(stat.application_clicks)}</td>
                                <td>{formatPercentage(stat.click_through_rate)}</td>
                                <td>{formatPercentage(stat.engagement_rate)}</td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="no-stats-message">
                  <p>No statistics available for the selected period.</p>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default CompanyAnalyticsDashboard;