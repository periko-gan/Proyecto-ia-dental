<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import logo from '@/assets/img/logo.png'

const route = useRoute()
const isMenuOpen = ref(false)

// Calcula clases de navegacion segun la ruta activa actual.
function navLinkClass(routeName) {
  const baseClass = 'btn btn-ghost btn-sm font-bold rounded-none border-b-2'
  const activeClass = 'text-blue-700 border-blue-700'
  const inactiveClass = 'text-slate-500 border-transparent hover:text-blue-600'

  return `${baseClass} ${route.name === routeName ? activeClass : inactiveClass}`
}

function closeMenu() {
  isMenuOpen.value = false
}

watch(
  () => route.fullPath,
  () => {
    closeMenu()
  },
)
</script>

<template>
  <!-- Navbar -->
  <header
      class="navbar fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-slate-200 px-4 md:px-8 relative"
  >
    <div class="navbar-start">
      <router-link :to="{ name: 'Landing' }" @click="closeMenu">
        <img class="h-20 w-auto ml-2" :src="logo" alt="logo"/>
      </router-link>
    </div>

    <div class="navbar-end lg:hidden">
      <button
          type="button"
          class="btn btn-ghost btn-circle"
          :aria-expanded="isMenuOpen"
          aria-label="Abrir menú"
          @click="isMenuOpen = !isMenuOpen"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
             stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"/>
        </svg>
      </button>
    </div>

    <nav class="hidden lg:flex navbar-end ml-10 space-x-2">
      <router-link :to="{ name: 'Landing' }" :class="navLinkClass('Landing')" class="uppercase">
        Inicio
      </router-link>
      <router-link
          :to="{ name: 'Login' }"
          :class="navLinkClass('Login')"
          class="uppercase"
      >
        Iniciar sesión
      </router-link>
      <router-link :to="{ name: 'Register' }" :class="navLinkClass('Register')" class="uppercase">
        Registro
      </router-link>
    </nav>

    <div
        v-if="isMenuOpen"
        class="absolute left-0 top-full w-full border-b border-slate-200 bg-white/95 px-4 py-4 shadow-md lg:hidden"
    >
      <nav class="flex flex-col gap-2">
        <router-link
            :to="{ name: 'Landing' }"
            :class="navLinkClass('Landing')"
            class="uppercase w-full justify-start"
            @click="closeMenu"
        >
          Inicio
        </router-link>
        <router-link
            :to="{ name: 'Login' }"
            :class="navLinkClass('Login')"
            class="uppercase w-full justify-start"
            @click="closeMenu"
        >
          Iniciar sesión
        </router-link>
        <router-link
            :to="{ name: 'Register' }"
            :class="navLinkClass('Register')"
            class="uppercase w-full justify-start"
            @click="closeMenu"
        >
          Registro
        </router-link>
      </nav>
    </div>
  </header>
</template>

<style scoped></style>
