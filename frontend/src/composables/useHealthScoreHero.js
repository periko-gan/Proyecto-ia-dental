import {computed} from 'vue'
import {useMyAnalyses} from '@/composables/useMyAnalyses'
import {useDiagnosticAnalysis} from '@/composables/useDiagnosticAnalysis'
import {getProblemSeverity} from '@/utils/problemTranslations'

function normalizeConfidenceToPercent(confidence) {
  const value = Number(confidence)
  if (!Number.isFinite(value)) return null
  return Math.max(0, Math.min(100, value <= 1 ? value * 100 : value))
}

const useHealthScoreHero = () => {
  const {analyses, loading: analysesLoading, error: analysesError, formatDate} = useMyAnalyses(50)
  const {currentAnalysis} = useDiagnosticAnalysis()

  const heroAnalyses = computed(() => {
    const unique = new Map()

    for (const analysis of analyses.value) {
      if (analysis?.analysisId) {
        unique.set(analysis.analysisId, analysis)
      }
    }

    if (currentAnalysis.value?.analysisId) {
      unique.set(currentAnalysis.value.analysisId, currentAnalysis.value)
    }

    return [...unique.values()]
  })

  const heroCompletedAnalyses = computed(() => {
    return heroAnalyses.value.filter((analysis) => analysis?.status === 'COMPLETED')
  })

  const heroDetections = computed(() => {
    return heroCompletedAnalyses.value.flatMap((analysis) => analysis?.detections ?? [])
  })

  const heroSeverityCounts = computed(() => {
    const counts = {critical: 0, warning: 0, success: 0}

    for (const detection of heroDetections.value) {
      const severity = getProblemSeverity(detection)
      if (Object.prototype.hasOwnProperty.call(counts, severity)) {
        counts[severity] += 1
      }
    }

    return counts
  })

  const heroHealthScore = computed(() => {
    if (heroCompletedAnalyses.value.length === 0) return null

    const confidences = heroDetections.value
        .map((detection) => normalizeConfidenceToPercent(detection?.confidence))
        .filter((value) => value !== null)

    if (confidences.length === 0) return 100

    const average = confidences.reduce((sum, value) => sum + value, 0) / confidences.length
    return Math.max(0, Math.min(100, Math.round(average)))
  })

  const heroHealthLabel = computed(() => {
    if (heroHealthScore.value === null) {
      return analysesLoading.value ? 'Cargando historial' : 'Sin análisis disponible'
    }

    if (heroHealthScore.value >= 90) return 'Excelente'
    if (heroHealthScore.value >= 75) return 'Estable'
    if (heroHealthScore.value >= 60) return 'Atención'
    return 'Revisión prioritaria'
  })

  const heroHealthSummary = computed(() => {
    if (heroCompletedAnalyses.value.length === 0) {
      return analysesError.value
          ? `No se pudo cargar el historial: ${analysesError.value}. Inicia un análisis nuevo para generar el score.`
          : 'Sube una radiografía para calcular un índice de salud dental y compararlo con tu historial.'
    }

    if (heroDetections.value.length === 0) {
      return 'El historial no muestra hallazgos relevantes en los análisis completados.'
    }

    const averageConfidence = heroHealthScore.value ?? 0
    return `La media de acierto de ${heroDetections.value.length} hallazgo(s) es ${averageConfidence}%.`
  })

  const heroLatestAnalysis = computed(() => {
    return heroCompletedAnalyses.value
        .slice()
        .sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime())[0] ?? null
  })

  const heroLastUpdate = computed(() => {
    if (!heroLatestAnalysis.value?.createdAt) return 'Sin fecha disponible'
    return formatDate(heroLatestAnalysis.value.createdAt)
  })

  return {
    analysesLoading,
    heroCompletedAnalyses,
    heroDetections,
    heroSeverityCounts,
    heroHealthScore,
    heroHealthLabel,
    heroHealthSummary,
    heroLatestAnalysis,
    heroLastUpdate,
  }
}

void useHealthScoreHero

export {useHealthScoreHero}

