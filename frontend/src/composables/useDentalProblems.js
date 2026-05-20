import { computed, ref, watch } from 'vue'
import { useDiagnosticAnalysis } from '@/composables/useDiagnosticAnalysis'
import { getProblemSeverity } from '@/utils/problemTranslations'

const CONFIDENCE_STORAGE_KEY = 'dentalProblems.minimumConfidence.v1'

const disabledDetections = ref(new Set())
const minimumConfidence = ref(loadStoredMinimumConfidence())
const { currentAnalysis } = useDiagnosticAnalysis()

// Reinicia selecciones cuando cambia el análisis actual.
watch(currentAnalysis, () => {
  disabledDetections.value = new Set()
})

// Persiste el umbral de confianza en localStorage.
watch(minimumConfidence, (value) => {
  const normalized = clampPercent(value)
  if (normalized !== value) {
    minimumConfidence.value = normalized
    return
  }

  try {
    localStorage.setItem(CONFIDENCE_STORAGE_KEY, String(normalized))
  } catch {
    // Si localStorage falla, el filtro sigue funcionando en memoria.
  }
})

function clampPercent(value) {
  const numeric = Number(value)
  if (!Number.isFinite(numeric)) return 0
  return Math.min(100, Math.max(0, Math.round(numeric)))
}

function loadStoredMinimumConfidence() {
  try {
    const stored = localStorage.getItem(CONFIDENCE_STORAGE_KEY)
    if (stored == null) return 0
    return clampPercent(stored)
  } catch {
    return 0
  }
}

// Normaliza confianza 0-1 o 0-100 a porcentaje 0-100.
function normalizeConfidence(confidence) {
  const value = Number(confidence)
  if (!Number.isFinite(value)) return 0
  return value > 1 ? value : value * 100
}

export function useDentalProblems() {
  // Detecciones del análisis
  const detections = computed(() => {
    return currentAnalysis.value?.detections || []
  })

  const isDetectionVisible = (detection) => {
    if (!detection) return false
    return normalizeConfidence(detection.confidence) >= minimumConfidence.value
  }

  // Detecciones visibles según el umbral seleccionado
  const visibleDetections = computed(() => {
    return detections.value.filter((detection) => isDetectionVisible(detection))
  })

  // Total de detecciones visibles
  const totalDetections = computed(() => {
    return visibleDetections.value.length
  })

  // Activa o desactiva manualmente un hallazgo en la UI.
  const toggleDetection = (detection) => {
    const newSet = new Set(disabledDetections.value)
    if (newSet.has(detection)) {
      newSet.delete(detection)
    } else {
      newSet.add(detection)
    }
    disabledDetections.value = newSet
  }

  const isDetectionEnabled = (detection) => {
    return !disabledDetections.value.has(detection)
  }

  // Active detections only (for ImageAnalyzed)
  const activeDetections = computed(() => {
    return visibleDetections.value.filter((d) => isDetectionEnabled(d))
  })

  // Estadísticas por severidad
  const detectionStats = computed(() => {
    const stats = {
      critical: [],
      warning: [],
      success: [],
    }

    for (const detection of visibleDetections.value) {
      const severity = getProblemSeverity(detection)
      stats[severity].push(detection)
    }

    return stats
  })

  return {
    detections,
    visibleDetections,
    activeDetections,
    totalDetections,
    detectionStats,
    minimumConfidence,
    toggleDetection,
    isDetectionEnabled,
  }
}
