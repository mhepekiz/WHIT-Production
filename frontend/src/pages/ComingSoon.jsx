import { Link } from 'react-router-dom';
import './ComingSoon.css';

function ComingSoon({ title = 'Recruiter Features Coming Soon', message }) {
  return (
    <div className="coming-soon-page">
      <section className="coming-soon-panel" role="status" aria-live="polite">
        <div className="coming-soon-icon" aria-hidden="true">💼</div>
        <h1>{title}</h1>
        <p>{message || 'Jobs and recruiter-connected features are being prepared. Please check back soon.'}</p>
        <Link to="/" className="coming-soon-home-link">Back to Homepage</Link>
      </section>
    </div>
  );
}

export default ComingSoon;
