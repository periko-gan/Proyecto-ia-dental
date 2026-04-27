<script setup>
// Vista de reporte diagnostico: combina imagen anotada y panel de hallazgos.

import Header from "@/components/parts/all_pages/Header.vue";
import Aside from "@/components/parts/all_pages/Aside.vue";
import Footer from "@/components/parts/all_pages/Footer.vue";
import ImageAnalyzed from "@/components/parts/diagnostic/ImageAnalyzed.vue";
import DentalProblems from "@/components/parts/diagnostic/DentalProblems.vue";
</script>

<template>

  <div class="bg-surface font-body text-on-surface">
    <!-- TopNavBar -->
<!--    <Header/>-->
    <!-- SideNavBar -->
    <Aside/>
    <!-- Main Content Canvas -->
    <main class="md:ml-64 pt-20 px-8 pb-12 min-h-screen">
      <div class="max-w-7xl mx-auto py-8">
        <!-- Header Section -->
        <div class="flex flex-col md:flex-row justify-between items-start md:items-end mb-10 gap-4">
          <div>
            <div class="text-xs breadcrumbs text-slate-400 mb-2 p-0">
              <ul>
                <li>Analisis</li>
                <li class="text-primary font-semibold">Informe #AX-9021</li>
              </ul>
            </div>
            <h1 class="text-4xl font-headline font-extrabold text-on-surface tracking-tight">Informe diagnóstico de
              IA</h1>
            <p class="text-on-surface-variant mt-1">Paciente: Elena Rodriguez • Fecha de escaneo: 24 oct., 2024</p>
          </div>
          <div class="flex gap-3">
            <button class="btn btn-outline btn-sm border-outline-variant text-on-surface font-bold normal-case">
              <span class="material-symbols-outlined text-sm">share</span> Compartir
            </button>
            <button class="btn btn-primary btn-sm font-bold normal-case">
              <span class="material-symbols-outlined text-sm">picture_as_pdf</span> Descargar informe PDF
            </button>
          </div>
        </div>
        <!-- Stats Overview using DaisyUI Stats -->
        <div class="stats shadow-sm w-full bg-white mb-8 border border-slate-100">
          <div class="stat">
            <div class="stat-figure text-error">
              <span class="material-symbols-outlined text-3xl">priority_high</span>
            </div>
            <div class="stat-title text-slate-500 font-medium">Problemas críticos</div>
            <div class="stat-value text-error">1</div>
            <div class="stat-desc">Requiere acción inmediata</div>
          </div>
          <div class="stat">
            <div class="stat-figure text-warning">
              <span class="material-symbols-outlined text-3xl">visibility</span>
            </div>
            <div class="stat-title text-slate-500 font-medium">Seguimientos</div>
            <div class="stat-value text-warning">1</div>
            <div class="stat-desc">21% de aumento desde el último escaneo</div>
          </div>
          <div class="stat">
            <div class="stat-figure text-success">
              <span class="material-symbols-outlined text-3xl">check_circle</span>
            </div>
            <div class="stat-title text-slate-500 font-medium">Salud general</div>
            <div class="stat-value text-success">88%</div>
            <div class="stat-desc">Por encima del promedio del paciente</div>
          </div>
        </div>
        <!-- Analysis Layout -->
        <div class="grid grid-cols-12 gap-6">
          <!-- Left: Visualizer -->
          <ImageAnalyzed/>
          <!-- Right: Findings Panel -->
          <DentalProblems/>
        </div>
      </div>
    </main>
    <!-- Footer -->
    <Footer/>
  </div>

</template>

<style scoped>
.material-symbols-outlined {
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}

.glass-panel {
  backdrop-filter: blur(12px);
  background: rgba(255, 255, 255, 0.8);
}

.scan-line {
  height: 2px;
  background: linear-gradient(90deg, transparent, #75e7fe, transparent);
  box-shadow: 0 0 15px #75e7fe;
}
</style>
