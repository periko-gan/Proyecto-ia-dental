<script setup>
import {useRoute} from 'vue-router'

import logo from '@/assets/img/logo.png'

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
  <header
      class="navbar fixed top-0 z-50 bg-white/80 backdrop-blur-md border-b border-slate-200 px-4 md:px-8"
  >
    <!--    logo-->
    <router-link :to="{ name: 'Landing' }">
      <img class="h-20 w-auto ml-2" :src="logo" alt="logo"/>
    </router-link>

    <nav class="hidden lg:flex ml-10 space-x-2">
      <router-link :to="{ name: 'Landing' }" :class="navLinkClass('Landing')" class="uppercase">
        Inicio
      </router-link>
      <router-link
          :to="{ name: 'Login' }"
          :class="navLinkClass('Iniciar sesión')"
          class="uppercase"
      >
        Iniciar sesión
      </router-link>
      <router-link :to="{ name: 'Register' }" :class="navLinkClass('Register')" class="uppercase">
        Registro
      </router-link>
    </nav>
  </header>
</template>

<style scoped></style>
