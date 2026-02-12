import { useState, useEffect } from 'react';

const useHomepageSections = () => {
  const [sections, setSections] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSections = async () => {
      try {
        // Use environment variable for API URL
        const apiUrl = import.meta.env.VITE_API_URL || '/api';
        const response = await fetch(`${apiUrl}/homepage-sections/`);

        if (!response.ok) {
          // If the endpoint doesn't exist or fails, just return empty sections
          console.warn('Homepage sections API not available:', response.status);
          setSections({ how_it_works_sections: [], recruiter_sections: [] });
          setError(null);
          return;
        }

        const data = await response.json();
        setSections(data);
        setError(null);
      } catch (err) {
        console.warn('Failed to fetch homepage sections:', err);
        // Don't show error to user, just use empty sections
        setSections({ how_it_works_sections: [], recruiter_sections: [] });
        setError(null);
      } finally {
        setLoading(false);
      }
    };

    fetchSections();
  }, []);

  return { sections, loading, error };
};

export default useHomepageSections;