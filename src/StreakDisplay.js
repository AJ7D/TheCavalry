import React from 'react';
import './StreakDisplay.css'; // Ensure the CSS file is imported

function StreakDisplay({ streakNum }) {
    return (
        <div className="streak-display">
            <span>{streakNum} WEEK STREAK</span>
            <img src="http://127.0.0.1:5000/static/images/flame.png" alt="Flame Icon" />
        </div>
    );
}

export default StreakDisplay;
