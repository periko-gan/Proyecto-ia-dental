<script setup>
// Vista de reporte diagnostico: combina imagen anotada y panel de hallazgos.

import Aside from '@/components/parts/all_pages/Aside.vue'
import Footer from '@/components/parts/all_pages/Footer.vue'
import ImageAnalyzed from '@/components/parts/diagnostic/ImageAnalyzed.vue'
import DentalProblems from '@/components/parts/diagnostic/DentalProblems.vue'
import {computed} from 'vue'
import {getSession} from '@/services/authService.js'

const loggedUserEmail = computed(() => getSession()?.email || 'Usuario sin sesión')
</script>

<template>
  <div class="bg-surface font-body text-on-surface">
    <!-- SideNavBar -->
    <Aside/>

    <!-- Main Content Canvas -->
    <main class="md:ml-64 pt-20 px-8 pb-12 min-h-screen">
      <div class="max-w-7xl mx-auto py-8">
        <!-- Header Section -->
        <div class="flex flex-col md:flex-row justify-between items-start md:items-end mb-10 gap-4">
          <div>
            <h1 class="text-4xl font-headline font-extrabold text-on-surface tracking-tight">
              Informe diagnóstico de IA
            </h1>
            <p class="text-on-surface-variant mt-1">
              Paciente: {{ loggedUserEmail }} • Fecha de escaneo: 24 oct., 2024
            </p>
          </div>
        </div>
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
  font-variation-settings: 'FILL' 0,
  'wght' 400,
  'GRAD' 0,
  'opsz' 24;
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
