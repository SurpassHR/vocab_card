import React from 'react';
import './Navigation.css';

const Navigation = ({ onClick, buttonText }) => {
  return (
    <button className="navigation-button" onClick={onClick}>
      {buttonText || '>'}
    </button>
  );
};

export default Navigation;
