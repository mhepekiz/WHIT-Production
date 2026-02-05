import { useState, useEffect } from 'react';

const useHomepageSections = () => {
  const [sections, setSections] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSections = async () => {
      try {
        const response = await fetch(
          `${import.meta.env.VITE_API_URL || 'http://localhost:8001/api'}/homepage-sections/`
        );

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        setSections(data);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch homepage sections:', err);
        setError('Failed to load homepage sections');
      } finally {
        setLoading(false);
      }
    };

    fetchSections();
  }, []);

  return { sections, loading, error };
};

export default useHomepageSections;