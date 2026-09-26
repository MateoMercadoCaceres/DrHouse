import React, { useState, useEffect, useRef } from 'react';
import Header from '../components/layout/header/Header'; 
import '../../styles/AboutPage.css';

const MISSION_TEXT = `My mission is to make your life easier, so that you can access a more friendly health care system at any time and any day.`;

const mindmapNodes = [
  { key: 'quest', label: 'Response', desc: '(different highly trained ia models are used for the answers for your safety and health.)' },
  { key: 'wm', label: 'World Model' },
  { key: 'hg', label: 'Hypothesis Generation' },
  { key: 'exp', label: 'Experimentation' },
  { key: 'agents', label: 'Agents for Specific Biological Workflows', desc: '(Literature Search, Functional protein annotation, Designing new proteins, Single cell seq, etc.)', wide: true },
  { key: 'pm', label: 'Predictive Models', desc: '(e.g. AlphaFold)' },
  { key: 'apis', label: 'APIs' },
  { key: 'lab', label: 'Laboratory Experiments' },
];

const AboutPage = () => {
  // Máquina de escribir para misión
  const [typedMission, setTypedMission] = useState('');
  const [missionActive, setMissionActive] = useState(false);

  // Refs para los nodos del mapa mental
  const nodeRefs = useRef({});
  const [illuminatedNodes, setIlluminatedNodes] = useState({});

  // Máquina de escribir
  useEffect(() => {
    if (missionActive && typedMission.length < MISSION_TEXT.length) {
      const timeout = setTimeout(() => {
        setTypedMission(MISSION_TEXT.slice(0, typedMission.length + 1));
      }, 18);
      return () => clearTimeout(timeout);
    }
  }, [typedMission, missionActive]);

  // Intersection Observer para nodos del mapa mental
  useEffect(() => {
    const observer = new window.IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          const key = entry.target.dataset.key;
          if (entry.isIntersecting) {
            setIlluminatedNodes((prev) => ({ ...prev, [key]: true }));
          }
        });
      },
      { threshold: 0.5 }
    );
    mindmapNodes.forEach((node) => {
      if (nodeRefs.current[node.key]) {
        observer.observe(nodeRefs.current[node.key]);
      }
    });
    return () => observer.disconnect();
  }, []);

  // Permitir scroll en la página
  useEffect(() => {
    document.body.style.overflow = 'auto';
    return () => {
      document.body.style.overflow = '';
    };
  }, []);

  // Activar máquina de escribir cuando la misión esté en viewport
  const missionRef = useRef(null);
  useEffect(() => {
    const observer = new window.IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) setMissionActive(true);
        });
      },
      { threshold: 0.5 }
    );
    if (missionRef.current) observer.observe(missionRef.current);
    return () => observer.disconnect();
  }, []);

  return (
    <div className="container" style={{ minHeight: '100vh', overflow: 'visible' }}>
      <Header />
      {/* Título ABOUT */}
      <div className="main-content" style={{ paddingTop: 32, paddingBottom: 0 }}>
        <div className="left-content" style={{ alignItems: 'center' }}>
          <div className="hero-section">
            <p className="subtitle">MODELS AND IAs</p>
            <div className="title-container">
              <h1 className="main-title">
                <span className="title-highlight">A</span>
                <span className="title-text">BOUT</span>
              </h1>
              <div className="title-accent"></div>
            </div>
          </div>
        </div>
      </div>

      {/* Sección Misión */}
      <section
        ref={missionRef}
        className="about-section mission-section"
      >
        <p className="about-section-title">MISSION</p>
        <h2 className="mission-typewriter">{typedMission}</h2>
      </section>

      {/* Sección Mapa Mental */}
      <section className="about-section map-section">
        <p className="about-section-title">The four layers of science automation:</p>
        <div className="mindmap">
          {/* Fila 1: Quest */}
          <div className="mindmap-row">
            <div
              ref={el => nodeRefs.current['quest'] = el}
              data-key="quest"
              className={`mindmap-node quest${illuminatedNodes['quest'] ? ' illuminated' : ''}`}
            >
              Response
              <div className="mindmap-desc">(different highly trained ia models are used for the answers for your safety and health.)</div>
            </div>
          </div>
          {/* Fila 2: World Model, Hypothesis Generation, Experimentation */}
          <div className="mindmap-row">
            <div
              ref={el => nodeRefs.current['wm'] = el}
              data-key="wm"
              className={`mindmap-node${illuminatedNodes['wm'] ? ' illuminated' : ''}`}
            >DeepSeek-r1</div>
            <div
              ref={el => nodeRefs.current['hg'] = el}
              data-key="hg"
              className={`mindmap-node${illuminatedNodes['hg'] ? ' illuminated' : ''}`}
            >DeepSeek-v3</div>
            <div
              ref={el => nodeRefs.current['exp'] = el}
              data-key="exp"
              className={`mindmap-node${illuminatedNodes['exp'] ? ' illuminated' : ''}`}
            >Gemini-generationia</div>
          </div>
          {/* Fila 3: Agents */}
          <div className="mindmap-row">
            <div
              ref={el => nodeRefs.current['agents'] = el}
              data-key="agents"
              className={`mindmap-node wide agents${illuminatedNodes['agents'] ? ' illuminated' : ''}`}
            >
              These models are specialized in the use of science and medicine.
              <div className="mindmap-desc small">(Medical diagnostics, disease understanding, drug screening and imaging)</div>
            </div>
          </div>
          {/* Fila 4: Predictive Models, APIs, Laboratory Experiments */}
          <div className="mindmap-row">
            <div
              ref={el => nodeRefs.current['pm'] = el}
              data-key="pm"
              className={`mindmap-node${illuminatedNodes['pm'] ? ' illuminated' : ''}`}
            >DrHouse-models<br/><span className="mindmap-desc small">(4 models working in your security)</span></div>
            <div
              ref={el => nodeRefs.current['apis'] = el}
              data-key="apis"
              className={`mindmap-node${illuminatedNodes['apis'] ? ' illuminated' : ''}`}
            >DrHouse-backend</div>
            <div
              ref={el => nodeRefs.current['lab'] = el}
              data-key="lab"
              className={`mindmap-node${illuminatedNodes['lab'] ? ' illuminated' : ''}`}
            >DrHouse-frontend</div>
          </div>
        </div>
      </section>

      {/* Fondo cuadriculado y orbes */}
      <div className="background-grid">
        <div className="grid">
          {[...Array(144)].map((_, i) => (
            <div key={i} className="grid-cell"></div>
          ))}
        </div>
      </div>
      <div className="glow-orb glow-orb-1"></div>
      <div className="glow-orb glow-orb-2"></div>
    </div>
  );
};

export default AboutPage;