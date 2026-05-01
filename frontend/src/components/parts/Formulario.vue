<script setup>
import { computed } from 'vue'
import { useAuthForm } from '@/composables/useAuthForm'

// Recibe el contexto de página para reutilizar el mismo formulario en login y registro.
const props = defineProps({
  page: {
    type: String,
    default: 'register',
  },
})

const {
  isLogin,
  fullName,
  email,
  password,
  loading,
  errorMessage,
  emailError,
  passwordError,
  emailTouched,
  passwordTouched,
  passwordVisible,
  formTitle,
  formSubtitle,
  submitLabel,
  submitLabelLoading,
  switchText,
  switchLabel,
  switchRouteName,
  handleSubmit,
  onEmailBlur,
  onPasswordBlur,
  onEmailInput,
  onPasswordInput,
  togglePasswordVisibility,
} = useAuthForm(computed(() => props.page))
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
        <form class="space-y-5" @submit.prevent="handleSubmit">
          <div class="grid grid-cols-1 gap-5">
            <div v-if="!isLogin" class="group">
              <label
                  class="block text-[0.6875rem] font-bold uppercase tracking-wider text-outline mb-1.5 ml-1 transition-colors group-focus-within:text-secondary">Nombre
                completo
              </label>
              <input
                  v-model="fullName"
                  class="w-full bg-surface-container-high border-0 rounded-lg px-4 py-3.5 text-on-surface placeholder:text-outline/50 focus:ring-0 focus:bg-surface-container-lowest transition-all border-l-2 border-transparent focus:border-secondary"
                  placeholder="Dra. Maria Perez" type="text"/>
            </div>
            <div class="group">
              <label
                  class="block text-[0.6875rem] font-bold uppercase tracking-wider text-outline mb-1.5 ml-1 transition-colors group-focus-within:text-secondary">
                Correo electronico</label>
              <input
                  v-model="email"
                  class="w-full bg-surface-container-high border-0 rounded-lg px-4 py-3.5 text-on-surface placeholder:text-outline/50 focus:ring-0 focus:bg-surface-container-lowest transition-all border-l-2 border-transparent focus:border-secondary"
                  placeholder="Correo electronico" type="email" @blur="onEmailBlur" @input="onEmailInput"/>
              <p v-if="emailTouched && emailError" class="mt-1 ml-1 text-sm text-error">{{ emailError }}</p>
            </div>
            <div class="group">
              <label
                  class="block text-[0.6875rem] font-bold uppercase tracking-wider text-outline mb-1.5 ml-1 transition-colors group-focus-within:text-secondary">Contrasena</label>
              <div class="relative">
                <input
                    v-model="password"
                    class="w-full bg-surface-container-high border-0 rounded-lg px-4 py-3.5 text-on-surface placeholder:text-outline/50 focus:ring-0 focus:bg-surface-container-lowest transition-all border-l-2 border-transparent focus:border-secondary"
                    placeholder="••••••••" :type="passwordVisible ? 'text' : 'password'" @blur="onPasswordBlur" @input="onPasswordInput"/>
                <span
                    class="material-symbols-outlined absolute right-4 top-1/2 -translate-y-1/2 cursor-pointer text-outline-variant hover:text-secondary transition-colors"
                    :data-icon="passwordVisible ? 'visibility_off' : 'visibility'"
                    @click="togglePasswordVisibility">{{ passwordVisible ? 'visibility_off' : 'visibility' }}</span>
              </div>
              <p v-if="passwordTouched && passwordError" class="mt-1 ml-1 text-sm text-error">{{ passwordError }}</p>
            </div>
          </div>
          <!--          <div class="flex items-center gap-3 pt-2">-->
          <!--            <input class="rounded-sm border-outline-variant text-primary focus:ring-primary h-4 w-4" id="terms"-->
          <!--                   type="checkbox"/>-->
          <!--            <label class="text-xs text-on-surface-variant" for="terms">Acepto los <a-->
          <!--                class="text-primary font-semibold hover:underline" href="#">Términos del servicio</a> y los <a-->
          <!--                class="text-primary font-semibold hover:underline" href="#">Protocolos de datos clínicos</a>.</label>-->
          <!--          </div>-->
          <p v-if="errorMessage" class="text-sm text-error">{{ errorMessage }}</p>
          <div class="pt-4">
            <button
                :disabled="loading"
                class="w-full bg-primary text-white text-on-primary py-4 px-6 rounded-lg font-bold clinical-shadow hover:bg-primary-container active:scale-[0.98] transition-all flex items-center justify-center gap-2 group"
                type="submit">
              {{ loading ? submitLabelLoading : submitLabel }}
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
