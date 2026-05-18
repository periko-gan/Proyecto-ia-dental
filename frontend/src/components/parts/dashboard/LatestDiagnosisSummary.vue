<script setup>
import { useLatestDiagnosisSummary } from '@/composables/useLatestDiagnosisSummary'

const {
  analysesLoading,
  latestAnalysis,
  statusLabel,
  statusBadgeClass,
  mainFinding,
  averageConfidence,
  summary,
  detections,
  lastUpdate,
  latestImageUrl,
} = useLatestDiagnosisSummary()
</script>

<template>
  <div class="flex-1 md:col-span-5 flex justify-around">
    <div class="card bg-white border border-slate-200 shadow-sm w-full">
      <div class="card-body p-6">
        <div class="flex justify-between items-start mb-3 gap-4">
          <div>
            <h3 class="font-headline font-extrabold text-slate-900 text-lg">Último diagnóstico</h3>
            <p class="text-[10px] text-slate-500 font-label tracking-wide uppercase">
              {{
                latestAnalysis
                  ? `${lastUpdate}`
                  : analysesLoading
                    ? 'Cargando historial'
                    : 'Sin diagnóstico reciente'
              }}
            </p>
          </div>
          <div class="badge font-black text-[8px] py-3 px-3" :class="statusBadgeClass">
            {{ statusLabel }}
          </div>
        </div>

        <div v-if="latestAnalysis" class="space-y-5">
          <div class="flex items-start gap-4">
            <div class="w-full sm:w-32">
              <div
                class="relative group w-full aspect-square rounded-xl overflow-hidden border border-slate-100"
              >
                <img
                  v-if="latestImageUrl"
                  :src="latestImageUrl"
                  :alt="`Radiografía - ${latestAnalysis.fileName}`"
                  class="w-full h-full object-cover"
                />
                <div
                  v-else
                  class="w-full h-full bg-slate-100 flex items-center justify-center text-slate-400"
                >
                  No hay imagen
                </div>
              </div>
            </div>

            <div class="flex-1">
              <div class="rounded-xl border border-slate-100 bg-slate-50 p-4 space-y-2">
                <p class="text-[10px] font-black text-slate-400 uppercase tracking-tighter">
                  RESUMEN DEL ÚLTIMO RESULTADO
                </p>
                <p class="text-slate-700 leading-relaxed">{{ summary }}</p>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-center">
            <div class="rounded-xl border border-slate-100 bg-white p-3">
              <p class="text-[10px] font-black text-slate-400 uppercase tracking-tighter">
                Hallazgos
              </p>
              <p class="mt-1 text-2xl font-black text-slate-900">{{ detections.length }}</p>
            </div>
            <div class="rounded-xl border border-slate-100 bg-white p-3">
              <p class="text-[10px] font-black text-slate-400 uppercase tracking-tighter">
                Confianza media
              </p>
              <p class="mt-1 text-2xl font-black text-slate-900">
                {{ averageConfidence ?? '--' }}%
              </p>
            </div>
          </div>

          <div class="space-y-1">
            <p class="text-[10px] font-black text-slate-400 uppercase tracking-tighter">
              Hallazgo principal
            </p>
            <p class="text-base font-bold text-slate-900 leading-tight">{{ mainFinding }}</p>
            <!--            <p class="text-xs text-slate-500">{{ latestAnalysis.fileName }}</p>-->
            <!--            <p class="text-xs text-slate-500">{{ lastUpdate }}</p>-->
          </div>
        </div>

        <div
          v-else
          class="rounded-xl border border-dashed border-slate-200 bg-slate-50 p-5 text-slate-600"
        >
          <p class="font-semibold">Aún no hay un diagnóstico reciente para resumir.</p>
          <p class="text-sm mt-1">
            Sube una radiografía o fotografía para ver aquí el último resultado analizado.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
