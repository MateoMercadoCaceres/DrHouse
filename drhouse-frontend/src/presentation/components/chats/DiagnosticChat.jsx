import React, { useState, useRef, useEffect } from 'react';
import { diagnosticService } from '../../../infrastructure/services/diagnosticChat';
import '../../../styles/ModelsPage.css';

const DiagnosticChat = ({ hideHeader = false }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "¡Hola! Soy tu asistente de diagnosticos medicos. ¿En qué puedo ayudarte hoy?",
      sender: 'bot',
      timestamp: new Date(),
      images: []
    }
  ]);
  const [showCurrentMode, setShowCurrentMode] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [attachedImages, setAttachedImages] = useState([]);
  const [selectedMode, setSelectedMode] = useState('diagnose');
  const [showModeSelector, setShowModeSelector] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const fileInputRef = useRef(null);

  // Auto-scroll al último mensaje
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Manejar selección de archivos
  const handleFileSelect = (event) => {
    const files = Array.from(event.target.files);
    const remainingSlots = 3 - attachedImages.length;
    const filesToAdd = files.slice(0, remainingSlots);
    
    filesToAdd.forEach(file => {
      if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (e) => {
          const newImage = {
            id: Date.now() + Math.random(),
            file: file,
            url: e.target.result,
            name: file.name
          };
          setAttachedImages(prev => [...prev, newImage]);
        };
        reader.readAsDataURL(file);
      }
    });
    
    // Resetear el input
    event.target.value = '';
  };

  // Remover imagen adjunta
  const removeAttachedImage = (imageId) => {
    setAttachedImages(prev => prev.filter(img => img.id !== imageId));
  };

  // Respuestas automáticas del bot
