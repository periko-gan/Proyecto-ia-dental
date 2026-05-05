import { computed, ref, onMounted, onUnmounted, watch } from 'vue'
import { useDiagnosticAnalysis } from '@/composables/useDiagnosticAnalysis'

export function useImageAnalyzed() {
  const { currentAnalysis, currentImage } = useDiagnosticAnalysis()
  const imageNaturalWidth = ref(0)
  const imageNaturalHeight = ref(0)
  
  const imageRef = ref(null)
  const containerWidth = ref(0)
  const containerHeight = ref(0)
  let resizeObserver = null

  onMounted(() => {
    resizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        containerWidth.value = entry.contentRect.width
        containerHeight.value = entry.contentRect.height
      }
    })
    if (imageRef.value) {
      resizeObserver.observe(imageRef.value)
    }
  })

  watch(imageRef, (newEl, oldEl) => {
    if (resizeObserver) {
      if (oldEl) resizeObserver.unobserve(oldEl)
      if (newEl) resizeObserver.observe(newEl)
    }
  })

  onUnmounted(() => {
    if (resizeObserver) {
      resizeObserver.disconnect()
    }
  })

  function isHttpUrl(value) {
    return typeof value === 'string' && /^https?:\/\//i.test(value)
  }

  // Imagen base64 o URL
  const imageUrl = computed(() => {
    if (currentImage.value?.imageSrc) {
      return currentImage.value.imageSrc
    }

    const filePath = currentAnalysis.value?.filePath
    if (filePath) {
      if (isHttpUrl(filePath)) {
        return filePath
      }
      
      // Extraer el nombre de archivo de la ruta absoluta devuelta por el backend
      const parts = String(filePath).split(/[/\\]/)
      const fileName = parts[parts.length - 1]
      
      // Construir la URL del backend (usar VITE_GRAPHQL_ENDPOINT o localhost:8000 por defecto)
      const baseUrl = import.meta.env.VITE_GRAPHQL_ENDPOINT 
        ? import.meta.env.VITE_GRAPHQL_ENDPOINT.replace('/graphql', '') 
        : 'http://localhost:8000'
        
      return `${baseUrl}/uploads/${fileName}`
    }

    return 'https://lh3.googleusercontent.com/aida-public/AB6AXuDEXf34UgRNFGqb6Vc9yeb-ySBpcKcd5i3YjYQ00PKVS2O1sYFdg6mu22F-aK2B086Dgha46TK9oNF9PcNO-RsrkikrnqSVFjcICU5fx07pm1y56KDcU_Sgw-B5CuJy8TrVZbC3X-Aff9hxwF9P9qGlGo_RvCNBCeTB-NO5gEpbFZCFa3J3KzvpsIZOtrgirS2XaP_Ck9yzHuA0KkZ8_-ujWOd8I_106X9iGP2zk05gz3kLxz2jdIiGfJsP7EuXMW8QmAdEb2HmDr9H'
  })

  function parseBboxXyxy(rawBbox) {
    if (Array.isArray(rawBbox)) {
      return rawBbox.map((item) => Number(item))
    }
    if (typeof rawBbox === 'string') {
      try {
        const parsedJson = JSON.parse(rawBbox)
        if (Array.isArray(parsedJson)) {
          return parsedJson.map((item) => Number(item))
        }
      } catch {
        return rawBbox.replaceAll('[', '').replaceAll(']', '').split(',').map((item) => Number(item.trim()))
      }
    }
    return []
  }

  function clampPercent(value) {
    return Math.max(0, Math.min(100, value))
  }

  function toPercentCoordinates(x1, y1, x2, y2) {
    const NW = imageNaturalWidth.value
    const NH = imageNaturalHeight.value

    if (NW > 0 && NH > 0) {
      return {
        left: (x1 / NW) * 100,
        top: (y1 / NH) * 100,
        width: ((x2 - x1) / NW) * 100,
        height: ((y2 - y1) / NH) * 100,
      }
    }

    const maxCoordinate = Math.max(x1, y1, x2, y2)
    if (maxCoordinate <= 1) {
      return { left: x1 * 100, top: y1 * 100, width: (x2 - x1) * 100, height: (y2 - y1) * 100 }
    }

    return { left: 0, top: 0, width: 0, height: 0 }
  }

  function calculateHotspotStyle(bboxXyxy) {
    const parsed = parseBboxXyxy(bboxXyxy)
    if (!parsed || parsed.length < 4 || parsed.some((value) => !Number.isFinite(value))) return {}

    let [x1, y1, x2, y2] = parsed

    // Asegurar orden correcto
    if (x2 < x1) [x1, x2] = [x2, x1]
    if (y2 < y1) [y1, y2] = [y2, y1]

    const percent = toPercentCoordinates(x1, y1, x2, y2)

    const left = clampPercent(percent.left)
    const top = clampPercent(percent.top)
    const width = Math.max(0.8, clampPercent(percent.width))
    const height = Math.max(0.8, clampPercent(percent.height))

    // Evitar que salga del contenedor
    const safeWidth = Math.min(width, 100 - left)
    const safeHeight = Math.min(height, 100 - top)

    return {
      left: `${left}%`,
      top: `${top}%`,
      width: `${safeWidth}%`,
      height: `${safeHeight}%`,
      zIndex: 5,
    }
  }

  function onImageLoad(event) {
    const target = event.target
    imageNaturalWidth.value = target?.naturalWidth || 0
    imageNaturalHeight.value = target?.naturalHeight || 0
  }

  function formatConfidence(confidenceValue) {
    const value = Number(confidenceValue)
    if (!Number.isFinite(value)) return 0
    return Math.round(value <= 1 ? value * 100 : value)
  }

  return {
    currentAnalysis,
    imageUrl,
    imageRef,
    imageNaturalWidth,
    imageNaturalHeight,
    calculateHotspotStyle,
    onImageLoad,
    formatConfidence
  }
}
