<script setup>
import {computed} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import {getSession} from '@/services/authService'
import {useDiagnosticAnalysis} from '@/composables/useDiagnosticAnalysis'

import logo from "@/assets/img/logo01.png";

const route = useRoute()
const router = useRouter()
const { clearAnalysis } = useDiagnosticAnalysis()

const loggedUserEmail = computed(() => getSession()?.email || 'Usuario sin sesión')

// Aplica estilo activo/inactivo a cada opción del sidebar en función de la ruta.
function navLinkClass(routeName) {
  const baseClass = 'text-slate-500 hover:text-blue-700'
  const activeClass = 'active bg-blue-50 text-blue-700 font-bold border-r-4 border-blue-700 rounded-noness'
  const inactiveClass = 'text-slate-500 border-transparent hover:text-blue-600'

  return `${baseClass} ${route.name === routeName ? activeClass : inactiveClass}`
}

// Maneja el logout: limpia sessionStorage, IndexedDB y redirige a la página principal
async function handleLogout() {
  clearAnalysis()
  sessionStorage.clear()
  
  try {
    if (window.indexedDB) {
      // Eliminar bases de datos explícitas de la aplicación
      window.indexedDB.deleteDatabase('DentalAI-Images')
      window.indexedDB.deleteDatabase('dental-ai-upload-queue')
      
      // Intentar eliminar cualquier otra si el navegador lo soporta
      if (indexedDB.databases) {
        const dbs = await indexedDB.databases()
        dbs.forEach(db => {
          if (db.name) {
            window.indexedDB.deleteDatabase(db.name)
          }
        })
      }
    }
  } catch (error) {
    console.warn('Error limpiando IndexedDB en logout:', error)
  }
  
  router.push('/')
}
</script>

<template>
  <aside
      class="w-55 h-full  fixed top-0 left-0 hidden md:flex flex-col bg-white border-r border-slate-200 z-40 transition-all">
    <div class="px-6 py-6 border-t border-slate-200/50">
<!--      <div class="flex items-center tex gap-3 mb-6">-->
<!--      <div class="flex items-center tex mb-6">      -->
      <div class="flex flex-col items-center tex mb-6">
<!--        <router-link :to="{name: 'Landing'}">-->
        <img class="h-20 w-auto ml-2" :src="logo" alt="logo">
<!--      </router-link>-->
<!--        <div class="avatar">-->
<!--          <div class="w-10 rounded-full">-->
<!--            <img alt="Retrato profesional de un cirujano dental"-->
<!--                 data-alt="professional portrait of a male dental surgeon"-->
<!--                 src="https://lh3.googleusercontent.com/aida-public/AB6AXuD6U4FRC9SmbBNDhZ-tJESgi2UgtW6a-5oylEeWZ1RlnjLegnAFSgs8wYqSAxuMHu9Pemhqne9uOWzjdJUt7yuJ7YmmONlaRKA31C4M8XEBqLX5-R9CLi_tjsn0barAhAp1W_nrctT5LeEMcHrUI4hhPYbeFQMdKkAOFopPQpv6lksBTGlOfe6qVuhvfRlxXmB7s3AnVhpz6o1SNg54GdxjccpXVSVO2b-e3zihYyfB-B0QW06vswwq9CXOIKWlyMqgYGqpFpGZcVOg"/>-->
<!--          </div>-->
<!--        </div>-->
<!--        <div>-->
          <p class="text-xs font-bold text-on-surface pt-5">Hola {{ loggedUserEmail }}</p>
<!--          <p class="text-[10px] text-slate-500 uppercase tracking-wider">Cirujano dental</p>-->
<!--        </div>-->
      </div>
    </div>
    <nav class="p-6">
      <ul class="menu menu-md w-full p-0 gap-1">
        <li>
          <router-link :to="{name: 'Dashboard'}" :class="navLinkClass('Dashboard')">
            <span class="uppercase">Dashboard</span>
          </router-link>
        </li>
        <li>
          <router-link :to="{name: 'Analyze'}" :class="navLinkClass('Analyze')">
            <span class="uppercase">Analizar imagen</span>
          </router-link>
        </li>
        <li>
          <router-link :to="{name: 'Diagnostic'}" :class="navLinkClass('Diagnostic')">
            <span class="uppercase">Diagnóstico</span>
          </router-link>
        </li>
        <!-- <li>
          <router-link :to="{name: 'Evolution'}" :class="navLinkClass('Evolution')">
            <span class="uppercase">Evolution</span>
          </router-link>
        </li> -->
<!--        <li>-->
<!--          <router-link :to="{name: 'Login'}" :class="navLinkClass('Login')">-->
<!--            <span class="uppercase">Iniciar sesión</span>-->
<!--          </router-link>-->
<!--        </li>-->
<!--        <li>-->
<!--          <router-link :to="{name: 'Register'}" :class="navLinkClass('Register')">-->
<!--            <span class="uppercase">Registro</span>-->
<!--          </router-link>-->
<!--        </li>-->
        <li>
          <button @click="handleLogout" class="w-full text-left" :class="navLinkClass('Salir')">
            <span class="uppercase">Salir</span>
          </button>
        </li>

      </ul>
    </nav>

  </aside>
</template>

<style scoped>

</style>
