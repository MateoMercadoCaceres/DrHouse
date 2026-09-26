import React, { useState, useRef, useEffect } from 'react';
import { createImageService, extractMedicineName } from '../../../infrastructure/services/createImage';
import '../../../styles/ModelsPage.css';

const ImageGenerationsChat = ({ hideHeader = false }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "¡Hola! Soy tu asistente de imágenes sobre medicamentos. Puedo generar imágenes de medicamentos para ti. ¿En qué puedo ayudarte hoy?",
      sender: 'bot',
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isGeneratingImage, setIsGeneratingImage] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll al último mensaje
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Función para generar imagen de medicamento
  const generateMedicineImage = async (medicineName) => {
    setIsGeneratingImage(true);
    
    try {
      const result = await createImageService(medicineName);
      
      if (result.success) {
        return {
          text: `Aquí tienes la imagen del medicamento ${medicineName}:`,
          imageUrl: result.imageUrl,
          hasImage: true
        };
      } else {
        return {
          text: `Lo siento, no pude generar la imagen para ${medicineName}. ${result.error || 'Inténtalo de nuevo más tarde.'}`,
          hasImage: false
        };
      }
    } catch (error) {
      console.error('Error generando imagen:', error);
      return {
        text: `Hubo un error al generar la imagen para ${medicineName}. Por favor, inténtalo de nuevo.`,
        hasImage: false
      };
    } finally {
      setIsGeneratingImage(false);
    }
  };

  // Respuestas automáticas del bot mejoradas
  const getBotResponse = async (userMessage) => {
    const message = userMessage.toLowerCase();
    
    // Verificar si el usuario quiere una imagen
    const medicineName = extractMedicineName(userMessage);
    if (medicineName) {
      return await generateMedicineImage(medicineName);
    }
    
    // Respuestas existentes
    if (message.includes('dolor') || message.includes('aspirina') || message.includes('ibuprofeno')) {
      return {
        text: "Para el dolor, es importante consultar con un médico antes de tomar cualquier medicamento. ¿Podrías describir el tipo de dolor que tienes? También puedo mostrarte imágenes de medicamentos si lo necesitas.",
        hasImage: false
      };
    }
    
    if (message.includes('dosis') || message.includes('cantidad')) {
      return {
        text: "Las dosis de medicamentos deben ser siempre prescritas por un profesional de la salud. ¿Tienes alguna receta médica específica sobre la que quieres consultar? Puedo generar imágenes de medicamentos para ayudarte a identificarlos.",
        hasImage: false
      };
    }
    
    if (message.includes('efectos') || message.includes('secundarios')) {
      return {
        text: "Los efectos secundarios pueden variar según la persona y el medicamento. Te recomiendo consultar el prospecto del medicamento o hablar con tu farmacéutico.",
        hasImage: false
      };
    }
    
    if (message.includes('hola') || message.includes('buenas')) {
      return {
        text: "¡Hola! Me alegra verte por aquí. ¿Tienes alguna pregunta sobre medicamentos o quieres que genere alguna imagen de un medicamento específico?",
        hasImage: false
      };
    }
    
    if (message.includes('gracias')) {
      return {
        text: "¡De nada! Estoy aquí para ayudarte con cualquier duda sobre medicamentos o generar imágenes. ¿Hay algo más en lo que pueda asistirte?",
        hasImage: false
      };
    }
    
    if (message.includes('qué puedes hacer') || message.includes('ayuda') || message.includes('comandos')) {
      return {
        text: "Puedo ayudarte con:\n• Generar imágenes de medicamentos (ej: 'muestra imagen de paracetamol')\n• Responder preguntas básicas sobre medicamentos\n• Proporcionar información general sobre tratamientos\n\nRecuerda siempre consultar con profesionales de la salud.",
        hasImage: false
      };
    }
    
    return {
      text: "Entiendo tu consulta. Recuerda que siempre es importante consultar con un profesional de la salud para obtener información médica precisa. ¿Puedes darme más detalles sobre tu consulta? También puedo generar imágenes de medicamentos si me dices cuál necesitas.",
      hasImage: false
    };
  };

  const handleSendMessage = async () => {
    if (inputValue.trim() === '') return;

    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = inputValue;
    setInputValue('');
    setIsTyping(true);

    try {
      // Generar respuesta del bot
      const botResponseData = await getBotResponse(currentInput);
      
      setTimeout(() => {
        const botResponse = {
          id: Date.now() + 1,
          text: botResponseData.text,
          sender: 'bot',
          timestamp: new Date(),
          imageUrl: botResponseData.imageUrl || null,
          hasImage: botResponseData.hasImage || false
        };
        
        setMessages(prev => [...prev, botResponse]);
        setIsTyping(false);
      }, 800);
      
    } catch (error) {
      console.error('Error processing message:', error);
      setTimeout(() => {
        const errorResponse = {
          id: Date.now() + 1,
          text: "Lo siento, hubo un error procesando tu mensaje. Por favor, inténtalo de nuevo.",
          sender: 'bot',
          timestamp: new Date(),
          hasImage: false
        };
        
        setMessages(prev => [...prev, errorResponse]);
        setIsTyping(false);
      }, 800);
    }
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
    <div className="chat-container" style={{ background: '#192233', height: 'calc(100vh - 87px)' }}>
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
            🎨 Generador de Imágenes de Medicamentos
          </h2>
          <p style={{ 
            margin: '5px 0 0 0', 
            color: '#7f8c8d',
            fontSize: '14px'
          }}>
            Asistente médico virtual - Genera imágenes y consulta sobre medicamentos
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
                <div style={{ fontSize: '15px', lineHeight: '1.4', whiteSpace: 'pre-line' }}>
                  {message.text}
                </div>
                
                {/* Mostrar imagen si existe */}
                {message.hasImage && message.imageUrl && (
                  <div style={{ marginTop: '10px' }}>
                    <img
                      src={message.imageUrl}
                      alt="Imagen del medicamento"
                      style={{
                        maxWidth: '100%',
                        height: 'auto',
                        borderRadius: '8px',
                        boxShadow: '0 2px 10px rgba(0,0,0,0.2)'
                      }}
                      onError={(e) => {
                        e.target.style.display = 'none';
                        // Agregar mensaje de error si la imagen no carga
                        const errorMsg = document.createElement('div');
                        errorMsg.textContent = 'Error cargando la imagen';
                        errorMsg.style.color = '#ffcccc';
                        errorMsg.style.fontSize = '12px';
                        errorMsg.style.marginTop = '5px';
                        e.target.parentNode.appendChild(errorMsg);
                      }}
                    />
                  </div>
                )}
                
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
          {(isTyping || isGeneratingImage) && (
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
                  <span>{isGeneratingImage ? 'Generando imagen' : 'Escribiendo'}</span>
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
                placeholder="Escribe tu consulta o pide una imagen (ej: 'mostrar imagen de paracetamol')..."
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
              disabled={inputValue.trim() === '' || isTyping || isGeneratingImage}
              style={{
                width: '50px',
                height: '50px',
                borderRadius: '50%',
                border: 'none',
                background: inputValue.trim() === '' || isTyping || isGeneratingImage
                  ? '#bdc3c7' 
                  : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                cursor: inputValue.trim() === '' || isTyping || isGeneratingImage ? 'not-allowed' : 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '20px',
                boxShadow: '0 4px 15px rgba(0,0,0,0.2)',
                transition: 'all 0.3s ease',
                transform: 'scale(1)'
              }}
              onMouseEnter={(e) => {
                if (inputValue.trim() !== '' && !isTyping && !isGeneratingImage) {
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

export default ImageGenerationsChat;