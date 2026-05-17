<script setup>

</script>

<template>
  <div class="flex-1 md:col-span-3 card bg-white border border-slate-200 shadow-sm overflow-hidden">
    <div class="card-body p-4 flex items-center justify-between">
      <div class="flex sm:flex-row items-start sm:items-center justify-between mb-10 gap-4">
        <div class="text-center">
          <h3 class="font-headline font-extrabold text-xl text-slate-900">Salud por zona dental</h3>
          <p class="text-sm text-slate-500 font-label">Análisis de IA de todos los problemas</p>
        </div>
      </div>


      <div class="flex justify-evenly w-full">
        <div class="flex flex-col items-center gap-6">
          <div class="radial-progress text-primary font-black font-headline text-lg" role="progressbar"
               style="--value:85; --size:6rem; --thickness: 8px;">90%
          </div>
          <span class="badge badge-ghost text-[10px] font-bold tracking-widest uppercase py-2 h-auto">Incisivos</span>
        </div>
        <div class="flex flex-col items-center gap-6">
          <div class="radial-progress text-secondary font-black font-headline text-lg" role="progressbar"
               style="--value:80; --size:6rem; --thickness: 8px;">75%
          </div>
          <span class="badge badge-ghost text-[10px] font-bold tracking-widest uppercase py-2 h-auto">Molares</span>
        </div>
      </div>
      <div class="flex justify-evenly w-full">
        <div class="flex flex-col items-center gap-6">
          <div class="radial-progress text-info font-black font-headline text-lg" role="progressbar"
               style="--value:85; --size:6rem; --thickness: 8px;">85%
          </div>
          <span class="badge badge-ghost text-[10px] font-bold tracking-widest uppercase py-2 h-auto">Caninos</span>
        </div>
        <div class="flex flex-col items-center gap-6">
          <div class="radial-progress text-emerald-600 font-black font-headline text-lg" role="progressbar"
               style="--value:80; --size:6rem; --thickness: 8px;">80%
          </div>
          <span class="badge badge-ghost text-[10px] font-bold tracking-widest uppercase py-2 h-auto">Premolares</span>
        </div>
      </div>
    </div>
  </div>

</template>

