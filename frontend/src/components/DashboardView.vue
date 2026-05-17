<script setup>

import Aside from '@/components/parts/all_pages/Aside.vue'
import Footer from "@/components/parts/all_pages/Footer.vue";
import AllDiagnostics from '@/components/parts/dashboard/AllDiagnostics.vue';
import HealthScoreHero from "@/components/parts/dashboard/HealthScoreHero.vue";
import LatestDiagnosisSummary from "@/components/parts/dashboard/LatestDiagnosisSummary.vue";
import ProblemTypesChart from "@/components/parts/dashboard/ProblemTypesChart.vue";
</script>

<template>
  <div class="bg-slate-50 font-body text-on-surface">

    <!-- Sidebar -->
    <Aside/>

    <!-- Layout Container -->
    <div class="flex pt-16 min-h-screen">

      <!-- Main Content -->

      <main class="flex-1 md:ml-64 p-6 md:p-10">
        <div class="max-w-6xl mx-auto">

          <div class="flex flex-col md:flex-row justify-between items-start md:items-end mb-10 gap-4">
            <div class="space-y-1">
              <span class="badge badge-secondary badge-outline font-bold tracking-widest text-[10px] h-auto py-1 px-3">RESUMEN CLÍNICO</span>
              <h1 class="text-3xl font-extrabold font-headline tracking-tight text-slate-900">Panel de salud del
                paciente</h1>
            </div>
            <div class="alert bg-white border border-slate-200 shadow-sm w-auto py-2 px-4 gap-3">
              <div class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
              <span class="text-xs font-bold text-slate-600 tracking-wider">MOTOR DE IA ACTIVO</span>
            </div>
          </div>

          <!-- Tabla-->
          <AllDiagnostics/>

          <!-- Bento Grid -->
          <div class="flex justify-evenly gap-2">

            <!-- Health Score Hero -->
            <HealthScoreHero/>

            <!-- Latest Diagnosis -->
            <LatestDiagnosisSummary/>

            <!-- Chart Section -->
            <ProblemTypesChart/>

          </div>
        </div>
      </main>
    </div>

    <!-- Footer -->
    <Footer/>

  </div>
</template>

<style>

.material-symbols-outlined {
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
  vertical-align: middle;
}

</style>