// Respuestas automáticas del bot
  const getBotResponse = async (userMessage, hasImages, selectedMode) => {
    try {
      console.log('Llamando a diagnosticService con:', { userMessage, selectedMode });
      const response = await diagnosticService(userMessage, selectedMode);
      
      console.log('Respuesta recibida de diagnosticService:', response);
      
      // Verificar si es la nueva estructura con description y treatment_recommendations
      if (response.description && response.treatment_recommendations) {
        return {
          message: response.description,
          hasTreatments: true,
          treatments: response.treatment_recommendations,
          diagnosis: response.diagnosis || response.disease_name,
          severity: response.severity
        };
      }
      
      // Procesar la respuesta del diagnóstico (estructura anterior)
      if (response.symptoms && response.final_diagnosis) {
        const symptoms = response.symptoms;
        const diagnosis = response.final_diagnosis;
        
        // Formatear los síntomas
        let symptomsText = '';
        if (symptoms.length > 0) {
          if (symptoms.length === 1) {
            symptomsText = symptoms[0];
          } else if (symptoms.length === 2) {
            symptomsText = symptoms.join(' y ');
          } else {
            symptomsText = symptoms.slice(0, -1).join(', ') + ' y ' + symptoms[symptoms.length - 1];
          }
        }
        
        // Crear mensaje de respuesta
        let botMessage = '';
        if (symptomsText && diagnosis !== 'No definido') {
          botMessage = `Por lo que parece, tienes como síntomas: ${symptomsText}, y como diagnóstico podría ser: ${diagnosis}.`;
        } else if (symptomsText) {
          botMessage = `He identificado los siguientes síntomas: ${symptomsText}. Sin embargo, no puedo establecer un diagnóstico específico en este momento.`;
        } else if (diagnosis !== 'No definido') {
          botMessage = `Basándome en tu consulta, el posible diagnóstico es: ${diagnosis}.`;
        } else {
          botMessage = 'He procesado tu consulta, pero necesito más información para poder ayudarte mejor.';
        }
        
        return {
          message: botMessage,
          diagnosis: diagnosis !== 'No definido' ? diagnosis : null,
          symptoms: symptoms,
          hasTreatments: false
        };
      }
      
      // Fallback para otras estructuras
      return {
        message: "No pude procesar tu consulta en este momento.",
        diagnosis: null,
        symptoms: [],
        hasTreatments: false
      };
    } catch (error) {
      console.error('Error en diagnóstico:', error);
      return {
        message: "Lo siento, hay un problema temporal con el servicio. Por favor, intenta más tarde.",
        diagnosis: null,
        symptoms: [],
        hasTreatments: false
      };
    }
  };

  const handleSendMessage = async () => {
    if (inputValue.trim() === '' && attachedImages.length === 0) return;

    const userMessage = {
      id: messages.length + 1,
      text: inputValue || (attachedImages.length > 0 ? "Imagen(es)" : ""),
      sender: 'user',
      timestamp: new Date(),
      images: [...attachedImages]
    };

    setMessages(prev => [...prev, userMessage]);
    const hasImages = attachedImages.length > 0;
    const currentInput = inputValue;
    setInputValue('');
    setAttachedImages([]);
    setIsTyping(true);

    try {
      // Obtener la respuesta del bot
      const botResponseData = await getBotResponse(currentInput, hasImages, selectedMode);
      
      const botResponse = {
        id: messages.length + 2,
        text: botResponseData.message,
        sender: 'bot',
        timestamp: new Date(),
        images: [],
        diagnosis: botResponseData.diagnosis,
        symptoms: botResponseData.symptoms,
        hasTreatments: botResponseData.hasTreatments,
        treatments: botResponseData.treatments,
        severity: botResponseData.severity,
        showTreatmentButtons: botResponseData.hasTreatments // Para mostrar los botones
      };
      
      setMessages(prev => [...prev, botResponse]);
    } catch (error) {
      const errorResponse = {
        id: messages.length + 2,
        text: "Lo siento, ocurrió un error al procesar tu mensaje.",
        sender: 'bot',
        timestamp: new Date(),
        images: []
      };
      setMessages(prev => [...prev, errorResponse]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleTreatmentResponse = (messageId, wantsTreatment) => {
    setMessages(prev => prev.map(msg => {
      if (msg.id === messageId) {
        return {
          ...msg,
          showTreatmentButtons: false,
          showTreatmentResponse: true,
          treatmentAccepted: wantsTreatment
        };
      }
      return msg;
    }));

    // Agregar mensaje de respuesta
    const responseMessage = {
      id: messages.length + 100 + messageId, // ID único
      text: wantsTreatment 
        ? "Aquí tienes las recomendaciones de tratamiento:"
        : "¿Requieres alguna consulta más?",
      sender: 'bot',
      timestamp: new Date(),
      images: [],
      isFollowUp: true,
      treatments: wantsTreatment ? messages.find(m => m.id === messageId)?.treatments : null
    };

    setTimeout(() => {
      setMessages(prev => [...prev, responseMessage]);
    }, 500);
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

  // Componente para mostrar imágenes en los mensajes
  const ImageGallery = ({ images }) => {
    if (images.length === 0) return null;
    
    return (
      <div style={{ 
        display: 'flex', 
        flexWrap: 'wrap', 
        gap: '8px', 
        marginTop: '8px' 
      }}>
        {images.map((image, index) => (
          <div key={index} style={{ position: 'relative' }}>
            <img
              src={image.url}
              alt={`Adjunto ${index + 1}`}
              style={{
                maxWidth: '150px',
                maxHeight: '150px',
                borderRadius: '8px',
                objectFit: 'cover',
                cursor: 'pointer'
              }}
              onClick={() => {
                // Abrir imagen en ventana nueva para ver en tamaño completo
                window.open(image.url, '_blank');
              }}
            />
          </div>
        ))}
      </div>
    );
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
            🩺 Consulta de Diagnósticos Médicos
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
        {/* Modal selector de modo */}
        {showModeSelector && (
          <div style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'rgba(0,0,0,0.5)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000
          }}>
            <div style={{
              background: 'white',
              borderRadius: '15px',
              padding: '30px',
              maxWidth: '400px',
              width: '90%',
              boxShadow: '0 10px 30px rgba(0,0,0,0.3)'
            }}>
              <h3 style={{ marginTop: 0, color: '#333', textAlign: 'center' }}>
                Selecciona el tipo de consulta
              </h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                {[
                  { mode: 'diagnose', label: '🩺 Diagnóstico', desc: 'Análisis de síntomas' },
                  { mode: 'symptoms', label: '🔍 Síntomas', desc: 'Explorar síntomas' },
                  { mode: 'explain', label: '📚 Explicar', desc: 'Información médica' }
                ].map(option => (
                  <button
                    key={option.mode}
                    onClick={() => {
                      setSelectedMode(option.mode);
                      setShowModeSelector(false);
                    }}
                    style={{
                      padding: '15px',
                      border: selectedMode === option.mode ? '2px solid #667eea' : '2px solid #e0e0e0',
                      borderRadius: '10px',
                      background: selectedMode === option.mode ? 'rgba(102, 126, 234, 0.1)' : 'white',
                      cursor: 'pointer',
                      textAlign: 'left',
                      transition: 'all 0.3s ease'
                    }}
                  >
                    <div style={{ fontSize: '16px', fontWeight: '600', marginBottom: '5px' }}>
                      {option.label}
                    </div>
                    <div style={{ fontSize: '14px', color: '#666' }}>
                      {option.desc}
                    </div>
                  </button>
                ))}
              </div>
              <button
                onClick={() => setShowModeSelector(false)}
                style={{
                  marginTop: '20px',
                  padding: '10px 20px',
                  background: '#e74c3c',
                  color: 'white',
                  border: 'none',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  width: '100%'
                }}
              >
                Cancelar
              </button>
            </div>
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
                  <ImageGallery images={message.images} />
                  
                  {/* Botones de tratamiento */}
                  {message.showTreatmentButtons && (
                    <div style={{ 
                      marginTop: '15px', 
                      display: 'flex', 
                      gap: '10px', 
                      justifyContent: 'center',
                      flexWrap: 'wrap'
                    }}>
                      <div style={{ 
                        width: '100%', 
                        textAlign: 'center', 
                        fontSize: '14px', 
                        marginBottom: '10px',
                        opacity: 0.9
                      }}>
                        ¿Quieres que te dé tratamientos recomendados?
                      </div>
                      <button
                        onClick={() => handleTreatmentResponse(message.id, true)}
                        style={{
                          padding: '8px 16px',
                          background: '#27ae60',
                          color: 'white',
                          border: 'none',
                          borderRadius: '20px',
                          cursor: 'pointer',
                          fontSize: '14px',
                          transition: 'all 0.3s ease',
                          boxShadow: '0 2px 8px rgba(39, 174, 96, 0.3)'
                        }}
                        onMouseEnter={(e) => {
                          e.target.style.background = '#2ecc71';
                          e.target.style.transform = 'translateY(-1px)';
                        }}
                        onMouseLeave={(e) => {
                          e.target.style.background = '#27ae60';
                          e.target.style.transform = 'translateY(0)';
                        }}
                      >
                        Sí, quiero tratamientos
                      </button>
                      <button
                        onClick={() => handleTreatmentResponse(message.id, false)}
                        style={{
                          padding: '8px 16px',
                          background: '#e74c3c',
                          color: 'white',
                          border: 'none',
                          borderRadius: '20px',
                          cursor: 'pointer',
                          fontSize: '14px',
                          transition: 'all 0.3s ease',
                          boxShadow: '0 2px 8px rgba(231, 76, 60, 0.3)'
                        }}
                        onMouseEnter={(e) => {
                          e.target.style.background = '#c0392b';
                          e.target.style.transform = 'translateY(-1px)';
                        }}
                        onMouseLeave={(e) => {
                          e.target.style.background = '#e74c3c';
                          e.target.style.transform = 'translateY(0)';
                        }}
                      >
                        No, gracias
                      </button>
                    </div>
                  )}

                  {/* Lista de tratamientos */}
                  {message.treatments && message.isFollowUp && (
                    <div style={{ marginTop: '15px' }}>
                      <div style={{ 
                        fontSize: '14px', 
                        fontWeight: '600', 
                        marginBottom: '10px',
                        color: 'white'
                      }}>
                        📋 Tratamientos recomendados:
                      </div>
                      <ul style={{ 
                        color: 'white', 
                        fontSize: '14px', 
                        paddingLeft: '20px',
                        margin: 0,
                        lineHeight: '1.5'
                      }}>
                        {message.treatments.map((treatment, index) => (
                          <li key={index} style={{ 
                            marginBottom: '8px',
                            listStyleType: '•'
                          }}>
                            {treatment}
                          </li>
                        ))}
                      </ul>
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
          </div>
          
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

        {/* Preview de imágenes adjuntas */}
        {attachedImages.length > 0 && (
          <div style={{
            padding: '10px 20px',
            background: '#111827',
            backdropFilter: 'blur(10px)',
            borderRadius: '10px',
          }}>
            <div style={{ 
              display: 'flex', 
              gap: '10px', 
              alignItems: 'center',
              flexWrap: 'wrap'
            }}>
              <span style={{ fontSize: '14px', color: '#666', fontWeight: '500' }}>
                ({attachedImages.length}/3):
              </span>
              {attachedImages.map(image => (
                <div key={image.id} style={{ position: 'relative', display: 'inline-block' }}>
                  <img
                    src={image.url}
                    alt={image.name}
                    style={{
                      width: '50px',
                      height: '50px',
                      borderRadius: '8px',
                      objectFit: 'cover',
                      border: '2px solid #667eea'
                    }}
                  />
                  <button
                    onClick={() => removeAttachedImage(image.id)}
                    style={{
                      position: 'absolute',
                      top: '-5px',
                      right: '-5px',
                      width: '20px',
                      height: '20px',
                      borderRadius: '50%',
                      border: 'none',
                      background: '#e74c3c',
                      color: 'white',
                      cursor: 'pointer',
                      fontSize: '12px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center'
                    }}
                  >
                    ×
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

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
            {/* Botón selector de modo */}
            <button
              onClick={() => setShowModeSelector(true)}
              style={{
                width: '50px',
                height: '50px',
                borderRadius: '50%',
                border: 'none',
                background: 'linear-gradient(135deg, #f39c12 0%, #e74c3c 100%)',
                color: 'white',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '20px',
                boxShadow: '0 4px 15px rgba(0,0,0,0.2)',
                transition: 'all 0.3s ease',
                transform: 'scale(1)'
              }}
              title={`Modo actual: ${selectedMode}`}
            >
              ⚙️
            </button>
            {/* Botón para adjuntar imágenes */}
            <button
              onClick={() => fileInputRef.current?.click()}
              disabled={attachedImages.length >= 3}
              style={{
                width: '50px',
                height: '50px',
                borderRadius: '50%',
                border: 'none',
                background: attachedImages.length >= 3 
                  ? '#bdc3c7' 
                  : 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                color: 'white',
                cursor: attachedImages.length >= 3 ? 'not-allowed' : 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '20px',
                boxShadow: '0 4px 15px rgba(0,0,0,0.2)',
                transition: 'all 0.3s ease',
                transform: 'scale(1)'
              }}
              onMouseEnter={(e) => {
                if (attachedImages.length < 3) {
                  e.target.style.transform = 'scale(1.05)';
                }
              }}
              onMouseLeave={(e) => {
                e.target.style.transform = 'scale(1)';
              }}
              title={`Adjuntar imagen (${attachedImages.length}/3)`}
            >
              📎
            </button>
            
            {/* Input oculto para archivos */}
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              multiple
              onChange={handleFileSelect}
              style={{ display: 'none' }}
            />

            <div style={{ flex: 1, position: 'relative' }}>
              <textarea
                ref={inputRef}
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Escribe tu consulta sobre diagnósticos médicos..."
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
              disabled={(inputValue.trim() === '' && attachedImages.length === 0) || isTyping}
              style={{
                width: '50px',
                height: '50px',
                borderRadius: '50%',
                border: 'none',
                background: (inputValue.trim() === '' && attachedImages.length === 0) || isTyping 
                  ? '#bdc3c7' 
                  : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                cursor: (inputValue.trim() === '' && attachedImages.length === 0) || isTyping ? 'not-allowed' : 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '20px',
                boxShadow: '0 4px 15px rgba(0,0,0,0.2)',
                transition: 'all 0.3s ease',
                transform: 'scale(1)'
              }}
              onMouseEnter={(e) => {
                if ((inputValue.trim() !== '' || attachedImages.length > 0) && !isTyping) {
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
  );
};

export default DiagnosticChat;

const styleSheet = document.createElement('style');
styleSheet.type = 'text/css';
styleSheet.innerText = `
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
`;
if (!document.head.querySelector('style[data-pulse-animation]')) {
  styleSheet.setAttribute('data-pulse-animation', 'true');
  document.head.appendChild(styleSheet);
}