import { computed, ref } from 'vue'
import { useDiagnosticAnalysis } from '@/composables/useDiagnosticAnalysis'

export function useImageAnalyzed() {
  const { currentAnalysis, currentImage } = useDiagnosticAnalysis()
  const imageNaturalWidth = ref(0)
  const imageNaturalHeight = ref(0)

  function isHttpUrl(value) {
    return typeof value === 'string' && /^https?:\/\//i.test(value)
  }

  // Imagen base64 o URL
  const imageUrl = computed(() => {
    if (currentImage.value?.imageSrc) {
      return currentImage.value.imageSrc
    }

    // filePath del backend suele ser ruta local de servidor y no se puede abrir desde navegador.
    if (isHttpUrl(currentAnalysis.value?.filePath)) {
      return currentAnalysis.value.filePath
    }

    return 'https://lh3.googleusercontent.com/aida-public/AB6AXuDEXf34UgRNFGqb6Vc9yeb-ySBpcKcd5i3YjYQ00PKVS2O1sYFdg6mu22F-aK2B086Dgha46TK9oNF9PcNO-RsrkikrnqSVFjcICU5fx07pm1y56KDcU_Sgw-B5CuJy8TrVZbC3X-Aff9hxwF9P9qGlGo_RvCNBCeTB-NO5gEpbFZCFa3J3KzvpsIZOtrgirS2XaP_Ck9yzHuA0KkZ8_-ujWOd8I_106X9iGP2zk05gz3kLxz2jdIiGfJsP7EuXMW8QmAdEb2HmDr9H'
  })

  // Mapea coordenadas bboxXyxy (x1, y1, x2, y2) a estilos CSS
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
        return rawBbox
          .replaceAll('[', '')
          .replaceAll(']', '')
          .split(',')
          .map((item) => Number(item.trim()))
      }
    }

    return []
  }

  function clampPercent(value) {
    return Math.max(0, Math.min(100, value))
  }

  function toPercentCoordinates(x1, y1, x2, y2) {
    const maxCoordinate = Math.max(x1, y1, x2, y2)

    // 0..1 normalizado
    if (maxCoordinate <= 1) {
      return {
        left: x1 * 100,
        top: y1 * 100,
        width: (x2 - x1) * 100,
        height: (y2 - y1) * 100,
      }
    }

    // Ya en porcentaje
    if (x2 <= 100 && y2 <= 100) {
      return {
        left: x1,
        top: y1,
        width: x2 - x1,
        height: y2 - y1,
      }
    }

    // En píxeles: convertir usando tamaño real de imagen
    if (imageNaturalWidth.value > 0 && imageNaturalHeight.value > 0) {
      return {
        left: (x1 / imageNaturalWidth.value) * 100,
        top: (y1 / imageNaturalHeight.value) * 100,
        width: ((x2 - x1) / imageNaturalWidth.value) * 100,
        height: ((y2 - y1) / imageNaturalHeight.value) * 100,
      }
    }

    // Fallback: escala por máximo coordenado para que sea visible
    return {
      left: (x1 / maxCoordinate) * 100,
      top: (y1 / maxCoordinate) * 100,
      width: ((x2 - x1) / maxCoordinate) * 100,
      height: ((y2 - y1) / maxCoordinate) * 100,
    }
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
    calculateHotspotStyle,
    onImageLoad,
    formatConfidence
  }
}
