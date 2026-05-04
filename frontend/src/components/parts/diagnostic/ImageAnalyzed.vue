<script setup>
import { computed, ref } from 'vue'
import { useDiagnosticAnalysis } from '@/composables/useDiagnosticAnalysis'
import { translateProblem, getProblemSeverity, severityConfig, getProblemColor } from '@/utils/problemTranslations'

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

// Detecciones del análisis
const detections = computed(() => {
  return currentAnalysis.value?.detections || []
})

// Estadísticas de detecciones
const detectionStats = computed(() => {
  const stats = {
    critical: 0,
    warning: 0,
    success: 0,
  }

  for (const detection of detections.value) {
    const severity = getProblemSeverity(detection)
    stats[severity]++
  }

  return stats
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

// Obtiene la clase de borde para un hotspot
function getHotspotClass(detection) {
  return 'border-2 ring-4 pointer-events-none'
}

function getHotspotBorderStyle(detection) {
  const color = getProblemColor(detection)
  return {
    borderColor: color,
    boxShadow: `0 0 0 3px ${color}40`,
  }
}
</script>

<template>
  <div class="col-span-12 lg:col-span-8 space-y-6">
    <div class="card bg-slate-900 overflow-hidden shadow-xl relative group border-0">
      <!-- AI Visualizer Toolbar -->
      <div class="absolute top-4 left-4 z-10 flex gap-2">
        <div
            class="badge badge-primary gap-2 p-3 font-bold text-[10px] tracking-wider border-none bg-primary/80 backdrop-blur-md">
          <span class="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-pulse"></span>
          VISIÓN IA ACTIVA
        </div>
      </div>
      <div class="absolute top-4 right-4 z-10 flex gap-2">
        <button class="btn btn-circle btn-sm glass text-white hover:bg-white hover:text-primary">
          <span class="material-symbols-outlined text-lg">zoom_in</span>
        </button>
        <button class="btn btn-circle btn-sm glass text-white hover:bg-white hover:text-primary">
          <span class="material-symbols-outlined text-lg">layers</span>
        </button>
      </div>
      <!-- Main Image with Hotspots -->
      <div class="aspect-16/10 relative flex items-center justify-center bg-slate-950">
        <img
            :alt="`Radiografía - ${currentAnalysis?.fileName || 'Análisis dental'}`"
            :src="imageUrl"
            class="w-full h-full object-cover opacity-80"
            @load="onImageLoad"
        />
        <div class="absolute inset-0 pointer-events-none overflow-hidden">
          <div class="scan-line absolute w-full top-1/3"></div>
        </div>
        <!-- Hotspots dinámicos basados en detecciones -->
        <template v-if="detections.length > 0">
          <div
              v-for="(detection, index) in detections"
              :key="`detection-${index}`"
              :class="getHotspotClass(detection)"
              :style="{ ...calculateHotspotStyle(detection.bboxXyxy), ...getHotspotBorderStyle(detection) }"
              class="absolute border-2 pointer-events-none"
          >
            <span
                :style="{ backgroundColor: getProblemColor(detection) }"
                class="absolute -top-7 -left-1 px-2 py-0.5 text-white text-[10px] font-bold h-auto rounded-none border-none whitespace-nowrap"
            >
              {{ translateProblem(detection) }} {{ formatConfidence(detection.confidence) }}%
            </span>
          </div>
        </template>
        <!-- Fallback si no hay detecciones -->
        <template v-else>
          <div class="absolute inset-0 flex items-center justify-center bg-black/40">
            <p class="text-white text-center text-sm">Cargando análisis...</p>
          </div>
        </template>
      </div>
      <!-- Caption bar -->
      <div class="p-4 bg-white flex flex-wrap justify-between items-center border-t border-slate-100">
        <p class="text-xs text-slate-500 font-medium">
          {{ currentAnalysis?.fileName || 'Radiografía' }} • {{ detections.length }} hallazgo(s) detectado(s)
        </p>
        <div class="flex items-center gap-4">
          <div
              v-if="detectionStats.critical > 0"
              class="flex items-center gap-1.5">
            <span class="w-2.5 h-2.5 rounded-full bg-error"></span>
            <span class="text-[10px] font-bold text-slate-500">{{ detectionStats.critical }} CRÍTICO</span>
          </div>
          <div
              v-if="detectionStats.warning > 0"
              class="flex items-center gap-1.5">
            <span class="w-2.5 h-2.5 rounded-full bg-warning"></span>
            <span class="text-[10px] font-bold text-slate-500">{{ detectionStats.warning }} SEGUIMIENTO</span>
          </div>
          <div
              v-if="detectionStats.success > 0"
              class="flex items-center gap-1.5">
            <span class="w-2.5 h-2.5 rounded-full bg-success"></span>
            <span class="text-[10px] font-bold text-slate-500">{{ detectionStats.success }} ÓPTIMO</span>
          </div>
        </div>
      </div>
    </div>
    <!-- ... resto del componente ... -->
  </div>
</template>

<style scoped>

</style>