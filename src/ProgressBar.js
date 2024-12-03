import React from 'react';
import './ProgressBar.css'; // Import CSS for styling

function ProgressBar({ currentValue, goalValue }) {
    // Calculate the percentage of completion
    const percentage = (currentValue / goalValue) * 100;

    return (
        <div className="progress-container">
            {/* Display current and goal value */}
            <div className="progress-text">{currentValue} / {goalValue}</div>
            
            {/* The progress bar */}
            <div className="progress-bar-background">
                <div
                    className="progress-bar"
                    style={{ width: `${percentage}%` }} // Dynamically set the width based on the percentage
                ></div>
            </div>
        </div>
    );
}

export default ProgressBar;
