<script setup>
import {computed} from 'vue'

// Recibe el contexto de página para reutilizar el mismo formulario en login y registro.
const props = defineProps({
  page: {
    type: String,
    default: 'register',
  },
})

const isLogin = computed(() => props.page === 'login')
// Textos reactivos para evitar duplicar plantillas entre ambas vistas.
const formTitle = computed(() => (isLogin.value ? 'Bienvenido de nuevo' : 'Crea tu cuenta profesional'))
const formSubtitle = computed(() => (
    isLogin.value
        ? 'Introduce tus credenciales para continuar.'
        : 'Proporciona tus credenciales clínicas para empezar.'
))
const submitLabel = computed(() => (isLogin.value ? 'Iniciar sesión' : 'Registrarse'))
const switchText = computed(() => (isLogin.value ? '¿No tienes una cuenta?' : '¿Ya tienes una cuenta?'))
const switchLabel = computed(() => (isLogin.value ? 'Regístrate' : 'Inicia sesión'))
const switchRouteName = computed(() => (isLogin.value ? 'Register' : 'Login'))
</script>

<template>

  <main class="">
    <section class="flex-1 flex flex-col justify-center items-center p-6 md:p-16 lg:p-24 bg-surface">
      <div class="w-full max-w-md">
        <div class="mb-10">
          <div class="flex items-center gap-2 mb-8">
            <div class="w-10 h-10 tech-gradient rounded-md flex items-center justify-center">
              <span class="material-symbols-outlined text-white" data-icon="dentistry"
                    style="font-variation-settings: 'FILL' 1;">dentistry</span>
            </div>
            <span class="text-2xl font-extrabold tracking-tighter text-primary">Dentis AI</span>
          </div>
          <h2 class="text-3xl font-bold text-on-surface mb-2">{{ formTitle }}</h2>
          <p class="text-on-surface-variant text-sm">{{ formSubtitle }}</p>
        </div>
        <form class="space-y-5">
          <div class="grid grid-cols-1 gap-5">
            <div v-if="!isLogin" class="group">
              <label
                  class="block text-[0.6875rem] font-bold uppercase tracking-wider text-outline mb-1.5 ml-1 transition-colors group-focus-within:text-secondary">Nombre
                completo</label>
              <input
                  class="w-full bg-surface-container-high border-0 rounded-lg px-4 py-3.5 text-on-surface placeholder:text-outline/50 focus:ring-0 focus:bg-surface-container-lowest transition-all border-l-2 border-transparent focus:border-secondary"
                  placeholder="Dra. Maria Perez" type="text"/>
            </div>
            <div class="group">
              <label
                  class="block text-[0.6875rem] font-bold uppercase tracking-wider text-outline mb-1.5 ml-1 transition-colors group-focus-within:text-secondary">
                Correo electrónico</label>
              <input
                  class="w-full bg-surface-container-high border-0 rounded-lg px-4 py-3.5 text-on-surface placeholder:text-outline/50 focus:ring-0 focus:bg-surface-container-lowest transition-all border-l-2 border-transparent focus:border-secondary"
                  placeholder="Correo electrónico" type="email"/>
            </div>
            <div class="group">
              <label
                  class="block text-[0.6875rem] font-bold uppercase tracking-wider text-outline mb-1.5 ml-1 transition-colors group-focus-within:text-secondary">Contraseña</label>
              <div class="relative">
                <input
                    class="w-full bg-surface-container-high border-0 rounded-lg px-4 py-3.5 text-on-surface placeholder:text-outline/50 focus:ring-0 focus:bg-surface-container-lowest transition-all border-l-2 border-transparent focus:border-secondary"
                    placeholder="••••••••" type="password"/>
                <span
                    class="material-symbols-outlined absolute right-4 top-1/2 -translate-y-1/2 cursor-pointer text-outline-variant hover:text-secondary transition-colors"
                    data-icon="visibility">visibility</span>
              </div>
            </div>
          </div>
          <div class="flex items-center gap-3 pt-2">
            <input class="rounded-sm border-outline-variant text-primary focus:ring-primary h-4 w-4" id="terms"
                   type="checkbox"/>
            <label class="text-xs text-on-surface-variant" for="terms">Acepto los <a
                class="text-primary font-semibold hover:underline" href="#">Términos del servicio</a> y los <a
                class="text-primary font-semibold hover:underline" href="#">Protocolos de datos clínicos</a>.</label>
          </div>
          <div class="pt-4">
            <button
                class="w-full bg-primary text-white text-on-primary py-4 px-6 rounded-lg font-bold clinical-shadow hover:bg-primary-container active:scale-[0.98] transition-all flex items-center justify-center gap-2 group"
                type="submit">
              {{ submitLabel }}
            </button>
          </div>
        </form>
        <div class="mt-8 pt-8 border-t border-outline-variant/15 text-center">
          <p class="text-sm text-on-surface-variant">
            {{ switchText }}
            <router-link :to="{ name: switchRouteName }"
                         class="text-secondary font-bold hover:text-on-secondary-container transition-colors ml-1">
              {{ switchLabel }}
            </router-link>
          </p>
        </div>
      </div>
    </section>
  </main>


</template>

<style scoped>

</style>