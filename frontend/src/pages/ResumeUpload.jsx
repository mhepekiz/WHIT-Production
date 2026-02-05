import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './ResumeUpload.css';

const ResumeUpload = () => {
  const navigate = useNavigate();
  const { token } = useAuth();
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');
  const [currentResume, setCurrentResume] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);

  useEffect(() => {
    fetchCurrentResume();
  }, []);

  const fetchCurrentResume = async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/accounts/profile/me/`, {
        headers: {
          'Authorization': `Token ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setCurrentResume(data.resume);
      }
    } catch (error) {
      console.error('Error fetching resume:', error);
    } finally {
      setLoading(false);
    }
  };

  const validateFile = (file) => {
    // Validate file type
    const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    if (!allowedTypes.includes(file.type)) {
      setMessage('Please upload a PDF or Word document');
      return false;
    }

    // Validate file size (5MB max)
    if (file.size > 5 * 1024 * 1024) {
      setMessage('File size must be less than 5MB');
      return false;
    }

    return true;
  };

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file && validateFile(file)) {
      setSelectedFile(file);
      setMessage('');
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
    event.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (event) => {
    event.preventDefault();
    event.stopPropagation();
    setIsDragging(false);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    event.stopPropagation();
    setIsDragging(false);

    const file = event.dataTransfer.files[0];
    if (file && validateFile(file)) {
      setSelectedFile(file);
      setMessage('');
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setMessage('Please select a file first');
      return;
    }

    setUploading(true);
    setMessage('');

    const formData = new FormData();
    formData.append('resume', selectedFile);

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/accounts/profile/me/`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Token ${token}`,
        },
        body: formData,
      });

      if (response.ok) {
        setMessage('Resume uploaded successfully!');
        setSelectedFile(null);
        fetchCurrentResume();
        
        // Clear file input
        const fileInput = document.getElementById('resume-input');
        if (fileInput) fileInput.value = '';
      } else {
        const data = await response.json();
        setMessage(data.resume?.[0] || 'Failed to upload resume');
      }
    } catch (error) {
      console.error('Error uploading resume:', error);
      setMessage('Error uploading resume. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete your resume?')) {
      return;
    }

    setUploading(true);
    setMessage('');

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/accounts/profile/me/`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ resume: null }),
      });

      if (response.ok) {
        setMessage('Resume deleted successfully');
        setCurrentResume(null);
      } else {
        setMessage('Failed to delete resume');
      }
    } catch (error) {
      console.error('Error deleting resume:', error);
      setMessage('Error deleting resume. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  const getFileName = (url) => {
    if (!url) return '';
    return url.split('/').pop();
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="resume-upload-page">
      <div className="resume-container">
        <button onClick={() => navigate('/dashboard')} className="back-button">
          ← Back to Dashboard
        </button>

        <h1>Resume Management</h1>
        <p className="subtitle">Upload and manage your resume for job applications</p>

        {/* Current Resume Section */}
        {currentResume && (
          <div className="resume-section">
            <h2 className="section-label">Current Resume</h2>
            <div className="current-resume-card">
              <div className="resume-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                  <polyline points="14 2 14 8 20 8" />
                  <line x1="16" y1="13" x2="8" y2="13" />
                  <line x1="16" y1="17" x2="8" y2="17" />
                </svg>
              </div>
              <div className="resume-info">
                <h3>{getFileName(currentResume)}</h3>
                <p>Currently uploaded resume</p>
              </div>
              <div className="resume-actions">
                <a 
                  href={currentResume} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="view-button"
                >
                  View
                </a>
                <button 
                  onClick={handleDelete}
                  disabled={uploading}
                  className="delete-button"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Upload New Resume Section */}
        <div className="resume-section">
          <h2 className="section-label">
            {currentResume ? 'Upload New Resume' : 'Upload Resume'}
          </h2>
          
          <div 
            className={`upload-area ${isDragging ? 'dragging' : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            <div className="upload-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                <polyline points="17 8 12 3 7 8" />
                <line x1="12" y1="3" x2="12" y2="15" />
              </svg>
            </div>
            
            <div className="upload-text">
              <h3>{isDragging ? 'Drop file here' : 'Drag & drop your resume here'}</h3>
              <p>or</p>
            </div>

            <input
              id="resume-input"
              type="file"
              accept=".pdf,.doc,.docx"
              onChange={handleFileSelect}
              className="file-input"
            />
            
            <label htmlFor="resume-input" className="file-input-label">
              Browse Files
            </label>

            <p className="upload-hint">Supported formats: PDF, DOC, DOCX (Max 5MB)</p>

            {selectedFile && (
              <div className="selected-file">
                <div className="file-icon">📄</div>
                <div className="file-details">
                  <p className="file-name">{selectedFile.name}</p>
                  <p className="file-size">
                    {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
                <button
                  type="button"
                  onClick={() => {
                    setSelectedFile(null);
                    const fileInput = document.getElementById('resume-input');
                    if (fileInput) fileInput.value = '';
                  }}
                  className="remove-file-button"
                >
                  ×
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="actions">
          {message && (
            <div className={`message ${message.includes('success') ? 'success' : 'error'}`}>
              {message}
            </div>
          )}
          
          <button 
            onClick={handleUpload}
            disabled={!selectedFile || uploading}
            className="upload-button"
          >
            {uploading ? 'Uploading...' : 'Upload Resume'}
          </button>
        </div>

        {/* Tips Section */}
        <div className="tips-section">
          <h3>Resume Tips</h3>
          <ul>
            <li>Keep your resume updated with your latest experience and skills</li>
            <li>Use a clear, professional format that's easy to read</li>
            <li>Tailor your resume to highlight relevant experience for your target roles</li>
            <li>Include keywords from job descriptions you're interested in</li>
            <li>Proofread carefully for spelling and grammar errors</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ResumeUpload;
