<script setup>

</script>

<template>
  <div class="col-span-12 lg:col-span-4 space-y-6">
    <div class="card bg-white rounded-xl shadow-sm border border-slate-200 h-full">
      <div class="card-body p-6">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-headline font-extrabold text-on-surface tracking-tight">Hallazgos
            Detectados</h3>
          <div class="badge badge-neutral font-bold text-[10px]">3 TOTAL</div>
        </div>
        <div class="space-y-4">
          <!-- Finding: Critical -->
          <div
              class="card bg-surface-container-low border-l-4 border-error rounded-lg shadow-sm hover:shadow-md transition-all cursor-pointer">
            <div class="p-4">
              <div class="flex justify-between items-start mb-2">
                <div>
                  <h4 class="font-bold text-on-surface text-sm">Caries Detectada</h4>
                  <p class="text-[10px] text-slate-500 font-medium uppercase tracking-widest">Molar 16 •
                    Superior
                    Izq</p>
                </div>
                <div class="badge badge-error badge-sm font-black text-[10px] text-white">CRÍTICO</div>
              </div>
              <div class="mt-4">
                <div class="flex justify-between text-[10px] font-bold text-slate-400 mb-1">
                  <span>Confianza IA</span>
                  <span>94%</span>
                </div>
                <progress class="progress progress-error w-full h-1.5" max="100" value="94"></progress>
              </div>
            </div>
          </div>
          <!-- Finding: Warning -->
          <div
              class="card bg-surface-container-low border-l-4 border-warning rounded-lg shadow-sm hover:shadow-md transition-all cursor-pointer">
            <div class="p-4">
              <div class="flex justify-between items-start mb-2">
                <div>
                  <h4 class="font-bold text-on-surface text-sm">Acumulación de Placa</h4>
                  <p class="text-[10px] text-slate-500 font-medium uppercase tracking-widest">Zona Cervical •
                    General</p>
                </div>
                <div class="badge badge-warning badge-sm font-black text-[10px] text-white">SEGUIMIENTO</div>
              </div>
              <div class="mt-4">
                <div class="flex justify-between text-[10px] font-bold text-slate-400 mb-1">
                  <span>Confianza IA</span>
                  <span>78%</span>
                </div>
                <progress class="progress progress-warning w-full h-1.5" max="100" value="78"></progress>
              </div>
            </div>
          </div>
          <!-- Finding: Optimal -->
          <div
              class="card bg-surface-container-low border-l-4 border-success rounded-lg shadow-sm hover:shadow-md transition-all cursor-pointer">
            <div class="p-4">
              <div class="flex justify-between items-start mb-2">
                <div>
                  <h4 class="font-bold text-on-surface text-sm">Integridad Ósea</h4>
                  <p class="text-[10px] text-slate-500 font-medium uppercase tracking-widest">Densidad
                    Mandibular</p>
                </div>
                <div class="badge badge-success badge-sm font-black text-[10px] text-white">ÓPTIMO</div>
              </div>
              <div class="mt-4">
                <div class="flex justify-between text-[10px] font-bold text-slate-400 mb-1">
                  <span>Confianza IA</span>
                  <span>98%</span>
                </div>
                <progress class="progress progress-success w-full h-1.5" max="100" value="98"></progress>
              </div>
            </div>
          </div>
        </div>
        <!-- Data Transparency Info -->
        <div class="mt-auto pt-10">
          <div class="alert bg-slate-50 border-none p-4 rounded-xl">
            <div>
              <div class="flex items-center gap-2 text-primary mb-1">
                <span class="material-symbols-outlined text-sm">shield</span>
                <span class="text-[10px] font-bold uppercase tracking-widest">Medical Accuracy</span>
              </div>
              <p class="text-[11px] leading-relaxed text-slate-500 italic">
                Este análisis ha sido procesado por el motor Dentis AI v4.2. Los hallazgos presentados son
                sugerencias de diagnóstico y requieren validación profesional.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>