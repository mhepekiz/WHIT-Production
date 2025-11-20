import React, { useState, useEffect } from 'react';
import './LocationInput.css';

const LocationInput = ({ value, onChange }) => {
  const [country, setCountry] = useState('');
  const [state, setState] = useState('');
  const [city, setCity] = useState('');
  const [countryInput, setCountryInput] = useState('');
  const [stateInput, setStateInput] = useState('');
  const [showCountrySuggestions, setShowCountrySuggestions] = useState(false);
  const [showStateSuggestions, setShowStateSuggestions] = useState(false);

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

  const filteredCountries = countries.filter(c =>
    c.toLowerCase().includes(countryInput.toLowerCase())
  );

  const filteredStates = usStates.filter(s =>
    s.toLowerCase().includes(stateInput.toLowerCase())
  );

  // Parse initial value
  useEffect(() => {
    if (value) {
      const parts = value.split(';').map(p => p.trim());
      parts.forEach(part => {
        const [type, val] = part.split(':').map(p => p.trim());
        if (type === 'country') setCountry(val);
        if (type === 'state') setState(val);
        if (type === 'city') setCity(val);
      });
    }
  }, [value]);

  // Update parent when location changes
  useEffect(() => {
    const parts = [];
    if (country) parts.push(`country:${country}`);
    if (state) parts.push(`state:${state}`);
    if (city) parts.push(`city:${city}`);
    const newValue = parts.join(';');
    // Only call onChange if the value actually changed
    if (newValue !== value) {
      onChange(newValue);
    }
  }, [country, state, city]);

  const handleCountrySelect = (selectedCountry) => {
    setCountry(selectedCountry);
    setCountryInput('');
    setShowCountrySuggestions(false);
    // Clear state if changing from US to non-US
    if (selectedCountry !== 'United States') {
      setState('');
    }
  };

  const handleStateSelect = (selectedState) => {
    setState(selectedState);
    setStateInput('');
    setShowStateSuggestions(false);
  };

  const isUS = country === 'United States';

  return (
    <div className="location-input-component">
      {/* Country */}
      <div className="location-field">
        <label>Country</label>
        <div className="autocomplete-container">
          <input
            type="text"
            value={country || countryInput}
            onChange={(e) => {
              if (!country) {
                setCountryInput(e.target.value);
                setShowCountrySuggestions(true);
              }
            }}
            onFocus={() => !country && setShowCountrySuggestions(true)}
            placeholder="Type to search countries..."
            className="location-input-field"
            disabled={!!country}
          />
          {country && (
            <button
              type="button"
              onClick={() => {
                setCountry('');
                setState('');
                setCountryInput('');
              }}
              className="clear-button"
            >
              ×
            </button>
          )}
          {showCountrySuggestions && !country && countryInput && filteredCountries.length > 0 && (
            <div className="autocomplete-dropdown">
              {filteredCountries.slice(0, 8).map(c => (
                <div
                  key={c}
                  className="autocomplete-item"
                  onClick={() => handleCountrySelect(c)}
                >
                  {c}
                </div>
              ))}
            </div>
          )}
        </div>
        {country && <span className="selected-tag">{country}</span>}
      </div>

      {/* State (Only for US) */}
      {isUS && (
        <div className="location-field">
          <label>State (US only)</label>
          <div className="autocomplete-container">
            <input
              type="text"
              value={state || stateInput}
              onChange={(e) => {
                if (!state) {
                  setStateInput(e.target.value);
                  setShowStateSuggestions(true);
                }
              }}
              onFocus={() => !state && setShowStateSuggestions(true)}
              placeholder="Type to search US states..."
              className="location-input-field"
              disabled={!!state}
            />
            {state && (
              <button
                type="button"
                onClick={() => {
                  setState('');
                  setStateInput('');
                }}
                className="clear-button"
              >
                ×
              </button>
            )}
            {showStateSuggestions && !state && stateInput && filteredStates.length > 0 && (
              <div className="autocomplete-dropdown">
                {filteredStates.slice(0, 8).map(s => (
                  <div
                    key={s}
                    className="autocomplete-item"
                    onClick={() => handleStateSelect(s)}
                  >
                    {s}
                  </div>
                ))}
              </div>
            )}
          </div>
          {state && <span className="selected-tag">{state}</span>}
        </div>
      )}

      {/* City */}
      <div className="location-field">
        <label>City</label>
        <input
          type="text"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          placeholder="Enter city name"
          className="location-input-field"
        />
      </div>
    </div>
  );
};

export default LocationInput;
