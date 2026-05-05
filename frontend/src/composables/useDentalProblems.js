import { computed, ref, watch } from 'vue'
import { useDiagnosticAnalysis } from '@/composables/useDiagnosticAnalysis'
import { getProblemSeverity } from '@/utils/problemTranslations'

const disabledDetections = ref(new Set())
const { currentAnalysis } = useDiagnosticAnalysis()

watch(currentAnalysis, () => {
  disabledDetections.value = new Set()
})

export function useDentalProblems() {
  // Detecciones del análisis
  const detections = computed(() => {
    return currentAnalysis.value?.detections || []
  })

  // Total de detecciones
  const totalDetections = computed(() => {
    return detections.value.length
  })

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
    return detections.value.filter(d => isDetectionEnabled(d))
  })

  // Estadísticas por severidad
  const detectionStats = computed(() => {
    const stats = {
      critical: [],
      warning: [],
      success: [],
    }

    for (const detection of detections.value) {
      const severity = getProblemSeverity(detection)
      stats[severity].push(detection)
    }

    return stats
  })

  return {
    detections,
    activeDetections,
    totalDetections,
    detectionStats,
    toggleDetection,
    isDetectionEnabled
  }
}
