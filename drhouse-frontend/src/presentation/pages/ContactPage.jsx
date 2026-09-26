import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import '../../styles/HomePage.css';
import heartImage from '../assets/icons/homeHeart.png';

const HomePage = () => {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e) => {
      setMousePosition({ x: e.clientX, y: e.clientY });
    };
    
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return (
    <div className="container">
      {/* Navigation */}
      <nav className="navigation">
        <div className="logo">NJEV</div>
        <div className="nav-menu">
          <Link to="/home" className="nav-link">HOME</Link>
          <Link to="/about" className="nav-link">ABOUT</Link>
          <Link to="/works" className="nav-link">WORKS</Link>
          <Link to="/services" className="nav-link">SERVICES</Link>
          <Link to="/contacts" className="nav-link">CONTACTS</Link>
        </div>
        <div className="nav-controls">
          <span className="language">ENG</span>
          <div className="grid-dots">
            {[...Array(9)].map((_, i) => (
              <div key={i} className="dot"></div>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="main-content">
        {/* Left Content */}
        <div className="left-content">
          <div className="hero-section">
            <p className="subtitle">HERE AND NOW</p>
            <div className="title-container">
              <h1 className="main-title">
                <span className="title-highlight">F</span>
                <span className="title-text">UTURE</span>
              </h1>
              <div className="title-accent"></div>
            </div>
          </div>
          
          <p className="description">
            People who think about the future, about how to improve their lives, 
            and take action in this direction, have a plan of action
          </p>
          
          <button className="cta-button">
            LET'S GO
          </button>
        </div>

        {/* Right Content - Heart Image */}
        <div className="right-content">
          <div className="heart-container">
            <div 
              className="heart-figure"
              style={{
                transform: `translate(${mousePosition.x * 0.01}px, ${mousePosition.y * 0.01}px)`
              }}
            >
              {/* Heart Image */}
              <div className="heart-image-wrapper">
                <img 
                  src={heartImage} 
                  alt="Heart" 
                  className="heart-image"
                />
                <div className="heart-glow"></div>
              </div>

              {/* Animated particles around heart */}
              <div className="particle particle-1"></div>
              <div className="particle particle-2"></div>
              <div className="particle particle-3"></div>
              <div className="particle particle-4"></div>

              {/* Floating elements */}
              <div className="floating-ring"></div>
              <div className="floating-orb"></div>
              
              {/* Heartbeat lines */}
              <div className="heartbeat-line heartbeat-line-1"></div>
              <div className="heartbeat-line heartbeat-line-2"></div>
            </div>

            {/* Labels */}
            <div className="label-ai">ARTIFICIAL INTELLIGENCE</div>
            <div className="label-emotion">PURE EMOTION</div>
          </div>
        </div>
      </div>

      {/* Social Links */}
      <div className="social-links">
        {['Vk', 'Tw', 'Fb', 'In', 'Be'].map((social) => (
          <a key={social} href="#" className="social-link">
            {social}
          </a>
        ))}
      </div>

      {/* Bottom Content */}
      <div className="bottom-content">
        <div className="bottom-section">
          <h3 className="section-title">TECHNOLOGY</h3>
          <p className="section-description">
            Lorem ipsum dolor sit amet, do consectetur adipiscing elit, sed
          </p>
        </div>
        <div className="bottom-section">
          <h3 className="section-title">INNOVATION</h3>
          <p className="section-description">
            Tempor incididunt ut labore dolore magna aliqua
          </p>
        </div>
      </div>

      {/* Background Grid */}
      <div className="background-grid">
        <div className="grid">
          {[...Array(144)].map((_, i) => (
            <div key={i} className="grid-cell"></div>
          ))}
        </div>
      </div>

      {/* Glowing orbs */}
      <div className="glow-orb glow-orb-1"></div>
      <div className="glow-orb glow-orb-2"></div>
    </div>
  );
};

export default HomePage;