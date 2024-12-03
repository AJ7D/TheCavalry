import React from 'react';
import './CustomButton.css';

function CustomButton({ subject, imageSrc, onClick }) {
    return (
        <button className="custom-button" onClick={() => onClick(subject)}>
            <img src={imageSrc} alt={`${subject}`} className="button-image" />
            <span className="button-label">{subject}</span>
        </button>
    );
}

export default CustomButton;
