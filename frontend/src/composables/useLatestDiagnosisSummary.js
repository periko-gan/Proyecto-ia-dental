import { computed } from 'vue'
import { useMyAnalyses } from '@/composables/useMyAnalyses'
import { useDiagnosticAnalysis } from '@/composables/useDiagnosticAnalysis'
import { getProblemSeverity, translateProblem } from '@/utils/problemTranslations'

// Normaliza confianza 0-1 o 0-100 a porcentaje 0-100.
function normalizeConfidenceToPercent(confidence) {
  const value = Number(confidence)
  if (!Number.isFinite(value)) return null
  return Math.max(0, Math.min(100, value <= 1 ? value * 100 : value))
}

const useLatestDiagnosisSummary = () => {
  const { analyses, loading: analysesLoading, error: analysesError, formatDate } = useMyAnalyses(50)
  const { currentAnalysis } = useDiagnosticAnalysis()

  // Unifica historial + análisis actual para tomar el más reciente.
  const allAnalyses = computed(() => {
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

  // Solo análisis completados para el resumen.
  const completedAnalyses = computed(() => {
    return allAnalyses.value.filter((analysis) => analysis?.status === 'COMPLETED')
  })

  // Selecciona el más reciente por fecha.
  const latestAnalysis = computed(() => {
    return (
      completedAnalyses.value
        .slice()
        .sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime())[0] ??
      null
    )
  })

  const detections = computed(() => latestAnalysis.value?.detections ?? [])

  // Conteo por severidades para texto de resumen.
  const severityCounts = computed(() => {
    const counts = { critical: 0, warning: 0, success: 0 }

    for (const detection of detections.value) {
      const severity = getProblemSeverity(detection)
      if (Object.prototype.hasOwnProperty.call(counts, severity)) {
        counts[severity] += 1
      }
    }

    return counts
  })

  // Hallazgo principal con mayor confianza.
  const mainFinding = computed(() => {
    if (detections.value.length === 0) return 'Sin hallazgos visibles'

    const topDetection = detections.value.slice().sort((a, b) => {
      const confidenceA = normalizeConfidenceToPercent(a?.confidence) ?? 0
      const confidenceB = normalizeConfidenceToPercent(b?.confidence) ?? 0
      return confidenceB - confidenceA
    })[0]

    return translateProblem(topDetection)
  })

  const averageConfidence = computed(() => {
    const confidences = detections.value
      .map((detection) => normalizeConfidenceToPercent(detection?.confidence))
      .filter((value) => value !== null)

    if (confidences.length === 0) return null

    const average = confidences.reduce((sum, value) => sum + value, 0) / confidences.length
    return Math.max(0, Math.min(100, Math.round(average)))
  })

  // Construye el texto visible del resumen.
  const summary = computed(() => {
    if (!latestAnalysis.value) {
      return analysesError.value
        ? `No se pudo cargar el historial: ${analysesError.value}.`
        : 'Todavía no hay un diagnóstico reciente para resumir.'
    }

    if (latestAnalysis.value.status === 'FAILED') {
      return latestAnalysis.value.errorMessage
        ? `El último análisis falló: ${latestAnalysis.value.errorMessage}`
        : 'El último análisis no pudo completarse correctamente.'
    }

    if (latestAnalysis.value.status === 'PENDING') {
      return 'El último análisis sigue en proceso. En cuanto termine, aquí verás el resumen del resultado.'
    }

    if (detections.value.length === 0) {
      return 'El último resultado no muestra hallazgos visibles.'
    }

    const average = averageConfidence.value ?? 0
    const parts = []
    if (severityCounts.value.critical) parts.push(`${severityCounts.value.critical} crítico(s)`)
    if (severityCounts.value.warning) parts.push(`${severityCounts.value.warning} en seguimiento`)
    if (severityCounts.value.success) parts.push(`${severityCounts.value.success} saludables`)

    return `Se detectaron ${detections.value.length} hallazgos. Principal: ${mainFinding.value}. Confianza media: ${average}%. ${parts.length > 0 ? `Distribución: ${parts.join(', ')}.` : ''}`
  })

  const statusLabel = computed(() => {
    if (!latestAnalysis.value) {
      return analysesLoading.value ? 'CARGANDO' : 'SIN RESULTADO'
    }

    if (latestAnalysis.value.status === 'FAILED') return 'FALLIDO'
    if (latestAnalysis.value.status === 'PENDING') return 'EN PROCESO'
    return 'RESUMEN LISTO'
  })

  const statusBadgeClass = computed(() => {
    if (!latestAnalysis.value) return 'badge-ghost text-slate-500'
    if (latestAnalysis.value.status === 'FAILED') return 'badge-error text-white'
    if (latestAnalysis.value.status === 'PENDING') return 'badge-warning text-white'
    return 'badge-secondary text-white'
  })

  const lastUpdate = computed(() => {
    if (!latestAnalysis.value?.createdAt) return 'Sin fecha disponible'
    return formatDate(latestAnalysis.value.createdAt)
  })

  function isHttpUrl(value) {
    return typeof value === 'string' && /^https?:\/\//i.test(value)
  }

  // Genera la URL de uploads según endpoint configurado.
  function buildUploadUrl(filePath) {
    if (!filePath) return null
    if (isHttpUrl(filePath)) return filePath

    const parts = String(filePath).split(/[/\\]/)
    const fileName = parts[parts.length - 1]

    const baseUrl = import.meta.env.VITE_GRAPHQL_ENDPOINT
      ? import.meta.env.VITE_GRAPHQL_ENDPOINT.replace('/graphql', '')
      : 'http://localhost:8000'

    return `${baseUrl}/uploads/${fileName}`
  }

  const latestImageUrl = computed(() => {
    const filePath = latestAnalysis.value?.filePath
    return buildUploadUrl(filePath) || null
  })

  return {
    analysesLoading,
    latestAnalysis,
    statusLabel,
    statusBadgeClass,
    mainFinding,
    averageConfidence,
    summary,
    severityCounts,
    detections,
    lastUpdate,
    latestImageUrl,
  }
}

void useLatestDiagnosisSummary

export { useLatestDiagnosisSummary }
