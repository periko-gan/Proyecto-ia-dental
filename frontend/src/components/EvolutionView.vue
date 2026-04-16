<script setup>

import Header from "@/components/parts/Header.vue";
import Aside from "@/components/parts/Aside.vue";
import Footer from "@/components/parts/Footer.vue";
</script>

<template>
  <div class="bg-surface font-body text-on-surface">

    <!-- TopNavBar Component -->
    <Header/>

    <!-- SideNavBar Component -->
    <Aside/>


    <!-- Main Content Area -->
    <main class="md:ml-64 pt-20 px-8 pb-12 min-h-screen">

      <!-- Content -->
      <div class="p-6 lg:p-10 max-w-7xl mx-auto w-full space-y-8">
        <!-- Header Section -->
        <div class="flex flex-col md:flex-row md:items-end justify-between gap-6">
          <div>
            <div class="text-[10px] font-bold uppercase tracking-[0.2em] text-slate-400 mb-2">Análisis de Progreso</div>
            <h3 class="text-4xl font-headline font-extrabold text-neutral tracking-tight">Evolución de Salud Dental</h3>
          </div>
          <div class="flex flex-wrap items-center gap-3">
            <div class="join bg-white border border-base-200">
              <button class="join-item btn btn-sm btn-ghost hover:bg-primary/10 text-primary font-bold">6 Meses</button>
              <button class="join-item btn btn-sm btn-ghost text-slate-500">1 Año</button>
              <button class="join-item btn btn-sm btn-ghost text-slate-500">Todo</button>
            </div>
            <button class="btn btn-sm btn-outline border-base-300 gap-2">
              <span class="material-symbols-outlined text-lg">filter_list</span>
              Filtros
            </button>
            <button class="btn btn-sm btn-secondary gap-2 text-white">
              <span class="material-symbols-outlined text-lg">share</span>
              Exportar
            </button>
          </div>
        </div>
        <!-- Dashboard Widgets -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <!-- Charts Card -->
          <div class="lg:col-span-8 card bg-white border border-base-200 shadow-sm overflow-hidden">
            <div class="card-body p-0">
              <div class="flex items-center justify-between p-6 border-b border-base-200">
                <div>
                  <h4 class="card-title font-headline font-bold text-primary">Puntuación de Salud General</h4>
                  <div class="badge badge-success badge-sm badge-outline gap-1 mt-1 font-bold">
                    <span class="material-symbols-outlined text-[10px]">trending_up</span>
                    +12% mejora
                  </div>
                </div>
                <div class="flex items-center gap-2 text-[11px] font-bold text-secondary uppercase tracking-wider">
                  <span class="w-2 h-2 rounded-full bg-secondary animate-pulse"></span>
                  AI Predictive Engine
                </div>
              </div>
              <div class="p-6 h-64 flex items-end justify-between gap-3 bg-slate-50/30">
                <!-- Chart Mockup with DaisyUI color accents -->
                <div class="flex-1 flex flex-col items-center gap-2">
                  <div class="w-full bg-primary/10 rounded-t-lg transition-all hover:bg-primary/20"
                       style="height: 40%"></div>
                  <span class="text-[10px] font-bold text-slate-400 uppercase">Ene</span>
                </div>
                <div class="flex-1 flex flex-col items-center gap-2">
                  <div class="w-full bg-primary/20 rounded-t-lg transition-all hover:bg-primary/30"
                       style="height: 45%"></div>
                  <span class="text-[10px] font-bold text-slate-400 uppercase">Feb</span>
                </div>
                <div class="flex-1 flex flex-col items-center gap-2">
                  <div class="w-full bg-primary/30 rounded-t-lg transition-all hover:bg-primary/40"
                       style="height: 58%"></div>
                  <span class="text-[10px] font-bold text-slate-400 uppercase">Mar</span>
                </div>
                <div class="flex-1 flex flex-col items-center gap-2">
                  <div class="w-full bg-primary/40 rounded-t-lg transition-all hover:bg-primary/50"
                       style="height: 52%"></div>
                  <span class="text-[10px] font-bold text-slate-400 uppercase">Abr</span>
                </div>
                <div class="flex-1 flex flex-col items-center gap-2">
                  <div class="w-full bg-primary/50 rounded-t-lg transition-all hover:bg-primary/60"
                       style="height: 65%"></div>
                  <span class="text-[10px] font-bold text-slate-400 uppercase">May</span>
                </div>
                <div class="flex-1 flex flex-col items-center gap-2">
                  <div class="w-full bg-secondary rounded-t-lg relative group" style="height: 82%">
                    <div
                        class="absolute -top-10 left-1/2 -translate-x-1/2 bg-neutral text-white text-[10px] px-2 py-1 rounded-md opacity-0 group-hover:opacity-100 transition-opacity">
                      82%
                    </div>
                  </div>
                  <span class="text-[10px] font-bold text-secondary uppercase">Jun</span>
                </div>
              </div>
            </div>
          </div>
          <!-- Stats/Metric Card -->
          <div class="lg:col-span-4 card bg-white border border-base-200 shadow-sm">
            <div class="card-body p-6">
              <h4 class="card-title font-headline font-bold text-primary mb-4 text-lg">Comparativa Directa</h4>
              <div class="flex flex-col gap-4">
                <div class="flex items-center gap-4 bg-base-100 p-4 rounded-xl border border-base-200">
                  <div class="avatar-group -space-x-4 rtl:space-x-reverse">
                    <div class="avatar border-white">
                      <div class="w-16 rounded-lg bg-slate-200">
                        <img class="grayscale opacity-50"
                             src="https://lh3.googleusercontent.com/aida-public/AB6AXuDe-W-Ca7g9eXU1KlgZqL1w8rruLs8ZaeG9X0k39DlPvUGF_TvoLfG6DuLAtSdAMTgjCUDxijNJ6yi_pvMaBYTYZyPP_yKwsqjjfgHQqaa6RjQI7mfCFtjfrh_-uzCMt1oZCQDnX70HmkadvI4_dmRZOqVXLqr8iBjbE-hd6GIThLbV6B4y-GFdTPzKESwx5BPT0ShDIxLwIeCe-x3Wcr1U6wFGDqfgLzthzuQPGXsNhuVDU_5Jbj9maMOcx4y-z9WCwIYjMbbiABFU"/>
                      </div>
                    </div>
                    <div class="avatar border-white">
                      <div class="w-16 rounded-lg border-2 border-secondary">
                        <img
                            src="https://lh3.googleusercontent.com/aida-public/AB6AXuD4J0U9xIdCwOPOrWwpQeqhCs3hAOcXGgGnQhElbmod4IPUOabK6T3wbXyy56gDsHGreoOhni7WZa4E5TocaF9ZomaHzjoXPw7z4q4mSZCNm-j_d5fo3p2sGSRoX7HuW7duuGstK1KTca9ooUOKpKM3DhbwVMRZKYL3DhTIBgkahGWimTHCUsKpHj2YUkhwjveb8piDwWd_Zj7g2QC_l_p_VCU2AqdzAS5aJzJMXiNxpBW_xV43SV5AdGyVtiWJTJSUZFrSiFqgOtUv"/>
                      </div>
                    </div>
                  </div>
                  <div class="flex-1">
                    <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Estado Actual</p>
                    <p class="text-xs font-medium text-neutral mt-1 leading-tight">Mejora del 45% en inflamación
                      gingival.</p>
                  </div>
                </div>
                <div class="stats stats-vertical bg-primary text-white shadow">
                  <div class="stat py-3">
                    <div class="stat-title text-white/70 text-[10px] uppercase font-bold">Densidad Ósea</div>
                    <div class="stat-value text-2xl font-headline">Estable</div>
                    <div class="stat-desc text-white/60">Sector 32 - Sin cambios</div>
                  </div>
                  <div class="stat py-3 border-t border-white/10">
                    <div class="stat-title text-white/70 text-[10px] uppercase font-bold">Riesgo AI</div>
                    <div class="stat-value text-2xl font-headline">Bajo</div>
                    <div class="stat-desc text-white/60">Monitoreo cada 3 meses</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- Detailed Table Section -->
          <div class="lg:col-span-12 space-y-6">
            <div class="flex items-center justify-between">
              <h4 class="font-headline font-bold text-2xl text-neutral">Cronología de Escaneos</h4>
              <div class="badge badge-outline badge-sm text-slate-400 font-bold border-base-300">Total: 12 registros
              </div>
            </div>
            <div class="overflow-x-auto bg-white rounded-xl border border-base-200 shadow-sm">
              <table class="table table-zebra w-full">
                <!-- head -->
                <thead>
                <tr class="bg-base-100 text-[11px] uppercase tracking-widest text-slate-500 border-b border-base-200">
                  <th class="py-4">Procedimiento</th>
                  <th class="py-4">Personal Médico</th>
                  <th class="py-4">Fecha &amp; Score</th>
                  <th class="py-4">Estado AI</th>
                  <th class="py-4 text-right">Acciones</th>
                </tr>
                </thead>
                <tbody>
                <!-- row 1 -->
                <tr class="hover">
                  <td>
                    <div class="flex items-center gap-3">
                      <div class="avatar">
                        <div class="mask mask-squircle w-12 h-12 bg-base-200">
                          <img alt="Scan"
                               src="https://lh3.googleusercontent.com/aida-public/AB6AXuAKgigzjoiQqElNKDqpOpDaeLPOM7rleU_6Uk-c9mYeJ4x6wLgVOBnrmc8APVJb7hFScpveAjGYlFKVqqA0wE6ESXjB1RCbrb19KVq8uAaX5phFpKNIwfg5EVL-gRq40NIx7hcnjsPrabhsen7U-AWfSBDaTVpam4wBe_NvjCFCBhp1No_FGXbbzVDalrUB659fpwHoZcxFLbga7kyb9YpA2fZjeOTf7qEPf0KmGCEu5sX6bTq2r4A8Te9TbGqbZCus3hP2srx7vzRe"/>
                        </div>
                      </div>
                      <div>
                        <div class="font-bold text-neutral text-sm">Escaneo de Control Trimestral</div>
                        <div class="text-[10px] text-slate-400 mt-0.5">Hallazgo: Sanación completa</div>
                      </div>
                    </div>
                  </td>
                  <td>
                    <div class="flex flex-col">
                      <span class="text-xs font-bold text-slate-600">Dr. Henderson</span>
                      <span class="text-[10px] text-slate-400 uppercase tracking-tighter">Cirujano Dentista</span>
                    </div>
                  </td>
                  <td>
                    <div class="flex flex-col">
                      <span class="text-xs font-bold text-neutral">14 Jun, 2024</span>
                      <span class="text-[10px] font-extrabold text-secondary mt-1">SCORE: 82/100</span>
                    </div>
                  </td>
                  <td><span class="badge badge-success badge-sm text-white font-bold">ESTABLE</span></td>
                  <th class="text-right">
                    <div class="join join-horizontal">
                      <button class="btn btn-ghost btn-xs join-item"><span class="material-symbols-outlined text-sm">visibility</span>
                      </button>
                      <button class="btn btn-ghost btn-xs join-item"><span class="material-symbols-outlined text-sm">download</span>
                      </button>
                    </div>
                  </th>
                </tr>
                <!-- row 2 -->
                <tr class="hover">
                  <td>
                    <div class="flex items-center gap-3">
                      <div class="avatar">
                        <div class="mask mask-squircle w-12 h-12 bg-base-200 grayscale opacity-40">
                          <img alt="Prophylaxis"
                               src="https://lh3.googleusercontent.com/aida-public/AB6AXuAeQVkPN0gAFlDDuTtU2qYMocTIrQ6K3HL2x1RRapr4pMGkOHDzotrkO2snOab_BbIN-ZbtwSRqJy7qr3jja-nMFRhLLVyVONV2DM2D8LI2eKEt2qAWs0cMkn7vS-TDqkhH9z2LztlzYSWapHNOsGv_M57SV3a3K8qIJsB6c2vctUTHmWdNOFyt2ChucHg_JZZ0gOIkRIxrMngotnbFiJ8qnku3gpGv80KPgZhSCEcoUgAYHZUcByuLTcba7pU9KvIqcJQ7LxvKJCYm"/>
                        </div>
                      </div>
                      <div>
                        <div class="font-bold text-neutral text-sm">Limpieza Profunda &amp; Profilaxis</div>
                        <div class="text-[10px] text-slate-400 mt-0.5">Mantenimiento preventivo</div>
                      </div>
                    </div>
                  </td>
                  <td>
                    <div class="flex flex-col">
                      <span class="text-xs font-bold text-slate-600">Dra. Martinez</span>
                      <span class="text-[10px] text-slate-400 uppercase tracking-tighter">Higienista</span>
                    </div>
                  </td>
                  <td>
                    <div class="flex flex-col">
                      <span class="text-xs font-bold text-neutral">02 Abr, 2024</span>
                      <span class="text-[10px] font-extrabold text-slate-300 mt-1">N/A</span>
                    </div>
                  </td>
                  <td><span class="badge badge-info badge-sm text-white font-bold">PROCEDIMIENTO</span></td>
                  <th class="text-right">
                    <button class="btn btn-ghost btn-xs disabled"><span class="material-symbols-outlined text-sm">visibility</span>
                    </button>
                  </th>
                </tr>
                <!-- row 3 -->
                <tr class="hover">
                  <td>
                    <div class="flex items-center gap-3">
                      <div class="avatar">
                        <div class="mask mask-squircle w-12 h-12 bg-error/10">
                          <img alt="Emergency"
                               src="https://lh3.googleusercontent.com/aida-public/AB6AXuA4TLailUnD4rKpG2WbgfmbvyL6yBkvrPI8_0cIN-9HaQ3UNls8KgXmCtPia-AE54QJFo-t9ZQf3K-CKSUcPfEvCjpYU8ql40IM_3qaVp3Q2BQYWGgWiCmIO3m6VlyGBuuBQRMajcLjD2cyhAw5Id-93zN4J_34d7oiQ6hCKbaSEt4fpwxZOz5LoaZzULltZ6_WHnaTpowRvVyrRY7SnPMv312Bt0-wxQUoWX-MAxb-1s44K4HUg9PYjZwRZYi54I2jC5mCTZ8flfox"/>
                        </div>
                      </div>
                      <div>
                        <div class="font-bold text-neutral text-sm">Escaneo de Emergencia</div>
                        <div class="text-[10px] text-error mt-0.5">Dolor agudo detectado</div>
                      </div>
                    </div>
                  </td>
                  <td>
                    <div class="flex flex-col">
                      <span class="text-xs font-bold text-slate-600">Dr. Henderson</span>
                      <span class="text-[10px] text-slate-400 uppercase tracking-tighter">Cirujano Dentista</span>
                    </div>
                  </td>
                  <td>
                    <div class="flex flex-col">
                      <span class="text-xs font-bold text-neutral">12 Ene, 2024</span>
                      <span class="text-[10px] font-extrabold text-error mt-1">SCORE: 68/100</span>
                    </div>
                  </td>
                  <td><span class="badge badge-error badge-sm text-white font-bold">ALERTA</span></td>
                  <th class="text-right">
                    <button class="btn btn-ghost btn-xs"><span
                        class="material-symbols-outlined text-sm">visibility</span></button>
                  </th>
                </tr>
                </tbody>
              </table>
            </div>
            <!-- Pagination Component -->
            <div class="flex justify-center mt-6">
              <div class="join bg-white border border-base-200">
                <button class="join-item btn btn-sm btn-ghost"><span class="material-symbols-outlined text-lg">chevron_left</span>
                </button>
                <button class="join-item btn btn-sm btn-active btn-primary text-white font-bold">1</button>
                <button class="join-item btn btn-sm btn-ghost">2</button>
                <button class="join-item btn btn-sm btn-ghost">3</button>
                <button class="join-item btn btn-sm btn-ghost"><span class="material-symbols-outlined text-lg">chevron_right</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- Footer Component -->
      <Footer/>
    </main>
  </div>
</template>

<style scoped>

</style>