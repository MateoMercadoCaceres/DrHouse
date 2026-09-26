import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

const Header = () => {
  return (
    <nav className="header-navigation">
      <div className="header-logo">DrHouse</div>
      
      <div className="header-nav-menu">
        <Link to="/home" className="header-nav-link">HOME</Link>
        <Link to="/about" className="header-nav-link">ABOUT</Link>
        <Link to="/models" className="header-nav-link">MODELS</Link>
        <Link to="/contacts" className="header-nav-link">CONTACTS</Link>
      </div>
      
      <div className="header-nav-controls">
        <Link to="/login" className="header-login-btn">
          <span className="login-text">LOGIN</span>
          <div className="login-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/>
              <polyline points="10,17 15,12 10,7"/>
              <line x1="15" y1="12" x2="3" y2="12"/>
            </svg>
          </div>
        </Link>
        <span className="header-language">ENG</span>
        <div className="header-grid-dots">
          {[...Array(9)].map((_, i) => (
            <div key={i} className="header-dot"></div>
          ))}
        </div>
      </div>
    </nav>
  );
};

export default Header;