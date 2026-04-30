<script setup>
// Vista principal del panel clinico con resumen de estado, metricas y accesos rapidos.

import Header from '@/components/parts/all_pages/Header.vue'
import Aside from '@/components/parts/all_pages/Aside.vue'
import Footer from "@/components/parts/all_pages/Footer.vue";
</script>

<template>
  <div class="bg-slate-50 font-body text-on-surface">

    <!-- Header -->
<!--    <Header/>-->

    <!-- Sidebar -->
    <Aside/>

    <!-- Layout Container -->
    <div class="flex pt-16 min-h-screen">

      <!-- Main Content -->
      <main class="flex-1 md:ml-64 p-6 md:p-10">
        <div class="max-w-6xl mx-auto">
          <!-- Header -->
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
          <!-- Bento Grid -->
          <div class="grid grid-cols-1 md:grid-cols-12 gap-6">
            <!-- Health Score Hero -->
            <div class="md:col-span-4 card bg-primary text-primary-content shadow-xl overflow-hidden group">
              <div
                  class="absolute top-[-10%] right-[-10%] w-48 h-48 bg-white/10 rounded-full blur-3xl transition-transform group-hover:scale-110"></div>
              <div class="card-body relative z-10 p-8">
                <h2 class="card-title font-headline text-blue-100 opacity-80 text-lg">Índice de salud dental</h2>
                <p class="text-[10px] text-blue-200 uppercase tracking-widest font-label -mt-2">Actualizado hace 2
                  horas</p>
                <div class="py-10 flex items-baseline gap-2">
                  <span class="text-7xl font-black font-headline">85</span>
                  <span class="text-2xl font-bold opacity-60">/100</span>
                </div>
                <div class="space-y-4">
                  <progress class="progress progress-secondary w-full" max="100" value="85"></progress>
                  <p class="text-sm font-medium leading-relaxed text-blue-50">Tu salud bucal está por encima del
                    promedio. Detectamos una acumulación leve de placa en la zona molar.</p>
                </div>
              </div>
            </div>
            <!-- Latest Diagnosis -->
            <div class="md:col-span-5 card bg-white border border-slate-200 shadow-sm">
              <div class="card-body p-6">
                <div class="flex justify-between items-start mb-6">
                  <div>
                    <h3 class="font-headline font-extrabold text-slate-900 text-lg">Último diagnóstico de IA</h3>
                    <p class="text-[10px] text-slate-500 font-label tracking-wide uppercase">24 MAYO, 2024 • 14:30</p>
                  </div>
                  <div class="badge badge-secondary font-black text-[10px] py-3 px-3">VERIFICADO</div>
                </div>
                <div class="flex flex-col sm:flex-row gap-6">
                  <div
                      class="relative group cursor-zoom-in w-full sm:w-32 aspect-square rounded-xl overflow-hidden border border-slate-100">
                    <img alt="Escaneo diagnóstico"
                         class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                         src="https://lh3.googleusercontent.com/aida-public/AB6AXuCBtlhexqqhYryJOAvfwoEJW6CPye5m2Pm-ZL_VlHL4LSVf5qiR2vrQeIcXtwqPPkx_i6S8W5tA8FJf1EKYJlYk-Ny35EF1iyrLD3fftK86LXpTrwvNRC7taWBVCiqevbmAutb-A31zna-HKZOxaFTqhuxjlOxpsXCvLPOpF-ggkpIHaO9S0KL7gCGXb9ZYoSJJZE733-jvlEOH8LQ_cCMprgBgzacVk64OMTPlcyhshQ9TIoznJUsgBue352KHJ6JbJsbf_tr1XAdO"/>
                    <div
                        class="absolute inset-0 bg-slate-900/40 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity">
                      <span class="material-symbols-outlined text-white">zoom_in</span>
                    </div>
                  </div>
                  <div class="flex-1 flex flex-col justify-center space-y-4">
                    <div class="space-y-1">
                      <p class="text-[10px] font-bold text-slate-400 uppercase tracking-tighter">HALLAZGO PRINCIPAL</p>
                      <p class="text-base font-bold text-slate-900 leading-tight">Erosión leve del esmalte en la pieza
                        #14</p>
                    </div>
                    <div class="flex items-center gap-2">
                      <div class="avatar-group -space-x-3 rtl:space-x-reverse">
                        <div class="avatar border-white w-6 h-6">
                          <div class="bg-slate-200 text-[10px] flex items-center justify-center">
                            <span class="material-symbols-outlined text-[10px] scale-75">drive_ai</span>
                          </div>
                        </div>
                        <div class="avatar border-white w-6 h-6">
                          <div class="bg-primary text-white text-[8px] font-bold flex items-center justify-center">DH
                          </div>
                        </div>
                      </div>
                      <span class="text-[10px] font-medium text-slate-500 italic">Validado por el Dr. Henderson</span>
                    </div>
                  </div>
                </div>
                <div class="card-actions mt-6">
                  <button
                      class="btn btn-outline btn-sm w-full font-bold text-blue-800 hover:bg-blue-50 hover:border-blue-800 transition-all">
                    Ver informe detallado
                  </button>
                </div>
              </div>
            </div>
            <!-- Reminders -->
            <div class="md:col-span-3 card bg-slate-100/50 border border-slate-200">
              <div class="card-body p-6">
                <h3 class="font-headline font-extrabold text-slate-900 mb-4">Recordatorios</h3>
                <div class="space-y-4">
                  <div class="flex items-start gap-4">
                    <div
                        class="w-10 h-10 rounded-xl bg-white flex items-center justify-center text-primary shadow-sm flex-shrink-0">
                      <span class="material-symbols-outlined text-lg">calendar_month</span>
                    </div>
                    <div class="space-y-0.5">
                      <p class="text-sm font-bold text-slate-900">Limpieza profesional</p>
                      <p class="text-[10px] text-slate-500 font-medium">12 JUNIO, 10:00</p>
                    </div>
                  </div>
                  <div class="flex items-start gap-4 opacity-50">
                    <div
                        class="w-10 h-10 rounded-xl bg-white flex items-center justify-center text-slate-400 shadow-sm flex-shrink-0">
                      <span class="material-symbols-outlined text-lg">pill</span>
                    </div>
                    <div class="space-y-0.5">
                      <p class="text-sm font-bold text-slate-900">Tratamiento antibiótico</p>
                      <p class="text-[10px] text-slate-500 font-medium uppercase">Completado el 15 de mayo</p>
                    </div>
                  </div>
                </div>
                <div class="mt-auto pt-6">
                  <div class="p-4 bg-white rounded-xl border-l-4 border-emerald-500 shadow-sm">
                    <p class="text-[10px] font-black text-emerald-700 uppercase mb-1 tracking-wider">CONSEJO</p>
                    <p class="text-[11px] text-slate-600 italic leading-relaxed">Se recomienda el siguiente escaneo en
                      14
                      días para seguimiento de tendencia.</p>
                  </div>
                </div>
              </div>
            </div>
            <!-- Chart Section -->
            <div class="md:col-span-8 card bg-white border border-slate-200 shadow-sm overflow-hidden">
              <div class="card-body p-8">
                <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-10 gap-4">
                  <div>
                    <h3 class="font-headline font-extrabold text-xl text-slate-900">Salud por zona dental</h3>
                    <p class="text-sm text-slate-500 font-label">Análisis de distribución por IA en todos los
                      cuadrantes</p>
                  </div>
                  <div class="join border border-slate-200 p-1 bg-slate-50 rounded-lg">
                    <button
                        class="btn btn-xs join-item btn-ghost text-[10px] h-7 font-bold text-blue-700 bg-white shadow-sm">
                      MENSUAL
                    </button>
                    <button class="btn btn-xs join-item btn-ghost text-[10px] h-7 font-bold text-slate-400">ANUAL
                    </button>
                  </div>
                </div>
                <div class="grid grid-cols-2 lg:grid-cols-4 gap-10">
                  <div class="flex flex-col items-center gap-6">
                    <div class="radial-progress text-primary font-black font-headline text-lg" role="progressbar"
                         style="--value:90; --size:6rem; --thickness: 8px;">90%
                    </div>
                    <span
                        class="badge badge-ghost text-[10px] font-bold tracking-widest uppercase py-2 h-auto">Incisivos</span>
                  </div>
                  <div class="flex flex-col items-center gap-6">
                    <div class="radial-progress text-secondary font-black font-headline text-lg" role="progressbar"
                         style="--value:75; --size:6rem; --thickness: 8px;">75%
                    </div>
                    <span
                        class="badge badge-ghost text-[10px] font-bold tracking-widest uppercase py-2 h-auto">Molares</span>
                  </div>
                  <div class="flex flex-col items-center gap-6">
                    <div class="radial-progress text-info font-black font-headline text-lg" role="progressbar"
                         style="--value:85; --size:6rem; --thickness: 8px;">85%
                    </div>
                    <span
                        class="badge badge-ghost text-[10px] font-bold tracking-widest uppercase py-2 h-auto">Caninos</span>
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
            <!-- CTA Action -->
            <div class="md:col-span-4 h-full">
              <button
                  class="card w-full h-full min-h-[220px] bg-gradient-to-br from-secondary to-primary text-white shadow-xl hover:shadow-2xl transition-all duration-300 group">
                <div class="card-body items-start text-left p-8 justify-between relative overflow-hidden">
                  <div class="absolute -bottom-8 -right-8 opacity-10 group-hover:scale-125 transition-transform">
                    <span class="material-symbols-outlined text-[180px]">biotech</span>
                  </div>
                  <div
                      class="w-14 h-14 bg-white/20 rounded-2xl flex items-center justify-center backdrop-blur-md group-hover:bg-white/30 transition-all border border-white/10">
                    <span class="material-symbols-outlined text-white text-3xl"
                          style="font-variation-settings: 'FILL' 1;">biotech</span>
                  </div>
                  <div class="space-y-2 relative z-10">
                    <h2 class="card-title text-2xl font-black font-headline leading-tight">Nuevo Análisis de IA</h2>
                    <p class="text-white/80 text-xs font-medium max-w-[200px]">Suba una foto o radiografía para un
                      diagnóstico instantáneo asistido por IA</p>
                  </div>
                  <div class="flex items-center gap-2 font-black text-sm uppercase tracking-widest mt-4">
                    <span>Comenzar</span>
                    <span class="material-symbols-outlined text-sm group-hover:translate-x-2 transition-transform">arrow_forward</span>
                  </div>
                </div>
              </button>
            </div>
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
