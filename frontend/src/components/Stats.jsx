import './Stats.css';

function Stats({ stats }) {
  return (
    <div className="stats-container">
      <div className="stat-card">
        <div className="stat-value">{stats.total_companies}</div>
        <div className="stat-label">Total Companies</div>
      </div>

      <div className="stat-card">
        <div className="stat-value">{stats.active_companies}</div>
        <div className="stat-label">Active Companies</div>
      </div>

      <div className="stat-card">
        <div className="stat-value">{stats.engineering_positions}</div>
        <div className="stat-label">Engineering Positions</div>
      </div>

      <div className="stat-card">
        <div className="stat-value">{stats.countries_count}</div>
        <div className="stat-label">Countries</div>
      </div>
    </div>
  );
}

export default Stats;
