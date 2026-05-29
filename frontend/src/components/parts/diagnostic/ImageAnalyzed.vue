<script setup>
import {ref} from 'vue'
import {useImageAnalyzed} from '@/composables/useImageAnalyzed'
import {useDentalProblems} from '@/composables/useDentalProblems'
import {getProblemHexColor, translateProblem} from '@/utils/problemTranslations'

// Datos de la imagen y helpers de coordenadas/estilos.
const {
  currentAnalysis,
  imageUrl,
  imageRef,
  imageNaturalWidth,
  imageNaturalHeight,
  calculateHotspotStyle,
  onImageLoad,
  formatConfidence,
} = useImageAnalyzed()

// Filtro y agrupación de detecciones visibles.
const {activeDetections, visibleDetections, detectionStats} = useDentalProblems()

// Estado del modal de zoom.
const isZoomed = ref(false)

// Obtiene la clase de borde para un hotspot
// getProblemBorderClass/getProblemBadgeClass proporcionan las clases CSS por tipo de problema
</script>

<template>
  <div class="col-span-12 lg:col-span-8 space-y-6">
    <div class="card bg-slate-900 overflow-hidden shadow-xl relative group border-0">
      <!-- AI Visualizer Toolbar -->
      <div class="absolute top-4 left-4 z-10 flex gap-2">
        <div
            class="badge badge-primary gap-2 p-3 font-bold text-[10px] tracking-wider border-none bg-primary/80 backdrop-blur-md"
        >
          <span class="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-pulse"></span>
          VISIÓN IA ACTIVA
        </div>
      </div>
      <div class="absolute top-4 right-4 z-10 flex gap-2">
        <button
            @click="isZoomed = true"
            class="btn btn-circle btn-sm glass text-white hover:bg-white hover:text-primary"
        >
          <span class="material-symbols-outlined text-lg">zoom_in</span>
        </button>
      </div>
      <!-- Main Image with Hotspots -->
      <div class="relative w-full h-[60vh] bg-slate-950 overflow-hidden">
        <img
            ref="imageRef"
            :alt="`Radiografía - ${currentAnalysis?.fileName || 'Análisis dental'}`"
            :src="imageUrl"
            class="absolute inset-0 w-full h-full object-fill opacity-80"
            @load="onImageLoad"
        />

        <div class="absolute inset-0 pointer-events-none overflow-hidden z-0">
          <div class="scan-line absolute w-full top-1/3"></div>
        </div>

        <!-- Hotspots dinámicos basados en detecciones -->
        <template v-if="activeDetections.length > 0">
          <div
              v-for="(detection, index) in activeDetections"
              :key="`detection-${index}`"
              class="absolute pointer-events-none border-2 z-10"
              :style="{
              borderColor: getProblemHexColor(detection),
              ...calculateHotspotStyle(detection.bboxXyxy),
            }"
          >
            <span
                :class="[
                'absolute -top-7 -left-1 px-2 py-0.5 text-white text-[10px] font-bold h-auto rounded-none border-none whitespace-nowrap shadow-sm',
              ]"
                :style="{ backgroundColor: getProblemHexColor(detection) }"
            >
              {{ translateProblem(detection) }} {{ formatConfidence(detection.confidence) }}%
            </span>
          </div>
        </template>
        <!-- Fallback si no hay detecciones -->
        <template v-else>
          <div class="absolute inset-0 flex items-center justify-center bg-black/40 z-10">
            <p class="text-white text-center text-sm">
              {{
                visibleDetections.length === 0
                    ? 'No hay resultados visibles con el umbral seleccionado.'
                    : 'Todos los hallazgos visibles están desactivados.'
              }}
            </p>
          </div>
        </template>
      </div>
      <!-- Caption bar -->
      <div
          class="p-4 bg-white flex flex-wrap justify-between items-center border-t border-slate-100"
      >
        <p class="text-xs text-slate-500 font-medium">
          {{ currentAnalysis?.fileName || 'Radiografía' }} •
          {{ activeDetections.length }} hallazgo(s) detectado(s)
        </p>
        <div class="flex items-center gap-4">
          <div v-if="detectionStats.critical.length > 0" class="flex items-center gap-1.5">
            <span class="w-2.5 h-2.5 rounded-full bg-error"></span>
            <span class="text-[10px] font-bold text-slate-500"
            >{{ detectionStats.critical.length }} CRÍTICO</span
            >
          </div>
          <div v-if="detectionStats.warning.length > 0" class="flex items-center gap-1.5">
            <span class="w-2.5 h-2.5 rounded-full bg-warning"></span>
            <span class="text-[10px] font-bold text-slate-500"
            >{{ detectionStats.warning.length }} SEGUIMIENTO</span
            >
          </div>
          <div v-if="detectionStats.success.length > 0" class="flex items-center gap-1.5">
            <span class="w-2.5 h-2.5 rounded-full bg-success"></span>
            <span class="text-[10px] font-bold text-slate-500"
            >{{ detectionStats.success.length }} ÓPTIMO</span
            >
          </div>
        </div>
      </div>
    </div>

    <!-- Zoom Modal -->
    <div
        v-if="isZoomed"
        @click.self="isZoomed = false"
        class="fixed inset-0 z-100 bg-slate-950/95 flex items-center justify-center backdrop-blur-sm p-4"
    >
      <button
          @click="isZoomed = false"
          class="absolute top-6 right-6 btn btn-circle glass text-white hover:bg-error hover:text-white z-110"
      >
        <span class="material-symbols-outlined text-2xl">close</span>
      </button>

      <div
          class="relative w-full max-w-[90vw] max-h-[90vh]"
          :style="{
          aspectRatio:
            imageNaturalWidth && imageNaturalHeight
              ? `${imageNaturalWidth} / ${imageNaturalHeight}`
              : 'auto',
          margin: 'auto',
        }"
      >
        <img
            :alt="`Radiografía Zoom - ${currentAnalysis?.fileName || 'Análisis dental'}`"
            :src="imageUrl"
            class="w-full h-full object-contain pointer-events-none"
        />

        <template v-if="activeDetections.length > 0">
          <div
              v-for="(detection, index) in activeDetections"
              :key="`zoomed-detection-${index}`"
              class="absolute pointer-events-none border-[3px] z-10"
              :style="{
              borderColor: getProblemHexColor(detection),
              ...calculateHotspotStyle(detection.bboxXyxy),
            }"
          >
            <span
                :class="[
                'absolute -top-8 -left-1 px-3 py-1 text-white text-sm font-bold h-auto rounded-none border-none whitespace-nowrap shadow-md',
              ]"
                :style="{ backgroundColor: getProblemHexColor(detection) }"
            >
              {{ translateProblem(detection) }} {{ formatConfidence(detection.confidence) }}%
            </span>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
