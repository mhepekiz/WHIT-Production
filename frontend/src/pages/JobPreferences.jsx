import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './JobPreferences.css';

const JobPreferences = () => {
  const navigate = useNavigate();
  const { token } = useAuth();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  // Form state
  const [selectedFunctions, setSelectedFunctions] = useState([]);
  const [selectedCountries, setSelectedCountries] = useState([]);
  const [selectedStates, setSelectedStates] = useState([]);
  const [selectedCities, setSelectedCities] = useState([]);
  const [selectedWorkEnvironments, setSelectedWorkEnvironments] = useState([]);
  const [activelyLooking, setActivelyLooking] = useState(false);

  // Autocomplete inputs
  const [countryInput, setCountryInput] = useState('');
  const [stateInput, setStateInput] = useState('');
  const [cityInput, setCityInput] = useState('');
  
  // Show/hide autocomplete suggestions
  const [showCountrySuggestions, setShowCountrySuggestions] = useState(false);
  const [showStateSuggestions, setShowStateSuggestions] = useState(false);

  // Available options from backend
  const [availableFunctions, setAvailableFunctions] = useState([]);
  const [availableWorkEnvironments, setAvailableWorkEnvironments] = useState([]);

  // Available options
  const countries = [
    'United States', 'Canada', 'United Kingdom', 'Germany', 'France', 
    'Netherlands', 'Sweden', 'Australia', 'Singapore', 'Japan', 'Ireland',
    'Switzerland', 'Denmark', 'Norway', 'Finland', 'Belgium', 'Austria',
    'Spain', 'Italy', 'Portugal', 'New Zealand', 'South Korea', 'Israel',
    'United Arab Emirates', 'India', 'Mexico', 'Brazil', 'Argentina'
  ];

  const usStates = [
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
    'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho',
    'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
    'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
    'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
    'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
    'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon',
    'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
    'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
    'West Virginia', 'Wisconsin', 'Wyoming'
  ];

  const filteredCountries = countries.filter(country =>
    country.toLowerCase().includes(countryInput.toLowerCase()) &&
    !selectedCountries.includes(country)
  );

  const filteredStates = usStates.filter(state =>
    state.toLowerCase().includes(stateInput.toLowerCase()) &&
    !selectedStates.includes(state)
  );

  useEffect(() => {
    if (!token) {
      navigate('/login');
      return;
    }
    fetchData();
  }, [token, navigate]);

  const fetchData = async () => {
    try {
      const [prefsRes, filtersRes] = await Promise.all([
        fetch('/api/accounts/job-preferences/me/', {
          headers: { 'Authorization': `Token ${token}` },
        }),
        fetch('/api/companies/filters/')
      ]);

      if (prefsRes.ok) {
        const data = await prefsRes.json();
        
        // Set job functions
        if (data.desired_functions) {
          setSelectedFunctions(data.desired_functions.map(f => f.id));
        }
        
        // Set work environments - now returns as array of names
        if (data.work_environments) {
          setSelectedWorkEnvironments(Array.isArray(data.work_environments) 
            ? data.work_environments 
            : []);
        }
        
        // Parse the preferred_locations field
        if (data.preferred_locations) {
          const locations = parseLocations(data.preferred_locations);
          setSelectedCountries(locations.countries);
          setSelectedStates(locations.states);
          setSelectedCities(locations.cities);
        }
        setActivelyLooking(data.actively_looking || false);
      }

      if (filtersRes.ok) {
        const filtersData = await filtersRes.json();
        setAvailableFunctions(filtersData.functions || []);
        // Work environments are simple strings
        const workEnvs = (filtersData.work_environments || [])
          .filter(env => env !== 'Undefined')
          .map(env => ({ id: env, name: env }));
        setAvailableWorkEnvironments(workEnvs);
      }
    } catch (error) {
      console.error('Error fetching preferences:', error);
    } finally {
      setLoading(false);
    }
  };

  const parseLocations = (locationsString) => {
    const locations = { countries: [], states: [], cities: [] };
    if (!locationsString) return locations;

    const parts = locationsString.split(';');
    parts.forEach(part => {
      const [type, value] = part.split(':');
      if (type === 'country' && value) {
        locations.countries.push(value);
      } else if (type === 'state' && value) {
        locations.states.push(value);
      } else if (type === 'city' && value) {
        locations.cities.push(value);
      }
    });

    return locations;
  };

  const serializeLocations = () => {
    const parts = [];
    selectedCountries.forEach(c => parts.push(`country:${c}`));
    selectedStates.forEach(s => parts.push(`state:${s}`));
    selectedCities.forEach(c => parts.push(`city:${c}`));
    return parts.join(';');
  };

  const handleAddCountry = (country) => {
    if (country && !selectedCountries.includes(country)) {
      setSelectedCountries([...selectedCountries, country]);
      setCountryInput('');
      setShowCountrySuggestions(false);
    }
  };

  const handleAddState = (state) => {
    if (state && !selectedStates.includes(state)) {
      setSelectedStates([...selectedStates, state]);
      setStateInput('');
      setShowStateSuggestions(false);
    }
  };

  const handleToggleFunction = (functionId) => {
    if (selectedFunctions.includes(functionId)) {
      setSelectedFunctions(selectedFunctions.filter(id => id !== functionId));
    } else {
      setSelectedFunctions([...selectedFunctions, functionId]);
    }
  };

  const handleToggleWorkEnvironment = (envName) => {
    if (selectedWorkEnvironments.includes(envName)) {
      setSelectedWorkEnvironments(selectedWorkEnvironments.filter(name => name !== envName));
    } else {
      setSelectedWorkEnvironments([...selectedWorkEnvironments, envName]);
    }
  };

  const handleAddCity = () => {
    if (cityInput.trim() && !selectedCities.includes(cityInput.trim())) {
      setSelectedCities([...selectedCities, cityInput.trim()]);
      setCityInput('');
    }
  };

  const handleRemoveCountry = (country) => {
    setSelectedCountries(selectedCountries.filter(c => c !== country));
  };

  const handleRemoveState = (state) => {
    setSelectedStates(selectedStates.filter(s => s !== state));
  };

  const handleRemoveCity = (city) => {
    setSelectedCities(selectedCities.filter(c => c !== city));
  };

  const handleSave = async () => {
    setSaving(true);
    setMessage('');

    try {
      const locationString = serializeLocations();
      
      const response = await fetch('/api/accounts/job-preferences/me/', {
        method: 'PATCH',
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          desired_function_ids: selectedFunctions,
          work_environment_names: selectedWorkEnvironments,
          preferred_locations: locationString,
          actively_looking: activelyLooking,
        }),
      });

      if (response.ok) {
        setMessage('Preferences saved successfully!');
        setTimeout(() => setMessage(''), 3000);
      } else {
        setMessage('Failed to save preferences. Please try again.');
      }
    } catch (error) {
      console.error('Error saving preferences:', error);
      setMessage('Network error. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading preferences...</div>;
  }

  return (
    <div className="job-preferences-page">
      <div className="preferences-container">
        <button onClick={() => navigate('/dashboard')} className="back-button">
          ← Back to Dashboard
        </button>

        <h1>Job Preferences</h1>
        <p className="subtitle">Set your preferred job functions, work environment, and locations</p>

        {/* Job Functions Section */}
        <div className="preference-section">
          <label className="section-label">Job Functions</label>
          <p className="section-description">Select the roles you're interested in</p>
          <div className="checkbox-grid">
            {availableFunctions.map(func => (
              <label key={func.id} className="checkbox-item">
                <input
                  type="checkbox"
                  checked={selectedFunctions.includes(func.id)}
                  onChange={() => handleToggleFunction(func.id)}
                  className="checkbox-input"
                />
                <span 
                  className="checkbox-label-text"
                  style={{ 
                    backgroundColor: selectedFunctions.includes(func.id) ? func.color : 'transparent',
                    color: selectedFunctions.includes(func.id) ? func.text_color : '#2c3e50',
                    border: selectedFunctions.includes(func.id) ? 'none' : '1px solid #ddd'
                  }}
                >
                  {func.name}
                </span>
              </label>
            ))}
          </div>
        </div>

        {/* Work Environment Section */}
        <div className="preference-section">
          <label className="section-label">Work Environment</label>
          <p className="section-description">Choose your preferred work settings</p>
          <div className="checkbox-grid">
            {availableWorkEnvironments.map(env => (
              <label key={env.name} className="checkbox-item">
                <input
                  type="checkbox"
                  checked={selectedWorkEnvironments.includes(env.name)}
                  onChange={() => handleToggleWorkEnvironment(env.name)}
                  className="checkbox-input"
                />
                <span 
                  className="checkbox-label-text"
                  style={{ 
                    backgroundColor: selectedWorkEnvironments.includes(env.name) ? '#e8e9ff' : 'transparent',
                    color: selectedWorkEnvironments.includes(env.name) ? '#4f46e5' : '#2c3e50',
                    border: selectedWorkEnvironments.includes(env.name) ? 'none' : '1px solid #ddd'
                  }}
                >
                  {env.name}
                </span>
              </label>
            ))}
          </div>
        </div>

        <h2 className="section-title">Preferred Locations</h2>
        <p className="subtitle">Add countries, states, and cities you're interested in</p>

        {/* Countries Section */}
        <div className="preference-section">
          <label className="section-label">Countries</label>
          <div className="autocomplete-container">
            <input
              type="text"
              value={countryInput}
              onChange={(e) => {
                setCountryInput(e.target.value);
                setShowCountrySuggestions(true);
              }}
              onFocus={() => setShowCountrySuggestions(true)}
              placeholder="Type to search countries..."
              className="location-input"
            />
            {showCountrySuggestions && countryInput && filteredCountries.length > 0 && (
              <div className="autocomplete-dropdown">
                {filteredCountries.slice(0, 8).map(country => (
                  <div
                    key={country}
                    className="autocomplete-item"
                    onClick={() => handleAddCountry(country)}
                  >
                    {country}
                  </div>
                ))}
              </div>
            )}
          </div>
          
          {selectedCountries.length > 0 && (
            <div className="tags-container">
              {selectedCountries.map(country => (
                <span key={country} className="tag">
                  {country}
                  <button onClick={() => handleRemoveCountry(country)} className="tag-remove">
                    ×
                  </button>
                </span>
              ))}
            </div>
          )}
        </div>

        {/* States Section */}
        <div className="preference-section">
          <label className="section-label">States (US only)</label>
          <div className="autocomplete-container">
            <input
              type="text"
              value={stateInput}
              onChange={(e) => {
                setStateInput(e.target.value);
                setShowStateSuggestions(true);
              }}
              onFocus={() => setShowStateSuggestions(true)}
              placeholder="Type to search US states..."
              className="location-input"
            />
            {showStateSuggestions && stateInput && filteredStates.length > 0 && (
              <div className="autocomplete-dropdown">
                {filteredStates.slice(0, 8).map(state => (
                  <div
                    key={state}
                    className="autocomplete-item"
                    onClick={() => handleAddState(state)}
                  >
                    {state}
                  </div>
                ))}
              </div>
            )}
          </div>
          
          {selectedStates.length > 0 && (
            <div className="tags-container">
              {selectedStates.map(state => (
                <span key={state} className="tag">
                  {state}
                  <button onClick={() => handleRemoveState(state)} className="tag-remove">
                    ×
                  </button>
                </span>
              ))}
            </div>
          )}
        </div>

        {/* Cities Section */}
        <div className="preference-section">
          <label className="section-label">Cities</label>
          <div className="input-group">
            <input
              type="text"
              value={cityInput}
              onChange={(e) => setCityInput(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                  handleAddCity();
                }
              }}
              placeholder="Add a city (e.g., New York, London)"
              className="location-input"
            />
            <button 
              onClick={handleAddCity}
              disabled={!cityInput.trim()}
              className="add-button"
            >
              Add
            </button>
          </div>
          
          {selectedCities.length > 0 && (
            <div className="tags-container">
              {selectedCities.map(city => (
                <span key={city} className="tag">
                  {city}
                  <button onClick={() => handleRemoveCity(city)} className="tag-remove">
                    ×
                  </button>
                </span>
              ))}
            </div>
          )}
        </div>

        {/* Actively Looking Checkbox */}
        <div className="checkbox-section">
          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={activelyLooking}
              onChange={(e) => setActivelyLooking(e.target.checked)}
              className="checkbox-input"
            />
            <span>I am actively looking for job opportunities</span>
          </label>
        </div>

        {/* Save Button */}
        <div className="actions">
          {message && (
            <div className={`message ${message.includes('success') ? 'success' : 'error'}`}>
              {message}
            </div>
          )}
          <button 
            onClick={handleSave}
            disabled={saving}
            className="save-button"
          >
            {saving ? 'Saving...' : 'Save Preferences'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default JobPreferences;
