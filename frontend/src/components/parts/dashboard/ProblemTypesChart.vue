<script setup>
import {useProblemTypesChart} from '@/composables/useProblemTypesChart'

const {problemCounts, problemPercentages} = useProblemTypesChart()
</script>

<template>
  <div class="flex-1 md:col-span-3 card bg-white border border-slate-200 shadow-sm overflow-hidden">
    <div class="card-body p-4 flex flex-col items-center justify-between">
      <div class="flex sm:flex-row items-start sm:items-center justify-between mb-10 gap-4 w-full">
        <div class="text-center w-full">
          <h3 class="font-headline font-extrabold text-xl text-slate-900">Salud por tipo de problema</h3>
          <p class="text-sm text-slate-500 font-label">Análisis de distribución por IA</p>
        </div>
      </div>

      <!--charts-->
      <div class="flex justify-evenly w-full">
        <div class="flex flex-col items-center gap-6">
          <div class="radial-progress text-caries font-black font-headline text-lg" role="progressbar"
               :style="`--value:${problemPercentages.caries}; --size:6rem; --thickness: 8px;`">{{ problemPercentages.caries }}%
          </div>
          <span class="badge badge-ghost text-[10px] font-bold tracking-widest uppercase py-2 h-auto">Caries ({{ problemCounts.caries }})</span>
        </div>
        <div class="flex flex-col items-center gap-6">
          <div class="radial-progress text-empaste font-black font-headline text-lg" role="progressbar"
               :style="`--value:${problemPercentages.empaste}; --size:6rem; --thickness: 8px;`">{{ problemPercentages.empaste }}%
          </div>
          <span class="badge badge-ghost text-[10px] font-bold tracking-widest uppercase py-2 h-auto">Empaste ({{ problemCounts.empaste }})</span>
        </div>
      </div>
      <div class="flex justify-evenly w-full mt-6">
        <div class="flex flex-col items-center gap-6">
          <div class="radial-progress text-implante font-black font-headline text-lg" role="progressbar"
               :style="`--value:${problemPercentages.implante}; --size:6rem; --thickness: 8px;`">{{ problemPercentages.implante }}%
          </div>
          <span class="badge badge-ghost text-[10px] font-bold tracking-widest uppercase py-2 h-auto">Implante ({{ problemCounts.implante }})</span>
        </div>
        <div class="flex flex-col items-center gap-6">
          <div class="radial-progress text-impactado font-black font-headline text-lg" role="progressbar"
               :style="`--value:${problemPercentages.impactado}; --size:6rem; --thickness: 8px;`">{{ problemPercentages.impactado }}%
          </div>
          <span class="badge badge-ghost text-[10px] font-bold tracking-widest uppercase py-2 h-auto">Diente impactado ({{ problemCounts.impactado }})</span>
        </div>
      </div>
    </div>
  </div>

</template>

<style>

.text-caries {
  color: #EF4444;
}

.text-empaste {
  color: #F59E0B;
}
.text-implante {
  color: #12457EFF;
}
.text-impactado {
  color: #8B5CF6;
}

</style>