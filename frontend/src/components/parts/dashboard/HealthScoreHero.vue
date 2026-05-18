<script setup>
import { useHealthScoreHero } from '@/composables/useHealthScoreHero'

const {
  analysesLoading,
  heroCompletedAnalyses,
  heroDetections,
  heroSeverityCounts,
  heroHealthScore,
  heroHealthLabel,
  heroHealthSummary,
  heroLatestAnalysis,
  heroLastUpdate,
} = useHealthScoreHero()
</script>

<template>
  <div class="flex-1 md:col-span-4 flex justify-around">
    <div
      class="card bg-primary text-primary-content shadow-xl overflow-hidden group text-left w-full border-0"
    >
      <div
        class="absolute top-[-10%] right-[-10%] w-48 h-48 bg-white/10 rounded-full blur-3xl transition-transform group-hover:scale-110"
      ></div>
      <div class="card-body relative z-10 p-8">
        <div class="flex items-start justify-between gap-4">
          <div>
            <h2 class="card-title font-headline text-blue-100 opacity-80 text-lg">
              Índice de salud dental
            </h2>
            <p class="text-[10px] text-blue-200 uppercase tracking-widest font-label -mt-2">
              {{
                heroLatestAnalysis
                  ? `Actualizado ${heroLastUpdate}`
                  : analysesLoading
                    ? 'Cargando historial'
                    : 'Sin análisis disponible'
              }}
            </p>
          </div>
          <div class="badge badge-secondary font-black text-[10px] py-3 px-3">
            {{ heroHealthLabel }}
          </div>
        </div>
        <div class="py-5 flex items-baseline gap-2">
          <span class="text-7xl font-black font-headline">{{ heroHealthScore ?? '--' }}</span>
          <span class="text-2xl font-bold opacity-60">/100</span>
        </div>
        <div class="space-y-4">
          <progress
            class="progress progress-secondary w-full"
            max="100"
            :value="heroHealthScore ?? 0"
          ></progress>
          <!-- <p class="text-sm font-medium leading-relaxed text-blue-50">{{ heroHealthSummary }}</p>-->
          <div
            v-if="heroCompletedAnalyses.length > 0"
            class="flex flex-col flex-wrap gap-4 text-[10px] font-bold uppercase tracking-wider mt-4"
          >
            <span
              class="badge badge-outline inline-flex whitespace-nowrap w-max max-w-full border-white/20 text-white/90"
              >{{ heroCompletedAnalyses.length }} radiografiàs analizadas</span
            >
            <span
              class="badge badge-outline inline-flex whitespace-nowrap w-max max-w-full border-white/20 text-white/90"
              >{{ heroDetections.length }} problemas hallados</span
            >
            <span
              class="badge badge-outline inline-flex whitespace-nowrap w-max max-w-full border-white/20 text-white/90"
              >Media de aciertos del {{ heroHealthScore ?? 0 }}%</span
            >
            <span
              v-if="heroSeverityCounts.critical > 0"
              class="badge badge-outline inline-flex whitespace-nowrap w-max max-w-full border-white/20 text-white/90"
              >{{ heroSeverityCounts.critical }} críticos</span
            >
            <span
              v-if="heroSeverityCounts.warning > 0"
              class="badge badge-outline inline-flex whitespace-nowrap w-max max-w-full border-white/20 text-white/90"
              >{{ heroSeverityCounts.warning }} problemas en seguimiento</span
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
