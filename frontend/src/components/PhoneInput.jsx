import React, { useState } from 'react';

const PhoneInput = ({ value, onChange, error }) => {
  const [focused, setFocused] = useState(false);

  const formatPhoneNumber = (input) => {
    // Remove all non-numeric characters except +
    const cleaned = input.replace(/[^\d+]/g, '');
    
    // Don't format if empty
    if (!cleaned) return '';
    
    // Ensure it starts with +
    let formatted = cleaned.startsWith('+') ? cleaned : '+' + cleaned;
    
    // Extract just the digits after +
    const digitsOnly = formatted.substring(1);
    
    // Determine country code length (1-3 digits)
    let countryCode = '';
    let remaining = '';
    
    // Try to intelligently detect country code
    if (digitsOnly.length >= 1) {
      if (digitsOnly[0] === '1') {
        // North American country code
        countryCode = digitsOnly.substring(0, 1);
        remaining = digitsOnly.substring(1);
      } else if (digitsOnly.length >= 2 && parseInt(digitsOnly.substring(0, 2)) <= 99) {
        // 2-digit country code
        countryCode = digitsOnly.substring(0, 2);
        remaining = digitsOnly.substring(2);
      } else if (digitsOnly.length >= 3) {
        // 3-digit country code
        countryCode = digitsOnly.substring(0, 3);
        remaining = digitsOnly.substring(3);
      } else {
        countryCode = digitsOnly;
        remaining = '';
      }
    }
    
    // Format remaining digits: (XXX) XXX-XXXX
    if (remaining.length === 0) {
      formatted = `+${countryCode}`;
    } else if (remaining.length <= 3) {
      formatted = `+${countryCode} (${remaining}`;
    } else if (remaining.length <= 6) {
      const area = remaining.substring(0, 3);
      const first = remaining.substring(3);
      formatted = `+${countryCode} (${area}) ${first}`;
    } else {
      const area = remaining.substring(0, 3);
      const first = remaining.substring(3, 6);
      const second = remaining.substring(6, 10);
      formatted = `+${countryCode} (${area}) ${first}-${second}`;
    }
    
    return formatted;
  };

  const handleChange = (e) => {
    const input = e.target.value;
    const formatted = formatPhoneNumber(input);
    onChange(formatted);
  };

  const handleBlur = () => {
    setFocused(false);
    // Validate on blur
    if (value && !isValidPhone(value)) {
      // Keep the value but show error
    }
  };

  const isValidPhone = (phone) => {
    if (!phone) return true; // Empty is valid (optional field)
    // Check format: +X (XXX) XXX-XXXX or similar
    const phoneRegex = /^\+\d{1,3}\s\(\d{3}\)\s\d{3}-\d{4}$/;
    return phoneRegex.test(phone);
  };

  return (
    <div className="phone-input-container">
      <input
        type="tel"
        value={value}
        onChange={handleChange}
        onFocus={() => setFocused(true)}
        onBlur={handleBlur}
        placeholder="+1 (555) 123-4567"
        className={error ? 'error' : ''}
      />
      {error && <span className="error-text">{error}</span>}
      {!error && !focused && value && !isValidPhone(value) && (
        <span className="error-text">
          Format: +country code (area) xxx-xxxx (e.g., +1 (555) 123-4567)
        </span>
      )}
    </div>
  );
};

export default PhoneInput;
