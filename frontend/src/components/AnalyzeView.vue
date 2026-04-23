<script setup>
// Vista de analisis: integra layout comun y el módulo de carga/validación de imagenes.

import Header from '@/components/parts/all_pages/Header.vue'
import Aside from "@/components/parts/all_pages/Aside.vue";
import Footer from "@/components/parts/all_pages/Footer.vue";
import UploadImages from "@/components/parts/upload_images/UploadImages.vue";
</script>

<template>

  <div class="bg-surface font-body text-on-surface antialiased">
    <!-- TopNavBar (Shared Component) -->
    <Header/>

    <!-- Sidebar -->
    <Aside/>

    <!-- Main Content Canvas -->
    <main class="pt-20 md:pl-64 min-h-screen flex flex-col lg:flex-row gap-0">
      <!-- Left Analysis Workspace -->
      <section class="flex-1 p-6 md:p-10 flex flex-col items-center">
        <div class="w-full max-w-4xl space-y-8">
          <div class="flex justify-between items-end">
            <div>
              <h3 class="font-headline text-3xl font-extrabold text-primary mb-2">Análisis clínico de imagen</h3>
              <p class="text-on-surface-variant font-medium">Sube fotografías intraorales o radiografías para apoyo
                diagnóstico con IA.</p>
            </div>
            <div class="flex gap-3">
              <div
                  class="badge badge-secondary badge-outline gap-2 p-3 font-bold uppercase tracking-widest text-[10px]">
                <span class="w-2 h-2 bg-secondary rounded-full animate-pulse"></span>
                Sistema de IA listo
              </div>
            </div>
          </div>
          <!-- Drag & Drop Zone -->
          <div class="relative group">
            <UploadImages/>
          </div>
          <!-- Bento Grid Tools -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="card bg-surface-container-low border-l-4 border-secondary shadow-sm">
              <div class="card-body p-5 flex-row items-center gap-4">
                <div class="p-2 bg-secondary/10 rounded-lg">
                  <span class="material-symbols-outlined text-secondary" data-icon="auto_awesome">auto_awesome</span>
                </div>
                <div>
                  <p class="text-xs font-bold text-on-surface">Escaneo de precisión</p>
                  <p class="text-[10px] text-on-surface-variant">Detección avanzada de caries activada</p>
                </div>
              </div>
            </div>
            <div class="card bg-surface-container-low shadow-sm">
              <div class="card-body p-5 flex-row items-center gap-4">
                <div class="p-2 bg-slate-200 rounded-lg">
                  <span class="material-symbols-outlined text-slate-600" data-icon="history">history</span>
                </div>
                <div>
                  <p class="text-xs font-bold text-on-surface">Historial del paciente</p>
                  <p class="text-[10px] text-on-surface-variant">Modo de comparación disponible</p>
                </div>
              </div>
            </div>
            <div class="card bg-surface-container-low shadow-sm">
              <div class="card-body p-5 flex-row items-center gap-4">
                <div class="p-2 bg-slate-200 rounded-lg">
                  <span class="material-symbols-outlined text-slate-600" data-icon="share">share</span>
                </div>
                <div>
                  <p class="text-xs font-bold text-on-surface">Exportar datos</p>
                  <p class="text-[10px] text-on-surface-variant">Sincronización en la nube con HCE activa</p>
                </div>
              </div>
            </div>
          </div>
          <!-- AI Progress Alert (Hidden by default, shown for logic showcase) -->
          <div class="alert alert-info shadow-lg bg-blue-50 border-blue-100 hidden">
            <span class="material-symbols-outlined text-blue-600" data-icon="info">info</span>
            <div class="flex-1">
              <h3 class="font-bold text-sm text-blue-900">Red neuronal activa</h3>
              <div class="text-xs text-blue-700">Analizando patrones patológicos... 78% completado</div>
              <progress class="progress progress-primary w-full mt-2" max="100" value="78"></progress>
            </div>
            <button class="btn btn-sm btn-ghost">Cancelar</button>
          </div>
        </div>
      </section>
      <!-- Right Side Panel: Visual Guide -->
      <aside
          class="w-full lg:w-[400px] bg-slate-50 dark:bg-slate-900 border-l border-slate-200/50 p-8 space-y-8 lg:min-h-screen">
        <div class="space-y-2">
          <span class="text-[10px] font-bold text-secondary uppercase tracking-widest">Guía de protocolo</span>
          <h4 class="font-headline text-2xl font-extrabold text-blue-900">Guía visual clínica</h4>
          <p class="text-sm text-on-surface-variant">Asegura un análisis de alta fidelidad siguiendo estos
            protocolos de captura.</p>
        </div>
        <!-- DaisyUI Steps -->
        <div class="mt-8">
          <ul class="steps steps-vertical w-full space-y-8">
            <li class="step step-primary" data-content="✓">
              <div class="text-left w-full pl-4">
                <div class="flex justify-between items-center mb-3">
                  <h5 class="text-sm font-bold text-blue-900">Iluminación óptima</h5>
                </div>
                <div class="relative h-32 rounded-lg overflow-hidden shadow-sm mb-3">
                  <img class="w-full h-full object-cover" data-alt="bright clinical lighting setup"
                       src="https://lh3.googleusercontent.com/aida-public/AB6AXuCYRDCzIwcyNHwte-xRrMqAIP5HWcLdPrJjVRLqV-HbJKP4_Hz_z6-rIVc2HkAqJawLWbmwUxqh9jRz32O5zxEeTHAwM9FAbZ4l4UjIOfxK0JyyRLR-DrzQCgpQx0BGyW4kO5pLVa-EusF7u6tTySIywxiHfqZgHIfPxoIoxsWWRJtU1P3jtI_-wohvP7ZO4GUx5g9yvD33s71qh1vvMULPuhuSwZObf2N0ONr9kXpkQ867WaOKd0K30On1N1NO3VUelUAnZcClF3KC"/>
                  <div
                      class="absolute bottom-2 left-2 px-2 py-1 bg-black/60 backdrop-blur-md rounded text-[9px] text-white font-bold uppercase">
                    Luz neutra suave
                  </div>
                </div>
                <p class="text-[11px] text-on-surface-variant leading-relaxed">Evita el flash directo sobre superficies
                  brillantes. Usa fuentes secundarias de luz blanca difusa.</p>
              </div>
            </li>
            <li class="step">
              <div class="text-left w-full pl-4">
                <div class="flex justify-between items-center mb-3">
                  <h5 class="text-sm font-bold text-blue-900">Ángulo correcto</h5>
                </div>
                <div class="relative h-32 rounded-lg overflow-hidden shadow-sm mb-3">
                  <img class="w-full h-full object-cover" data-alt="side view macro photography of dental models"
                       src="https://lh3.googleusercontent.com/aida-public/AB6AXuBNiCvKzHNUdRE0SDToBoiq0uv3Igb9XjSlBQXFYzCJ-s-t10M4r8blCDW0fjBpCnQHCOzb3Vd18n_d8eq5S74LF_A46jvnjh7xmLA_ak_WVPPLmfpHchVFek7EY4f6Yy6Loxi3isbpba7r4pZts4QSJEl4NKGnTnOd-02-biXcK0rVgBc52ZKupMsMDtPvKmz6NCjvZe0z1A0a0WkGwy0VsOA9ooYbYQMRNTXMe3SvERE-ygm37stTyfQs_bEq43EC9j3TfTwcHaCj"/>
                  <div
                      class="absolute bottom-2 left-2 px-2 py-1 bg-black/60 backdrop-blur-md rounded text-[9px] text-white font-bold uppercase">
                    Vista ortogonal
                  </div>
                </div>
                <p class="text-[11px] text-on-surface-variant leading-relaxed">Captura imágenes perpendiculares a la
                  superficie dental. Mantiene el plano oclusal horizontal.</p>
              </div>
            </li>
            <li class="step">
              <div class="text-left w-full pl-4">
                <div class="flex justify-between items-center mb-3">
                  <h5 class="text-sm font-bold text-blue-900">Calibración de enfoque</h5>
                </div>
                <div class="alert bg-white/50 border-slate-200 p-3 rounded-lg flex items-center gap-4">
                  <span class="material-symbols-outlined text-primary text-2xl" data-icon="center_focus_weak">center_focus_weak</span>
                  <p class="text-[11px] text-on-surface-variant">La IA requiere un mínimo de 300 DPI. Usa
                    bloqueo de enfoque óptico.</p>
                </div>
              </div>
            </li>
          </ul>
        </div>
        <!-- Support Module / DaisyUI Alert Style -->
        <div class="card bg-primary text-primary-content shadow-xl mt-8">
          <div class="card-body p-6 gap-4">
            <p class="text-[10px] font-bold uppercase tracking-widest opacity-80">Verificación profesional</p>
            <p class="text-sm font-medium leading-relaxed">Los resultados de IA son orientativos. Siempre
              contrástalos con exámenes clínicos táctiles.</p>
            <div class="card-actions">
              <button
                  class="btn btn-block btn-sm btn-neutral bg-white text-primary border-none hover:bg-slate-100 font-bold uppercase tracking-tight">
                Solicitar revisión manual
              </button>
            </div>
          </div>
        </div>
      </aside>
    </main>
    <!-- Footer (Shared Component) -->
    <Footer/>
  </div>

</template>

<style>
.material-symbols-outlined {
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}

.scan-line {
  height: 2px;
  background: linear-gradient(90deg, transparent, #22d3ee, transparent);
  box-shadow: 0 0 15px #22d3ee;
  position: absolute;
  width: 100%;
  top: 0;
  z-index: 20;
}

.glass-panel {
  backdrop-filter: blur(12px);
  background: rgba(15, 23, 42, 0.8);
}
</style>
