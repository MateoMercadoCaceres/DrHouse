import React from 'react';
import '../../../styles/Sidebar.css';

const Sidebar = ({ onNextTaskClick }) => {
  return (
    <div style={{
      width: '250px',
      height: '100vh',
      background: '#111827',
      color: 'white',
      padding: '100px 20px 20px',
      position: 'fixed',
      left: 0,
      top: 0,
      display: 'flex',
      flexDirection: 'column'
    }}>

      <div style={{ marginBottom: '30px' }}>
        <button 
          onClick={onNextTaskClick}
          className="sidebar-button"
          style={{
            width: '100%',
            display: 'flex',
            alignItems: 'center',
            marginBottom: '15px',
            background: 'transparent',
            border: 'none',
            color: 'white',
            cursor: 'pointer',
            padding: '10px',
            borderRadius: '8px',
            transition: 'all 0.3s ease'
          }}
        >
          <span style={{ marginRight: '10px' }}>📄</span>
          New Task +
        </button>
        <button 
          className="sidebar-button"
          style={{
            width: '100%',
            display: 'flex',
            alignItems: 'center',
            background: 'transparent',
            border: 'none',
            color: 'white',
            cursor: 'pointer',
            padding: '10px',
            borderRadius: '8px',
            transition: 'all 0.3s ease'
          }}
        >
          <span style={{ marginRight: '10px' }}>🕒</span>
          Recent Tasks <a href="#" style={{ color: '#60a5fa', marginLeft: 'auto', textDecoration: 'none' }}>view all</a>
        </button>
      </div>

      <div style={{ borderTop: '1px solid #333', paddingTop: '20px', flexGrow: 1 }}>
        <button 
          className="sidebar-button"
          style={{
            width: '100%',
            display: 'flex',
            alignItems: 'center',
            marginBottom: '15px',
            background: 'transparent',
            border: 'none',
            color: 'white',
            cursor: 'pointer',
            padding: '10px',
            borderRadius: '8px',
            transition: 'all 0.3s ease'
          }}
        >
          <span style={{ marginRight: '10px' }}>&lt;/&gt;</span>
          API
        </button>
        <button 
          className="sidebar-button"
          style={{
            width: '100%',
            display: 'flex',
            alignItems: 'center',
            marginBottom: '15px',
            background: 'transparent',
            border: 'none',
            color: 'white',
            cursor: 'pointer',
            padding: '10px',
            borderRadius: '8px',
            transition: 'all 0.3s ease'
          }}
        >
          <span style={{ marginRight: '10px' }}>⚙️</span>
          Settings
        </button>
      </div>
    </div>
  );
};

export default Sidebar;
