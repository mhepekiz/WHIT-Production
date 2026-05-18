import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import DOMPurify from 'dompurify';
import { staticPageService } from '../services/api';
import './StaticPage.css';

function StaticPage() {
  const { slug } = useParams();
  const [page, setPage] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let isMounted = true;

    const fetchPage = async () => {
      try {
        setLoading(true);
        setError('');
        const data = await staticPageService.getPage(slug);
        if (isMounted) {
          setPage(data);
          document.title = data.meta_title || `${data.title} | WhoIsHiringInTech`;
        }
      } catch (err) {
        if (isMounted) {
          setError('Page not found.');
          setPage(null);
        }
      } finally {
        if (isMounted) setLoading(false);
      }
    };

    fetchPage();

    return () => {
      isMounted = false;
    };
  }, [slug]);

  if (loading) {
    return (
      <div className="static-page-shell">
        <div className="static-page-card">Loading...</div>
      </div>
    );
  }

  if (error || !page) {
    return (
      <div className="static-page-shell">
        <div className="static-page-card static-page-empty">
          <h1>Page not found</h1>
          <p>The page you are looking for is not available.</p>
          <Link to="/" className="static-page-home-link">Go Home</Link>
        </div>
      </div>
    );
  }

  const safeContent = DOMPurify.sanitize(page.content || '');

  return (
    <div className="static-page-shell">
      <article className="static-page-card">
        <header className="static-page-header">
          <h1>{page.title}</h1>
          {page.excerpt && <p>{page.excerpt}</p>}
        </header>
        <div
          className="static-page-content"
          dangerouslySetInnerHTML={{ __html: safeContent }}
        />
      </article>
    </div>
  );
}

export default StaticPage;
