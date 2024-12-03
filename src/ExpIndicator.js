import React from 'react';
import './ExpIndicator.css';

function ExpIndicator({ count, imageSrc, onClick }) {
    return (
        <button className="exp-indicator" onClick={() => onClick(subject)}>
            <img src={imageSrc} alt={`${subject}`} className="exp-image" />
            <span className="exp-label">{subject}</span>
        </button>
    );
}

export default ExpIndicator;
