import { computed } from 'vue'
import { useDiagnosticAnalysis } from '@/composables/useDiagnosticAnalysis'
import { getProblemSeverity } from '@/utils/problemTranslations'

export function useDentalProblems() {
  const { currentAnalysis } = useDiagnosticAnalysis()

  // Detecciones del análisis
  const detections = computed(() => {
    return currentAnalysis.value?.detections || []
  })

  // Total de detecciones
  const totalDetections = computed(() => {
    return detections.value.length
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
    totalDetections,
    detectionStats
  }
}
