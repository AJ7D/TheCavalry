import React, { useState } from 'react';
import './CustomCheckbox.css'; // Import the CSS file

function CustomCheckbox() {
  const [isChecked, setIsChecked] = useState(false);

  const handleChange = (e) => {
    setIsChecked(e.target.checked);
  };

  return (
    <div className="custom-checkbox-container">
      <input
        type="checkbox"
        id="customCheckbox"
        className="custom-checkbox"
        checked={isChecked}
        onChange={handleChange}
      />
      <label htmlFor="customCheckbox">Agree to Terms</label>
    </div>
  );
}

export default CustomCheckbox;
