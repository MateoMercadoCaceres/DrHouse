const API_BASE_URL_IMAGE = 'http://localhost:2342/api/v1';
const STATIC_BASE_URL = 'http://localhost:2342/static/images';

/**
 * Service para generar imágenes de medicinas
 * @param {string} medicineName - Nombre de la medicina
 * @param {string} description - Descripción opcional de la medicina
 * @returns {Promise<{success: boolean, imageUrl?: string, error?: string}>} - Respuesta procesada
 */
export const createImageService = async (medicineName, description = '') => {
  try {
    const body = {
      medicine_name: medicineName.trim()
    };
    
    if (description && description.trim()) {
      body.description = description.trim();
    }

    const response = await fetch(
      `${API_BASE_URL_IMAGE}/medicine/generate-image`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      }
    );

    if (!response.ok) {
      throw new Error(`Error generando imagen: ${response.status} - ${response.statusText}`);
    }

    const data = await response.json();
    
    // Asumiendo que la respuesta incluye el nombre del archivo o path de la imagen
    // Ajusta según la estructura real de tu API
    const imagePath = data.image_path || data.filename || `${medicineName.toLowerCase().replace(/\s+/g, '_')}_package.png`;
    const imageUrl = `${STATIC_BASE_URL}/${imagePath}`;

    return {
      success: true,
      imageUrl: imageUrl,
      data: data
    };

  } catch (error) {
    console.error('Error en createImageService:', error);
    return {
      success: false,
      error: error.message || 'Error desconocido al generar la imagen'
    };
  }
};

/**
 * Función auxiliar para verificar si una imagen existe
 * @param {string} imageUrl - URL de la imagen
 * @returns {Promise<boolean>} - True si la imagen existe
 */
export const checkImageExists = async (imageUrl) => {
  try {
    const response = await fetch(imageUrl, { method: 'HEAD' });
    return response.ok;
  } catch (error) {
    console.error('Error verificando imagen:', error);
    return false;
  }
};

/**
 * Función para extraer nombre de medicamento de un texto
 * @param {string} text - Texto del usuario
 * @returns {string|null} - Nombre del medicamento extraído o null
 */
export const extractMedicineName = (text) => {
  console.log('🔍 Analizando texto:', text);
  const lowerText = text.toLowerCase();
  console.log('📄 Texto en minúsculas:', lowerText);
  
  // Palabras clave que indican solicitud de imagen
  const imageKeywords = ['imagen', 'foto', 'picture', 'mostrar', 'ver', 'generar'];
  const hasImageKeyword = imageKeywords.some(keyword => lowerText.includes(keyword));
  console.log('🔑 ¿Tiene palabra clave de imagen?', hasImageKeyword);
  
  if (!hasImageKeyword) {
    console.log('❌ No tiene palabras clave de imagen');
    return null;
  }
  
  // Lista de medicamentos comunes (puedes expandir esta lista)
  const commonMedicines = [
    'paracetamol', 'ibuprofeno', 'aspirina', 'omeprazol', 'amoxicilina',
    'diclofenaco', 'loratadina', 'simvastatina', 'atorvastatina', 'metformina',
    'losartan', 'amlodipino', 'enalapril', 'furosemida', 'prednisona',
    'acetaminofen', 'advil', 'tylenol', 'motrin'
  ];
  
  // Buscar medicamento en el texto
  for (const medicine of commonMedicines) {
    if (lowerText.includes(medicine)) {
      console.log('✅ Medicamento encontrado en lista:', medicine);
      return medicine;
    }
  }
  console.log('🔍 No encontrado en lista común, probando patrones...');
  
  // Patrones mejorados para extraer nombres después de palabras clave
  const patterns = [
    // "mostrar imagen de paracetamol"
    /(?:imagen|foto|picture|mostrar|ver|generar)(?:\s+(?:de|del|de la|para|el|la)?\s+)([a-záéíóúñü]+)/i,
    // "paracetamol imagen"
    /([a-záéíóúñü]+)(?:\s+(?:imagen|foto|picture))/i,
    // "imagen paracetamol"
    /(?:imagen|foto|picture)\s+([a-záéíóúñü]+)/i,
    // Cualquier palabra después de "de"
    /\bde\s+([a-záéíóúñü]+)/i
  ];
  
  for (let i = 0; i < patterns.length; i++) {
    const pattern = patterns[i];
    const match = text.match(pattern);
    console.log(`🎯 Patrón ${i + 1}:`, pattern, '-> Match:', match);
    
    if (match && match[1]) {
      const extracted = match[1].trim();
      console.log('📝 Texto extraído:', extracted);
      
      // Filtrar palabras muy cortas o muy largas
      if (extracted.length > 2 && extracted.length < 30) {
        console.log('✅ Medicamento extraído válido:', extracted);
        return extracted;
      } else {
        console.log('❌ Texto extraído no válido (muy corto/largo):', extracted);
      }
    }
  }
  
  console.log('❌ No se pudo extraer medicamento');
  return null;
};