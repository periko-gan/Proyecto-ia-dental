import { onMounted, ref } from 'vue'
import { fetchMyAnalyses } from '@/services/analysisService'
import { getProblemSeverity } from '@/utils/problemTranslations'

export function useMyAnalyses(itemsPerPage = 5) {
  const analyses = ref([])
  const loading = ref(true)
  const isPaginating = ref(false)
  const error = ref(null)

  const currentPage = ref(1)
  const hasMoreItems = ref(false)

  // Carga una página del historial con control de estados.
  async function loadPage(page) {
    if (page < 1) return

    if (page === 1 && analyses.value.length === 0) {
      loading.value = true
    } else {
      isPaginating.value = true
    }

    error.value = null

    try {
      const offset = (page - 1) * itemsPerPage
      // Solicitamos itemsPerPage + 1 para saber si hay una página siguiente
      const data = await fetchMyAnalyses(itemsPerPage + 1, offset)

      if (data.length > itemsPerPage) {
        hasMoreItems.value = true
        analyses.value = data.slice(0, itemsPerPage)
      } else {
        hasMoreItems.value = false
        analyses.value = data
      }
      currentPage.value = page
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
      isPaginating.value = false
    }
  }

  onMounted(() => {
    loadPage(1)
  })

  function nextPage() {
    if (hasMoreItems.value && !isPaginating.value) {
      loadPage(currentPage.value + 1)
    }
  }

  function prevPage() {
    if (currentPage.value > 1 && !isPaginating.value) {
      loadPage(currentPage.value - 1)
    }
  }

  // Formatea fechas del backend en formato local.
  function formatDate(dateString) {
    if (!dateString) return ''
    const date = new Date(dateString)
    return new Intl.DateTimeFormat('es-ES', {
      dateStyle: 'medium',
      timeStyle: 'short',
    }).format(date)
  }

  // Mapea estados de análisis a clases de badge.
  function getStatusBadgeClass(status) {
    if (status === 'COMPLETED') return 'badge-success text-white'
    if (status === 'FAILED') return 'badge-error text-white'
    return 'badge-warning text-white'
  }

  // Cuenta severidades para UI de resumen.
  function countSeverities(detections) {
    if (!detections) return { critical: 0, warning: 0, success: 0 }
    const counts = { critical: 0, warning: 0, success: 0 }
    for (const det of detections) {
      counts[getProblemSeverity(det)]++
    }
    return counts
  }

  return {
    analyses,
    loading,
    isPaginating,
    error,
    currentPage,
    hasMoreItems,
    nextPage,
    prevPage,
    formatDate,
    getStatusBadgeClass,
    countSeverities,
  }
}
