import React, { useState } from 'react';
import './Modal.css'; // Include the above CSS

function Modal({ isOpen, onClose, children }) {
    if (!isOpen) return null; // Don't render anything if modal is closed

    return (
        <div
            className="modal-overlay"
            onClick={onClose} // Close modal when clicking on the overlay
        >
            <div
                className="modal-content"
                onClick={(e) => e.stopPropagation()} // Prevent closing when clicking inside the modal
            >
                {children}
            </div>
        </div>
    );
}

export default Modal;
