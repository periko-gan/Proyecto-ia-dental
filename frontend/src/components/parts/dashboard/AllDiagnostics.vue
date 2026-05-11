<script setup>
import {useRouter} from 'vue-router'
import {useMyAnalyses} from '@/composables/useMyAnalyses.js'
import {useDiagnosticAnalysis} from '@/composables/useDiagnosticAnalysis.js'

const router = useRouter()
const {setAnalysis} = useDiagnosticAnalysis()

const {
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
  countSeverities
} = useMyAnalyses()

function viewDetails(analysis) {
  // Guardamos el análisis en el estado global para que la vista /diagnostic lo lea
  setAnalysis(analysis, {imageSrc: ''})
  router.push('/diagnostic')
}
</script>

<template>
  <div class="mb-10">
    <div class="flex items-center justify-between mb-6">
      <div class="space-y-1">
        <span
            class="badge badge-primary badge-outline font-bold tracking-widest text-[10px] h-auto py-1 px-3">HISTORIAL</span>
        <h2 class="text-2xl font-extrabold font-headline tracking-tight text-slate-900">Exámenes Recientes</h2>
      </div>
    </div>

    <div v-if="loading" class="flex justify-center py-10">
      <span class="loading loading-spinner loading-lg text-primary"></span>
    </div>

    <div v-else-if="error" class="alert alert-error">
      <span class="material-symbols-outlined">error</span>
      <span>{{ error }}</span>
    </div>

    <div v-else-if="analyses.length === 0" class="alert bg-white border border-slate-200">
      <span class="material-symbols-outlined text-slate-400">image_not_supported</span>
      <span class="text-slate-600">No tienes imágenes o análisis previos.</span>
    </div>

    <div v-else class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden relative">
      <!-- Loading overlay for pagination -->
      <div v-if="isPaginating"
           class="absolute inset-0 z-10 bg-white/50 backdrop-blur-sm flex items-center justify-center">
        <span class="loading loading-spinner text-primary"></span>
      </div>

      <div class="overflow-x-auto">
        <table class="table table-zebra w-full">
          <!-- head -->
          <thead class="bg-slate-50 text-slate-500 font-bold border-b border-slate-200">
          <tr>
            <th>Archivo</th>
            <th>Fecha</th>
            <th>Estado</th>
            <th>Hallazgos</th>
            <th class="text-right">Acciones</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="analysis in analyses" :key="analysis.analysisId" class="hover">
            <td>
              <div class="font-bold text-slate-800">{{ analysis.fileName }}</div>
              <div class="text-[10px] text-slate-400 font-mono mt-0.5">{{ analysis.analysisId.split('-')[0] }}</div>
            </td>
            <td class="text-sm text-slate-600">{{ formatDate(analysis.createdAt) }}</td>
            <td>
              <div class="badge badge-sm font-bold text-[10px]" :class="getStatusBadgeClass(analysis.status)">
                {{
                  analysis.status === 'COMPLETED' ? 'COMPLETADO' : analysis.status === 'FAILED' ? 'FALLIDO' : 'PENDIENTE'
                }}
              </div>
            </td>
            <td>
              <div v-if="analysis.status === 'COMPLETED' && analysis.detections" class="flex gap-3">
                <template v-for="(count, severity) in countSeverities(analysis.detections)" :key="severity">
                  <div v-if="count > 0" class="flex items-center gap-1.5"
                       :title="severity === 'critical' ? 'Críticos' : severity === 'warning' ? 'Seguimiento' : 'Óptimos'">
                      <span class="w-2 h-2 rounded-full" :class="{
                        'bg-error shadow-[0_0_8px_rgba(239,68,68,0.5)]': severity === 'critical',
                        'bg-warning shadow-[0_0_8px_rgba(245,158,11,0.5)]': severity === 'warning',
                        'bg-success shadow-[0_0_8px_rgba(34,197,94,0.5)]': severity === 'success'
                      }"></span>
                    <span class="text-xs font-bold text-slate-700">{{ count }}</span>
                  </div>
                </template>
                <div v-if="analysis.detections.length === 0" class="badge badge-ghost text-[10px] font-bold">Sin
                  hallazgos
                </div>
              </div>
              <div v-else class="text-xs text-slate-400">-</div>
            </td>
            <td class="text-right">
              <button
                  class="btn btn-sm btn-ghost text-primary font-bold text-xs"
                  :disabled="analysis.status !== 'COMPLETED'"
                  @click="viewDetails(analysis)"
              >
                Ver detalle
                <span class="material-symbols-outlined text-sm">arrow_forward</span>
              </button>
            </td>
          </tr>
          </tbody>
        </table>
      </div>

      <!-- Paginación -->
      <div class="flex items-center justify-center px-6 py-4 border-t border-slate-200 bg-slate-50">
        <div class="join">
          <button
              class="join-item btn btn-sm bg-white border-slate-200 hover:bg-slate-100 text-slate-600 disabled:bg-slate-50 disabled:text-slate-300"
              :disabled="currentPage === 1 || isPaginating"
              @click="prevPage"
          >
            « Anterior
          </button>
          <div class="join-item btn btn-sm bg-white border-slate-200 pointer-events-none text-slate-600 px-4">
            Pág. <span class="font-bold ml-1">{{ currentPage }}</span>
          </div>
          <button
              class="join-item btn btn-sm bg-white border-slate-200 hover:bg-slate-100 text-slate-600 disabled:bg-slate-50 disabled:text-slate-300"
              :disabled="!hasMoreItems || isPaginating"
              @click="nextPage"
          >
            Siguiente »
          </button>
        </div>
      </div>
    </div>
  </div>
</template>