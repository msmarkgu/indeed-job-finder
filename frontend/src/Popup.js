import React from 'react';
import './Popup.css';

const Popup = ({ title, message, handleClose }) => {
  return (
    <div className="popup">
      <div className="popup-inner">
        <h2>{title}</h2>
        <p>{message}</p>
        <button onClick={handleClose}>Dismiss</button>
      </div>
    </div>
  );
};

export default Popup;
