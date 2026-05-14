<script setup>
import logo from "@/assets/img/logo01.png";
import {useAside} from '@/composables/useAside'

// destructure the composable - mobile menu logic lives in the composable now
const {loggedUserName, navLinkClass, handleLogout, isOpen, openMenu, closeMenu, logoutAndClose} = useAside()
</script>

<template>
  <!-- Mobile: hamburger button -->
  <button aria-label="Abrir menú" @click="openMenu" class="md:hidden fixed top-4 left-4 z-50 btn btn-square btn-ghost">
    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
    </svg>
  </button>

  <!-- Mobile drawer -->
  <div v-if="isOpen" class="fixed inset-0 z-40 flex">
    <div class="absolute inset-0 bg-black/40" @click="closeMenu" aria-hidden="true"></div>
    <aside class="relative w-64 h-full bg-white border-r border-slate-200 p-6 shadow-lg">
      <button aria-label="Cerrar menú" @click="closeMenu" class="btn btn-ghost btn-square absolute top-4 right-4">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
        </svg>
      </button>
      <!-- drawer content -->
      <div class="flex flex-col items-center mb-6">
        <img class="h-20 w-auto" :src="logo" alt="logo">
        <p class="text-xs font-bold text-on-surface pt-4">Hola <span class="capitalize">{{ loggedUserName }}</span> </p>
      </div>
      <nav>
        <ul class="menu menu-md w-full p-0 gap-1">
          <li>
            <router-link @click="closeMenu" :to="{name: 'Dashboard'}" :class="navLinkClass('Dashboard')">
              <span class="uppercase">Dashboard</span>
            </router-link>
          </li>
          <li>
            <router-link @click="closeMenu" :to="{name: 'Analyze'}" :class="navLinkClass('Analyze')">
              <span class="uppercase">Analizar imagen</span>
            </router-link>
          </li>
          <li>
            <router-link @click="closeMenu" :to="{name: 'Diagnostic'}" :class="navLinkClass('Diagnostic')">
              <span class="uppercase">Diagnóstico</span>
            </router-link>
          </li>
          <li>
            <button @click="logoutAndClose" class="w-full text-left" :class="navLinkClass('Salir')">
              <span class="uppercase">Salir</span>
            </button>
          </li>
        </ul>
      </nav>
    </aside>
  </div>

  <!-- Desktop/large aside -->
  <aside class="w-55 h-full  fixed top-0 left-0 hidden md:flex flex-col bg-white border-r border-slate-200 z-40 transition-all">
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
        <p class="text-xs font-bold text-on-surface pt-5">Hola <span class="capitalize">{{ loggedUserName }}</span> </p>
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
