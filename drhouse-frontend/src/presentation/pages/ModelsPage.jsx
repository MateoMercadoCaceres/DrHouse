import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../../styles/ModelsPage.css';
import MedicationsChat from '../components/chats/MedicationsChat';
import Header from '../components/layout/header/Header'; 
import DiagnosticChat from '../components/chats/DiagnosticChat';
import ImageGenerationsChat from '../components/chats/ImageGenerationsChat';
import Sidebar from '../components/common/Sidebar';

const ModelsPage = () => {
  const [selectedModel, setSelectedModel] = useState(null);

  const handleSidebarClick = () => {
    setSelectedModel(null);
  };

  return (
    <>
      <Header />
      <div className="container" style={{ background: 'none', position: 'relative', minHeight: 'calc(100vh - 87px)', display: 'flex', paddingTop: '87px' }}>
        <Sidebar onNextTaskClick={handleSidebarClick} />
        {/* Contenido principal */}
        <div style={{ flexGrow: 1, position: 'relative', minHeight: 'calc(100vh - 87px)', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', overflow: 'auto', marginLeft: '250px' }}>
          {/* Fondo de cubos */}
          <div className="background-grid">
            <div className="grid">
              {[...Array(144)].map((_, i) => (
                <div key={i} className="grid-cell"></div>
              ))}
            </div>
            <div className="glow-orb glow-orb-1"></div>
            <div className="glow-orb glow-orb-2"></div>
          </div>

          {/* Contenido central (Agentes y Footer) */}
          {selectedModel ? (
            <div style={{ position: 'relative', zIndex: 1, minHeight: 'calc(100vh - 87px)', width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
              {selectedModel === 'Medications' && <MedicationsChat hideHeader={false} />}
              {selectedModel === 'Diagnostic' && <DiagnosticChat hideHeader={false} />}
              {selectedModel === 'Creator Image' && <ImageGenerationsChat hideHeader={false} />}
            </div>
          ) : (
            <div style={{ position: 'relative', zIndex: 1, minHeight: 'calc(100vh - 87px)', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '20px' }}>
              <h1 style={{ color: 'white', fontWeight: 400, fontSize: '2.5rem', marginBottom: '1rem', textAlign: 'center' }}>
                AI Agents for <span style={{ color: '#ef4444' }}>Scientific</span> Discovery
              </h1>
              <p style={{ color: '#9ca3af', marginBottom: '2rem', textAlign: 'center' }}>
                Automate your research workflows. Try one to get started:
              </p>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '2rem', justifyContent: 'center', marginBottom: '2rem' }}>
                <div 
                  className="model-card"
                  style={{ 
                    background: 'rgba(17,24,39,0.8)', 
                    borderRadius: '12px', 
                    padding: '2rem', 
                    minWidth: '320px', 
                    maxWidth: '340px', 
                    color: 'white', 
                    boxShadow: '0 2px 16px #0002', 
                    cursor: 'pointer',
                    transition: 'all 0.3s ease',
                    border: '1px solid transparent'
                  }}
                  onClick={() => setSelectedModel('Medications')}
                >
                  <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>💊</div>
                  <div style={{ fontWeight: 600, fontSize: '1.1rem', marginBottom: '0.5rem' }}>Medications - <span style={{ color: '#60a5fa' }}>Medicamentos</span></div>
                  <div style={{ fontSize: '0.95rem', color: '#d1d5db' }}>
                    Descripción y usos de medicamentos...
                  </div>
                </div>
                <div 
                  className="model-card"
                  style={{ 
                    background: 'rgba(17,24,39,0.8)', 
                    borderRadius: '12px', 
                    padding: '2rem', 
                    minWidth: '320px', 
                    maxWidth: '340px', 
                    color: 'white', 
                    boxShadow: '0 2px 16px #0002', 
                    cursor: 'pointer',
                    transition: 'all 0.3s ease',
                    border: '1px solid transparent'
                  }}
                  onClick={() => setSelectedModel('Diagnostic')}
                >
                  <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>🩺</div>
                  <div style={{ fontWeight: 600, fontSize: '1.1rem', marginBottom: '0.5rem' }}>Diagnostic - <span style={{ color: '#60a5fa' }}>Diagnóstico</span></div>
                  <div style={{ fontSize: '0.95rem', color: '#d1d5db' }}>
                    Detectar enfermedades...
                  </div>
                </div>
                <div 
                  className="model-card"
                  style={{ 
                    background: 'rgba(17,24,39,0.8)', 
                    borderRadius: '12px', 
                    padding: '2rem', 
                    minWidth: '320px', 
                    maxWidth: '340px', 
                    color: 'white', 
                    boxShadow: '0 2px 16px #0002', 
                    cursor: 'pointer',
                    transition: 'all 0.3s ease',
                    border: '1px solid transparent'
                  }}
                  onClick={() => setSelectedModel('Creator Image')}
                >
                  <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>🎨</div>
                  <div style={{ fontWeight: 600, fontSize: '1.1rem', marginBottom: '0.5rem' }}>Creator Image - <span style={{ color: '#60a5fa' }}>Generador de Imágenes</span></div>
                  <div style={{ fontSize: '0.95rem', color: '#d1d5db' }}>
                    Crear medicamentos y composición...
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default ModelsPage;