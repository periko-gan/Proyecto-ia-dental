<script setup>
import {useRoute} from 'vue-router'

const route = useRoute()

// Calcula clases de navegacion segun la ruta activa actual.
function navLinkClass(routeName) {
  const baseClass = 'btn btn-ghost btn-sm font-bold rounded-none border-b-2'
  const activeClass = 'text-blue-700 border-blue-700'
  const inactiveClass = 'text-slate-500 border-transparent hover:text-blue-600'

  return `${baseClass} ${route.name === routeName ? activeClass : inactiveClass}`
}
</script>

<template>
  <!-- Navbar -->
  <header class="navbar fixed top-0 z-50 bg-white/80 backdrop-blur-md border-b border-slate-200 px-4 md:px-8">
<!--    <div class="flex-1">-->
<!--    logo-->
      <router-link :to="{name: 'Landing'}"
                   class="btn btn-ghost text-xl font-black text-blue-900 font-headline normal-case tracking-tight px-0">
        Dentis AI
      </router-link>

      <nav class="hidden lg:flex ml-10 space-x-2">
        <router-link :to="{name: 'Landing'}" :class="navLinkClass('Landing')">
          Inicio
        </router-link>
<!--        <router-link :to="{name: 'Dashboard'}" :class="navLinkClass('Dashboard')">-->
<!--          Panel-->
<!--        </router-link>-->
<!--        <router-link :to="{name: 'Analyze'}" :class="navLinkClass('Analyze')">-->
<!--          Analizar-->
<!--        </router-link>-->
<!--        <router-link :to="{name: 'Diagnostic'}" :class="navLinkClass('Diagnostic')">-->
<!--          Diagnóstico-->
<!--        </router-link>-->
<!--        <router-link :to="{name: 'Evolution'}" :class="navLinkClass('Evolution')">-->
<!--          Evolución-->
<!--        </router-link>-->
        <router-link :to="{name: 'Login'}" :class="navLinkClass('Login')">
          Iniciar sesión
        </router-link>
        <router-link :to="{name: 'Register'}" :class="navLinkClass('Register')">
          Registro
        </router-link>
      </nav>

<!--    </div>-->

    <div class="flex-none gap-2">
<!--      <div class="hidden sm:flex form-control relative">-->
<!--          <span-->
<!--              class="absolute left-3 top-1/2 -translate-y-1/2 material-symbols-outlined text-slate-400 text-sm">search</span>-->
<!--        <input class="input input-sm input-bordered bg-slate-50 pl-9 w-48 focus:outline-blue-600"-->
<!--               placeholder="Buscar diagnósticos..." type="text"/>-->
<!--      </div>-->
<!--      <button class="btn btn-ghost btn-circle btn-sm ">-->
<!--        <div class="indicator">-->
<!--          <span class="material-symbols-outlined text-slate-600">notifications</span>-->
<!--          <span class="badge badge-xs badge-primary indicator-item"></span>-->
<!--        </div>-->
<!--      </button>-->
<!--      <div class="dropdown dropdown-end ml-2">-->
<!--        <div class="btn btn-ghost btn-circle avatar border border-slate-200" role="button" tabindex="0">-->
<!--          <div class="w-8 rounded-full">-->
<!--            <img alt="Perfil de usuario"-->
<!--                 src="https://lh3.googleusercontent.com/aida-public/AB6AXuB9xbAbyQCpcxRzZfqtzqLxPKaDAq2C0CKQok4nfj2JCMt4JeQUjiy2O0XNWTRAzTj5O_RhvmGWyalpU1UuUSJKkITid8KHsaNDdb-kjqkJ_zUEdSKyJljfZxXHaoBo6OYr6tgsV9Vqg7Q3CjPAVYs2QB9rMqc2hcQBUQ6OEaF1_KpN8P9nCbOd31M9v6cx1dzAQMLRDU5ZXuZz_m5UlOdRylWBH-CEE_dIhDMBRxEkYULmlM22TsEvZbHc799hltrcMLtFk0pn9IYt"/>-->
<!--          </div>-->
<!--        </div>-->
<!--        <ul class="mt-3 z-[1] p-2 shadow menu menu-sm dropdown-content bg-base-100 rounded-box w-52 border border-slate-100"-->
<!--            tabindex="0">-->
<!--          <li><a>Perfil</a></li>-->
<!--          <li><a>Configuración</a></li>-->
<!--          <li><a class="text-error font-bold">Cerrar sesión</a></li>-->
<!--        </ul>-->
<!--      </div>-->
    </div>
  </header>
</template>

<style scoped>

</style>
