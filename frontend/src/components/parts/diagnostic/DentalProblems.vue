<script setup>
import { computed, ref } from 'vue'
import { useDentalProblems } from '@/composables/useDentalProblems'
import { getProblemHexColor, translateProblem } from '@/utils/problemTranslations'

const { totalDetections, detectionStats, toggleDetection, isDetectionEnabled, minimumConfidence } =
  useDentalProblems()

const isSliding = ref(false)

function formatMinimumConfidence(value) {
  return `${Number(value) || 0}%`
}

function getConfidencePercent(confidence) {
  const value = Number(confidence)
  if (!Number.isFinite(value)) return 0
  return Math.max(0, Math.min(100, Math.round(value > 1 ? value : value * 100)))
}

const sliderBubbleLeft = computed(() => {
  const value = Number(minimumConfidence.value) || 0
  return `calc(${value}% - 16px)`
})
</script>

<template>
  <div class="col-span-12 lg:col-span-4 space-y-6">
    <div
      class="card bg-white rounded-xl shadow-sm border border-slate-200 flex flex-col lg:h-[calc(60vh+55px)]"
    >
      <div class="card-body p-6 flex flex-col h-full overflow-hidden">
        <div class="flex items-center justify-between mb-2 shrink-0">
          <h3 class="text-lg font-headline font-extrabold text-on-surface tracking-tight">
            Hallazgos Detectados
          </h3>
          <div class="badge badge-neutral font-bold text-[10px]">{{ totalDetections }} TOTAL</div>
        </div>

        <div
          class="mb-4 shrink-0 rounded-xl border border-cyan-200/70 bg-linear-to-br from-cyan-50 to-blue-50 px-4 py-1.5 shadow-sm"
        >
          <div class="flex items-center justify-between gap-3">
            <div>
              <p class="text-[10px] font-bold uppercase tracking-widest text-cyan-700">
                Umbral de confianza clínica
              </p>
              <!--              <p class="text-xs text-slate-600">Mostrar hallazgos desde este porcentaje mínimo</p>-->
            </div>
            <div class="badge badge-info badge-outline font-bold">
              {{ formatMinimumConfidence(minimumConfidence) }}
            </div>
          </div>

          <div class="relative pt-6">
            <div
              v-show="isSliding"
              class="absolute top-0 rounded-md bg-cyan-700 px-2 py-1 text-[10px] font-bold text-white shadow"
              :style="{ left: sliderBubbleLeft }"
            >
              {{ formatMinimumConfidence(minimumConfidence) }}
            </div>

            <input
              v-model.number="minimumConfidence"
              type="range"
              min="0"
              max="100"
              step="1"
              class="range range-info range-sm"
              @mousedown="isSliding = true"
              @mouseup="isSliding = false"
              @touchstart="isSliding = true"
              @touchend="isSliding = false"
              @focus="isSliding = true"
              @blur="isSliding = false"
            />
          </div>

          <div class="mt-2 flex justify-between text-[10px] font-semibold text-slate-500">
            <span>0%</span>
            <span>25%</span>
            <span>50%</span>
            <span>75%</span>
            <span>100%</span>
          </div>
        </div>

        <div class="space-y-4 overflow-y-auto flex-1 pr-2">
          <!-- Detecciones críticas -->
          <template
            v-for="(detection, index) in detectionStats.critical"
            :key="`critical-${index}`"
          >
            <div
              @click="toggleDetection(detection)"
              class="card bg-surface-container-low border-l-4 rounded-lg shadow-sm hover:shadow-md transition-all cursor-pointer"
              :class="!isDetectionEnabled(detection) ? 'opacity-40 grayscale' : ''"
              :style="{ borderLeftColor: getProblemHexColor(detection) }"
            >
              <div class="p-2">
                <div class="flex justify-between items-start mb-2">
                  <div>
                    <h4 class="font-bold text-on-surface text-sm">
                      {{ translateProblem(detection) }}
                    </h4>
                  </div>
                  <div
                    class="badge badge-sm font-black text-[10px] text-white border-none"
                    :style="{ backgroundColor: getProblemHexColor(detection) }"
                  >
                    CRÍTICO
                  </div>
                </div>
                <div class="mt-4">
                  <div class="flex justify-between text-[10px] font-bold text-slate-400 mb-1">
                    <span>Confianza IA</span>
                    <span>{{ getConfidencePercent(detection.confidence) }}%</span>
                  </div>
                  <progress
                    class="progress w-full h-1.5 [&::-webkit-progress-value]:bg-current [&::-moz-progress-bar]:bg-current"
                    :style="{ color: getProblemHexColor(detection) }"
                    :value="getConfidencePercent(detection.confidence)"
                    max="100"
                  ></progress>
                </div>
              </div>
            </div>
          </template>

          <!-- Detecciones de seguimiento -->
          <template v-for="(detection, index) in detectionStats.warning" :key="`warning-${index}`">
            <div
              @click="toggleDetection(detection)"
              class="card bg-surface-container-low border-l-4 rounded-lg shadow-sm hover:shadow-md transition-all cursor-pointer"
              :class="!isDetectionEnabled(detection) ? 'opacity-40 grayscale' : ''"
              :style="{ borderLeftColor: getProblemHexColor(detection) }"
            >
              <div class="p-4">
                <div class="flex justify-between items-start mb-2">
                  <div>
                    <h4 class="font-bold text-on-surface text-sm">
                      {{ translateProblem(detection) }}
                    </h4>
                  </div>
                  <div
                    class="badge badge-sm font-black text-[10px] text-white border-none"
                    :style="{ backgroundColor: getProblemHexColor(detection) }"
                  >
                    SEGUIMIENTO
                  </div>
                </div>
                <div class="mt-4">
                  <div class="flex justify-between text-[10px] font-bold text-slate-400 mb-1">
                    <span>Confianza IA</span>
                    <span>{{ getConfidencePercent(detection.confidence) }}%</span>
                  </div>
                  <progress
                    class="progress w-full h-1.5 [&::-webkit-progress-value]:bg-current [&::-moz-progress-bar]:bg-current"
                    :style="{ color: getProblemHexColor(detection) }"
                    :value="getConfidencePercent(detection.confidence)"
                    max="100"
                  ></progress>
                </div>
              </div>
            </div>
          </template>

          <!-- Detecciones óptimas -->
          <template v-for="(detection, index) in detectionStats.success" :key="`success-${index}`">
            <div
              @click="toggleDetection(detection)"
              class="card bg-surface-container-low border-l-4 rounded-lg shadow-sm hover:shadow-md transition-all cursor-pointer"
              :class="!isDetectionEnabled(detection) ? 'opacity-40 grayscale' : ''"
              :style="{ borderLeftColor: getProblemHexColor(detection) }"
            >
              <div class="p-4">
                <div class="flex justify-between items-start mb-2">
                  <div>
                    <h4 class="font-bold text-on-surface text-sm">
                      {{ translateProblem(detection) }}
                    </h4>
                  </div>
                  <div
                    class="badge badge-sm font-black text-[10px] text-white border-none"
                    :style="{ backgroundColor: getProblemHexColor(detection) }"
                  >
                    ÓPTIMO
                  </div>
                </div>
                <div class="mt-4">
                  <div class="flex justify-between text-[10px] font-bold text-slate-400 mb-1">
                    <span>Confianza IA</span>
                    <span>{{ getConfidencePercent(detection.confidence) }}%</span>
                  </div>
                  <progress
                    class="progress w-full h-1.5 [&::-webkit-progress-value]:bg-current [&::-moz-progress-bar]:bg-current"
                    :style="{ color: getProblemHexColor(detection) }"
                    :value="getConfidencePercent(detection.confidence)"
                    max="100"
                  ></progress>
                </div>
              </div>
            </div>
          </template>

          <!-- Sin detecciones -->
          <template v-if="totalDetections === 0">
            <div class="alert alert-info">
              <span>No se detectaron hallazgos en el análisis con el umbral seleccionado.</span>
            </div>
          </template>
        </div>
        <!-- Data Transparency Info -->
        <div class="mt-4 pt-4 border-t border-slate-100 shrink-0">
          <div class="alert bg-slate-50 border-none p-4 rounded-xl">
            <div>
              <div class="flex items-center gap-2 text-primary mb-1">
                <span class="material-symbols-outlined text-sm">shield</span>
                <span class="text-[10px] font-bold uppercase tracking-widest"
                  >Precisión médica</span
                >
              </div>
              <p class="text-[11px] leading-relaxed text-slate-500 italic">
                Este análisis ha sido procesado por el motor Dentis AI. Los hallazgos presentados
                son sugerencias de diagnóstico y requieren validación profesional.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Scrollbar personalizado */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
  border-radius: 10px;
}
</style>
