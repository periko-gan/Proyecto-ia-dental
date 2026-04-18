<script setup>

</script>

<template>
  <div class="col-span-12 lg:col-span-8 space-y-6">
    <div class="card bg-slate-900 overflow-hidden shadow-xl relative group border-0">
      <!-- AI Visualizer Toolbar -->
      <div class="absolute top-4 left-4 z-10 flex gap-2">
        <div
            class="badge badge-primary gap-2 p-3 font-bold text-[10px] tracking-wider border-none bg-primary/80 backdrop-blur-md">
          <span class="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-pulse"></span>
          AI VISION ACTIVE
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
      <div class="aspect-[16/10] relative flex items-center justify-center">
        <img alt="Clinical dental X-ray" class="w-full h-full object-cover opacity-80"
             src="https://lh3.googleusercontent.com/aida-public/AB6AXuDEXf34UgRNFGqb6Vc9yeb-ySBpcKcd5i3YjYQ00PKVS2O1sYFdg6mu22F-aK2B086Dgha46TK9oNF9PcNO-RsrkikrnqSVFjcICU5fx07pm1y56KDcU_Sgw-B5CuJy8TrVZbC3X-Aff9hxwF9P9qGlGo_RvCNBCeTB-NO5gEpbFZCFa3J3KzvpsIZOtrgirS2XaP_Ck9yzHuA0KkZ8_-ujWOd8I_106X9iGP2zk05gz3kLxz2jdIiGfJsP7EuXMW8QmAdEb2HmDr9H"/>
        <div class="absolute inset-0 pointer-events-none overflow-hidden">
          <div class="scan-line absolute w-full top-1/3"></div>
        </div>
        <!-- Hotspots -->
        <div
            class="absolute top-[42%] left-[32%] w-16 h-16 border-2 border-error rounded-sm ring-4 ring-error/20">
                <span
                    class="absolute -top-7 -left-1 badge badge-error text-white text-[10px] font-bold h-5 rounded-none border-none">CARIES (94%)</span>
        </div>
        <div
            class="absolute top-[55%] left-[65%] w-24 h-12 border-2 border-warning rounded-sm ring-4 ring-warning/20">
                <span
                    class="absolute -top-7 -left-1 badge badge-warning text-white text-[10px] font-bold h-5 rounded-none border-none">PLACA (78%)</span>
        </div>
        <div class="absolute top-[38%] left-[15%] w-12 h-14 border-2 border-success/50 rounded-sm">
                <span
                    class="absolute -top-7 -left-1 badge badge-success text-white text-[10px] font-bold h-5 rounded-none border-none">OPTIMAL</span>
        </div>
      </div>
      <!-- Caption bar -->
      <div class="p-4 bg-white flex flex-wrap justify-between items-center border-t border-slate-100">
        <p class="text-xs text-slate-500 font-medium">Digital Panoramic Radiograph • Layer: Enhanced
          Contrast</p>
        <div class="flex items-center gap-4">
          <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-error"></span><span
              class="text-[10px] font-bold text-slate-500">CRÍTICO</span></div>
          <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-warning"></span><span
              class="text-[10px] font-bold text-slate-500">SEGUIMIENTO</span></div>
          <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-success"></span><span
              class="text-[10px] font-bold text-slate-500">ÓPTIMO</span></div>
        </div>
      </div>
    </div>
    <!-- AI Recommendations - DaisyUI Accordion/Collapse -->
    <div class="space-y-4">
      <div class="flex items-center gap-2 px-2">
        <span class="material-symbols-outlined text-primary" style="font-variation-settings: 'FILL' 1;">auto_awesome</span>
        <h3 class="text-lg font-headline font-extrabold text-primary">AI Treatment Recommendations</h3>
      </div>
      <div class="collapse collapse-arrow bg-white border border-slate-200 shadow-sm rounded-xl">
        <input checked="checked" name="recommendations-accordion" type="radio"/>
        <div class="collapse-title flex items-center gap-4 py-4">
          <div
              class="w-10 h-10 shrink-0 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center">
            <span class="material-symbols-outlined">calendar_month</span>
          </div>
          <div>
            <h4 class="font-bold text-on-surface">Agendar Intervención</h4>
            <p class="text-[11px] text-slate-500">Molar 16 • Prioridad Alta</p>
          </div>
        </div>
        <div class="collapse-content px-16 pb-6">
          <p class="text-sm text-on-surface-variant leading-relaxed">Se recomienda tratamiento para la caries
            detectada en el cuadrante superior izquierdo en un plazo de 14 días para prevenir afectación pulpar.
            El análisis de densidad sugiere una cavidad de grado II.</p>
          <div class="mt-4 flex gap-2">
            <button class="btn btn-xs btn-primary normal-case font-bold">Book Procedure</button>
            <button class="btn btn-xs btn-ghost normal-case font-bold">Patient Notes</button>
          </div>
        </div>
      </div>
      <div class="collapse collapse-arrow bg-white border border-slate-200 shadow-sm rounded-xl">
        <input name="recommendations-accordion" type="radio"/>
        <div class="collapse-title flex items-center gap-4 py-4">
          <div
              class="w-10 h-10 shrink-0 bg-cyan-50 text-cyan-600 rounded-full flex items-center justify-center">
            <span class="material-symbols-outlined">brush</span>
          </div>
          <div>
            <h4 class="font-bold text-on-surface">Ajuste de Higiene</h4>
            <p class="text-[11px] text-slate-500">Zona Cervical • Preventivo</p>
          </div>
        </div>
        <div class="collapse-content px-16 pb-6">
          <p class="text-sm text-on-surface-variant leading-relaxed">Implementar cepillado interdental y uso de
            hilo dental reforzado en zonas de acumulación de placa. Se sugiere profilaxis profesional en la
            próxima visita rutinaria.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>