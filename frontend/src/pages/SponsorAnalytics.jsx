import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { getAccessibleCompanies, getSponsorStats } from '../services/recruiterApi';
import './SponsorAnalytics.css';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const SponsorAnalytics = () => {
  const [accessibleCompanies, setAccessibleCompanies] = useState([]);
  const [selectedCompany, setSelectedCompany] = useState('');
  const [sponsorStats, setSponsorStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [dateRange, setDateRange] = useState({
    startDate: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0], // 30 days ago
    endDate: new Date().toISOString().split('T')[0] // today
  });

  useEffect(() => {
    fetchAccessibleCompanies();
  }, []);

  const fetchAccessibleCompanies = async () => {
    try {
      setLoading(true);
      const companies = await getAccessibleCompanies();
      setAccessibleCompanies(companies);
      if (companies.length > 0) {
        setSelectedCompany(companies[0].id);
      }
      setError('');
    } catch (err) {
      setError('Failed to fetch accessible companies: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchSponsorStats = async () => {
    if (!selectedCompany) return;
    
    try {
      setLoading(true);
      const stats = await getSponsorStats(
        selectedCompany, 
        dateRange.startDate, 
        dateRange.endDate
      );
      setSponsorStats(stats);
      setError('');
    } catch (err) {
      setError('Failed to fetch sponsor statistics: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (selectedCompany) {
      fetchSponsorStats();
    }
  }, [selectedCompany, dateRange]);

  const handleDateRangeChange = (field, value) => {
    setDateRange(prev => ({
      ...prev,
      [field]: value
    }));
  };

  // Prepare chart data from API response
  const chartData = sponsorStats ? {
    labels: Object.keys(sponsorStats.daily_stats).sort(),
    datasets: [
      {
        label: 'Clicks',
        data: Object.keys(sponsorStats.daily_stats).sort().map(date => sponsorStats.daily_stats[date].clicks),
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        tension: 0.1,
        yAxisID: 'y',
      },
      {
        label: 'Impressions',
        data: Object.keys(sponsorStats.daily_stats).sort().map(date => sponsorStats.daily_stats[date].impressions),
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        tension: 0.1,
        yAxisID: 'y1',
      }
    ]
  } : { labels: [], datasets: [] };

  const chartOptions = {
    responsive: true,
    interaction: {
      mode: 'index',
      intersect: false,
    },
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Sponsor Performance Over Time',
      },
    },
    scales: {
      x: {
        display: true,
        title: {
          display: true,
          text: 'Date'
        }
      },
      y: {
        type: 'linear',
        display: true,
        position: 'left',
        title: {
          display: true,
          text: 'Clicks'
        },
      },
      y1: {
        type: 'linear',
        display: true,
        position: 'right',
        title: {
          display: true,
          text: 'Impressions'
        },
        grid: {
          drawOnChartArea: false,
        },
      },
    },
  };

  // Calculate totals from API response
  const totalClicks = sponsorStats?.summary?.total_clicks || 0;
  const totalImpressions = sponsorStats?.summary?.total_impressions || 0;
  const averageCTR = sponsorStats?.summary?.overall_ctr || 0;

  const selectedCompanyName = sponsorStats?.company_name || accessibleCompanies.find(c => c.id == selectedCompany)?.name || '';

  return (
    <div className="sponsor-analytics">
      <div className="analytics-header">
        <h2>Sponsor Analytics</h2>
        <p>View performance metrics for your accessible companies</p>
      </div>

      {error && (
        <div className="alert alert-danger">{error}</div>
      )}

      {/* Company and Date Selection */}
      <div className="controls-section">
        <div className="control-group">
          <div className="card">
            <div className="card-header">
              <h5>Select Company</h5>
            </div>
            <div className="card-body">
              <div className="form-group">
                <label className="form-label">Accessible Companies</label>
                <select 
                  className="form-select"
                  value={selectedCompany} 
                  onChange={(e) => setSelectedCompany(e.target.value)}
                  disabled={loading}
                >
                  <option value="">Choose a company...</option>
                  {accessibleCompanies.map(company => (
                    <option key={company.id} value={company.id}>
                      {company.name} 
                      {company.access_level === 'manage' && ' (Manager)'}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>
        </div>

        <div className="control-group">
          <div className="card">
            <div className="card-header">
              <h5>Date Range</h5>
            </div>
            <div className="card-body">
              <div className="date-controls">
                <div className="form-group">
                  <label className="form-label">Start Date</label>
                  <input
                    type="date"
                    className="form-control"
                    value={dateRange.startDate}
                    onChange={(e) => handleDateRangeChange('startDate', e.target.value)}
                    disabled={loading}
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">End Date</label>
                  <input
                    type="date"
                    className="form-control"
                    value={dateRange.endDate}
                    onChange={(e) => handleDateRangeChange('endDate', e.target.value)}
                    disabled={loading}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {loading && (
        <div className="loading-section">
          <div className="spinner"></div>
          <p>Loading sponsor analytics...</p>
        </div>
      )}

      {selectedCompany && sponsorStats && Object.keys(sponsorStats.daily_stats || {}).length > 0 && (
        <>
          {/* Summary Cards */}
          <div className="summary-section">
            <div className="summary-card clicks">
              <div className="summary-icon">👆</div>
              <div className="summary-number">{totalClicks.toLocaleString()}</div>
              <div className="summary-label">Total Clicks</div>
            </div>
            <div className="summary-card impressions">
              <div className="summary-icon">👁️</div>
              <div className="summary-number">{totalImpressions.toLocaleString()}</div>
              <div className="summary-label">Total Impressions</div>
            </div>
            <div className="summary-card ctr">
              <div className="summary-icon">📊</div>
              <div className="summary-number">{averageCTR}%</div>
              <div className="summary-label">Average CTR</div>
            </div>
          </div>

          {/* Chart */}
          <div className="chart-section">
            <div className="card">
              <div className="card-header">
                <h5>Performance Chart - {selectedCompanyName}</h5>
                <small className="text-muted">
                  {new Date(dateRange.startDate).toLocaleDateString()} - {new Date(dateRange.endDate).toLocaleDateString()}
                </small>
              </div>
              <div className="card-body">
                <Line data={chartData} options={chartOptions} />
              </div>
            </div>
          </div>

          {/* Detailed Stats Table */}
          <div className="table-section">
            <div className="card">
              <div className="card-header">
                <h5>Daily Statistics</h5>
              </div>
              <div className="card-body">
                <div className="table-responsive">
                  <table className="stats-table">
                    <thead>
                      <tr>
                        <th>Date</th>
                        <th>Campaign</th>
                        <th>Clicks</th>
                        <th>Impressions</th>
                        <th>CTR (%)</th>
                      </tr>
                    </thead>
                    <tbody>
                      {sponsorStats && Object.keys(sponsorStats.daily_stats).sort().map((date, index) => {
                        const stat = sponsorStats.daily_stats[date];
                        return (
                          <tr key={index}>
                            <td>{new Date(date).toLocaleDateString()}</td>
                            <td>
                              {Object.keys(sponsorStats.campaign_stats).map((campaignName, idx) => (
                                <span key={idx} className="campaign-badge" style={{ marginRight: '5px' }}>
                                  {campaignName}
                                </span>
                              ))}
                            </td>
                            <td>{stat.clicks.toLocaleString()}</td>
                            <td>{stat.impressions.toLocaleString()}</td>
                            <td>
                              <span className={`ctr-badge ${stat.ctr >= 2 ? 'good' : stat.ctr >= 1 ? 'average' : 'low'}`}>
                                {stat.ctr.toFixed(2)}%
                              </span>
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </>
      )}

      {selectedCompany && (!sponsorStats || Object.keys(sponsorStats.daily_stats || {}).length === 0) && !loading && (
        <div className="alert alert-info">
          No sponsor statistics found for the selected company and date range.
          Try selecting a different date range or contact support if you believe this is an error.
        </div>
      )}

      {accessibleCompanies.length === 0 && !loading && (
        <div className="alert alert-warning">
          You don't have access to any company sponsor statistics. 
          Contact your administrator to request access to specific companies.
        </div>
      )}
    </div>
  );
};

export default SponsorAnalytics;