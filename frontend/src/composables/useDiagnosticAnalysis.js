import { ref } from 'vue'

/**
 * Composable para manejar los datos del análisis diagnosticado
 */
const currentAnalysis = ref(null)
const currentImage = ref(null)

const DIAGNOSTIC_STORAGE_KEY = 'diagnostic.analysis.v1'

function revokeCurrentImageUrl() {
  const imageSrc = currentImage.value?.imageSrc
  if (imageSrc?.startsWith('blob:')) {
    URL.revokeObjectURL(imageSrc)
  }
}

function persistDiagnosticState() {
  try {
    if (!currentAnalysis.value || !currentImage.value) {
      sessionStorage.removeItem(DIAGNOSTIC_STORAGE_KEY)
      return
    }

    const payload = {
      analysis: currentAnalysis.value,
      image: {
        fileName: currentImage.value.fileName || '',
        mimeType: currentImage.value.mimeType || 'image/jpeg',
        // Solo persistimos data URL (serializable) y evitamos blob/file.
        imageSrc: currentImage.value.imageSrc?.startsWith('data:') ? currentImage.value.imageSrc : '',
      },
    }

    sessionStorage.setItem(DIAGNOSTIC_STORAGE_KEY, JSON.stringify(payload))
  } catch (error) {
    console.warn('No se pudo persistir el diagnóstico en sessionStorage:', error)
  }
}

function hydrateDiagnosticState() {
  try {
    const raw = sessionStorage.getItem(DIAGNOSTIC_STORAGE_KEY)
    if (!raw) return

    const parsed = JSON.parse(raw)
    if (!parsed?.analysis) return

    currentAnalysis.value = parsed.analysis
    currentImage.value = parsed.image || null
  } catch (error) {
    console.warn('No se pudo restaurar el diagnóstico desde sessionStorage:', error)
    sessionStorage.removeItem(DIAGNOSTIC_STORAGE_KEY)
  }
}

hydrateDiagnosticState()

export function useDiagnosticAnalysis() {
  /**
   * Establece el análisis actual y la imagen
   */
  function setAnalysis(analysis, imageData) {
    revokeCurrentImageUrl()

    let imageSrc = imageData?.imageSrc || ''
    if (!imageSrc && imageData?.file instanceof File) {
      imageSrc = URL.createObjectURL(imageData.file)
    }

    currentAnalysis.value = analysis
    currentImage.value = {
      ...imageData,
      imageSrc,
    }
    persistDiagnosticState()
    console.log('📊 Análisis diagnosticado:', analysis)
    console.log('🖼️ Imagen: ', currentImage.value)
  }

  /**
   * Obtiene el análisis actual
   */
  function getAnalysis() {
    return currentAnalysis.value
  }

  /**
   * Obtiene la imagen actual
   */
  function getImage() {
    return currentImage.value
  }

  /**
   * Limpia el análisis
   */
  function clearAnalysis() {
    revokeCurrentImageUrl()
    currentAnalysis.value = null
    currentImage.value = null
    sessionStorage.removeItem(DIAGNOSTIC_STORAGE_KEY)
  }

  return {
    currentAnalysis,
    currentImage,
    setAnalysis,
    getAnalysis,
    getImage,
    clearAnalysis,
  }
}

