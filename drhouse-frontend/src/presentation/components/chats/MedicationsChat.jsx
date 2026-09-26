import React, { useState, useRef, useEffect } from 'react';
import '../../../styles/ModelsPage.css';

const MedicationsChat = ({ hideHeader = false }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "¡Hola! Soy tu asistente de medicamentos. ¿En qué puedo ayudarte hoy?",
      sender: 'bot',
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll al último mensaje
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Respuestas automáticas del bot
  const getBotResponse = (userMessage) => {
    const message = userMessage.toLowerCase();
    
    if (message.includes('dolor') || message.includes('aspirina') || message.includes('ibuprofeno')) {
      return "Para el dolor, es importante consultar con un médico antes de tomar cualquier medicamento. ¿Podrías describir el tipo de dolor que tienes?";
    }
    
    if (message.includes('dosis') || message.includes('cantidad')) {
      return "Las dosis de medicamentos deben ser siempre prescritas por un profesional de la salud. ¿Tienes alguna receta médica específica sobre la que quieres consultar?";
    }
    
    if (message.includes('efectos') || message.includes('secundarios')) {
      return "Los efectos secundarios pueden variar según la persona y el medicamento. Te recomiendo consultar el prospecto del medicamento o hablar con tu farmacéutico.";
    }
    
    if (message.includes('hola') || message.includes('buenas')) {
      return "¡Hola! Me alegra verte por aquí. ¿Tienes alguna pregunta sobre medicamentos o tratamientos?";
    }
    
    if (message.includes('gracias')) {
      return "¡De nada! Estoy aquí para ayudarte con cualquier duda sobre medicamentos. ¿Hay algo más en lo que pueda asistirte?";
    }
    
    return "Entiendo tu consulta. Recuerda que siempre es importante consultar con un profesional de la salud para obtener información médica precisa. ¿Puedes darme más detalles sobre tu consulta?";
  };

  const handleSendMessage = async () => {
    if (inputValue.trim() === '') return;

    const userMessage = {
      id: messages.length + 1,
      text: inputValue,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsTyping(true);

    // Simular respuesta del bot con delay
    setTimeout(() => {
      const botResponse = {
        id: messages.length + 2,
        text: getBotResponse(inputValue),
        sender: 'bot',
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, botResponse]);
      setIsTyping(false);
    }, 1000 + Math.random() * 1000); // Delay aleatorio entre 1-2 segundos
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const formatTime = (date) => {
    return date.toLocaleTimeString('es-ES', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div className="chat-container" style={{ background: '#192233'}}>
      <div className="background-grid">
        <div className="grid">
          {Array.from({ length: 144 }).map((_, index) => (
            <div key={index} className="grid-cell" />
          ))}
        </div>
      </div>
      
      <div className="chat-content" style={{ 
        color: '#333',
        height: '100vh',
        display: 'flex',
        flexDirection: 'column',
        position: 'relative',
        zIndex: 1,
        background: 'transparent',
        backdropFilter: 'blur(10px)'
      }}>
        {/* Header del chat */}
        {!hideHeader && (
        <div style={{
          background: 'rgba(25, 29, 58, 0.95)',
          padding: '20px',
          backdropFilter: 'blur(10px)',
          borderRadius: '10px',
        }}>
          <h2 style={{ 
            margin: 0, 
            color: '#ffffff',
            fontSize: '24px',
            fontWeight: '600'
          }}>
            💊 Consulta de Medicamentos
          </h2>
          <p style={{ 
            margin: '5px 0 0 0', 
            color: '#7f8c8d',
            fontSize: '14px'
          }}>
            Asistente médico virtual - Recuerda consultar siempre con profesionales
          </p>
        </div>
        )}

        {/* Área de mensajes */}
        <div style={{
          flex: 1,
          overflowY: 'auto',
          padding: '20px',
          backdropFilter: 'blur(10px)'
        }}>
          {messages.map((message) => (
            <div
              key={message.id}
              style={{
                display: 'flex',
                justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start',
                marginBottom: '15px'
              }}
            >
              <div
                style={{
                  maxWidth: '70%',
                  padding: '12px 16px',
                  borderRadius: message.sender === 'user' ? '20px 20px 5px 20px' : '20px 20px 20px 5px',
                  background: message.sender === 'user' 
                    ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                    : 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                  color: 'white',
                  boxShadow: '0 4px 15px rgba(0,0,0,0.1)',
                  position: 'relative'
                }}
              >
                <div style={{ fontSize: '15px', lineHeight: '1.4' }}>
                  {message.text}
                </div>
                <div style={{ 
                  fontSize: '11px', 
                  opacity: 0.8, 
                  marginTop: '5px',
                  textAlign: message.sender === 'user' ? 'right' : 'left'
                }}>
                  {formatTime(message.timestamp)}
                </div>
              </div>
            </div>
          ))}
          
          {/* Indicador de escritura */}
          {isTyping && (
            <div style={{
              display: 'flex',
              justifyContent: 'flex-start',
              marginBottom: '15px'
            }}>
              <div style={{
                padding: '12px 16px',
                borderRadius: '20px 20px 20px 5px',
                background: 'rgba(52, 73, 94, 0.1)',
                color: '#34495e',
                fontStyle: 'italic'
              }}>
                <div style={{ display: 'flex', alignItems: 'center' }}>
                  <span>Escribiendo</span>
                  <div style={{ marginLeft: '8px', display: 'flex', gap: '2px' }}>
                    <div style={{ 
                      width: '4px', 
                      height: '4px', 
                      background: '#34495e', 
                      borderRadius: '50%',
                      animation: 'pulse 1.5s infinite ease-in-out'
                    }}></div>
                    <div style={{ 
                      width: '4px', 
                      height: '4px', 
                      background: '#34495e', 
                      borderRadius: '50%',
                      animation: 'pulse 1.5s infinite ease-in-out 0.2s'
                    }}></div>
                    <div style={{ 
                      width: '4px', 
                      height: '4px', 
                      background: '#34495e', 
                      borderRadius: '50%',
                      animation: 'pulse 1.5s infinite ease-in-out 0.4s'
                    }}></div>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input de escritura */}
        <div style={{
          padding: '20px',
          background: 'transparent',
          backdropFilter: 'blur(10px)'
        }}>
          <div style={{
            display: 'flex',
            gap: '10px',
            alignItems: 'center',
            minHeight: '50px',
          }}>
            <div style={{ flex: 1, position: 'relative' }}>
              <textarea
                ref={inputRef}
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Escribe tu consulta sobre medicamentos..."
                style={{
                  width: '100%',
                  minHeight: '50px',
                  maxHeight: '120px',
                  padding: '15px 20px',
                  border: '2px solid #e0e0e0',
                  borderRadius: '25px',
                  fontSize: '15px',
                  resize: 'none',
                  outline: 'none',
                  fontFamily: 'inherit',
                  background: 'white',
                  boxShadow: '0 2px 10px rgba(0,0,0,0.05)',
                  transition: 'all 0.3s ease'
                }}
                onFocus={(e) => {
                  e.target.style.borderColor = '#667eea';
                  e.target.style.boxShadow = '0 4px 20px rgba(102, 126, 234, 0.2)';
                }}
                onBlur={(e) => {
                  e.target.style.borderColor = '#e0e0e0';
                  e.target.style.boxShadow = '0 2px 10px rgba(0,0,0,0.05)';
                }}
              />
            </div>
            <button
              onClick={handleSendMessage}
              disabled={inputValue.trim() === '' || isTyping}
              style={{
                width: '50px',
                height: '50px',
                borderRadius: '50%',
                border: 'none',
                background: inputValue.trim() === '' || isTyping 
                  ? '#bdc3c7' 
                  : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                cursor: inputValue.trim() === '' || isTyping ? 'not-allowed' : 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '20px',
                boxShadow: '0 4px 15px rgba(0,0,0,0.2)',
                transition: 'all 0.3s ease',
                transform: 'scale(1)'
              }}
              onMouseEnter={(e) => {
                if (inputValue.trim() !== '' && !isTyping) {
                  e.target.style.transform = 'scale(1.05)';
                }
              }}
              onMouseLeave={(e) => {
                e.target.style.transform = 'scale(1)';
              }}
            >
              ➤
            </button>
          </div>
        </div>
      </div>

      {/* Estilos para la animación */}
      <style jsx>{`
        @keyframes pulse {
          0%, 60%, 100% {
            transform: scale(1);
            opacity: 1;
          }
          30% {
            transform: scale(1.2);
            opacity: 0.7;
          }
        }
      `}</style>
    </div>
  );
};

export default MedicationsChat;