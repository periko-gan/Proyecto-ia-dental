<script setup>

import Header from "@/components/parts/Header.vue";
import Aside from "@/components/parts/Aside.vue";
import Footer from "@/components/parts/Footer.vue";
</script>

<template>

  <div class="bg-surface font-body text-on-surface">
    <!-- TopNavBar -->
    <Header/>
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
                <li>Analysis</li>
                <li class="text-primary font-semibold">Report #AX-9021</li>
              </ul>
            </div>
            <h1 class="text-4xl font-headline font-extrabold text-on-surface tracking-tight">AI Diagnostic Report</h1>
            <p class="text-on-surface-variant mt-1">Patient: Elena Rodriguez • Scan Date: Oct 24, 2024</p>
          </div>
          <div class="flex gap-3">
            <button class="btn btn-outline btn-sm border-outline-variant text-on-surface font-bold normal-case">
              <span class="material-symbols-outlined text-sm">share</span> Share
            </button>
            <button class="btn btn-primary btn-sm font-bold normal-case">
              <span class="material-symbols-outlined text-sm">picture_as_pdf</span> Download Informe PDF
            </button>
          </div>
        </div>
        <!-- Stats Overview using DaisyUI Stats -->
        <div class="stats shadow-sm w-full bg-white mb-8 border border-slate-100">
          <div class="stat">
            <div class="stat-figure text-error">
              <span class="material-symbols-outlined text-3xl">priority_high</span>
            </div>
            <div class="stat-title text-slate-500 font-medium">Critical Issues</div>
            <div class="stat-value text-error">1</div>
            <div class="stat-desc">Requires immediate action</div>
          </div>
          <div class="stat">
            <div class="stat-figure text-warning">
              <span class="material-symbols-outlined text-3xl">visibility</span>
            </div>
            <div class="stat-title text-slate-500 font-medium">Follow-ups</div>
            <div class="stat-value text-warning">1</div>
            <div class="stat-desc">21% increase from last scan</div>
          </div>
          <div class="stat">
            <div class="stat-figure text-success">
              <span class="material-symbols-outlined text-3xl">check_circle</span>
            </div>
            <div class="stat-title text-slate-500 font-medium">Overall Health</div>
            <div class="stat-value text-success">88%</div>
            <div class="stat-desc">Above patient average</div>
          </div>
        </div>
        <!-- Analysis Layout -->
        <div class="grid grid-cols-12 gap-6">
          <!-- Left: Visualizer -->
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
          <!-- Right: Findings Panel -->
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