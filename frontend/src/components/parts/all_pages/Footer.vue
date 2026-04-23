<script setup>
// Pie global con disclaimer clínico y enlaces legales.

import Aside from "@/components/parts/all_pages/Aside.vue";
</script>

<template>
  <footer
      class="fixed z-99 bottom-0 footer footer-center bg-slate-100 text-slate-400 border-t border-slate-200/60 mt-20">
    <div class="max-w-6xl w-full flex flex-col md:flex-row justify-between items-center gap-6">
      <aside class="text-left">
        <p class="text-[10px] uppercase tracking-[0.2em] font-medium max-w-lg">
          © 2024 Sistemas Clínicos Dentis AI. Todos los diagnósticos de IA requieren verificación profesional
          odontológica.
        </p>
      </aside>
      <nav class="flex flex-wrap justify-center gap-6">
        <a class="link link-hover text-[10px] font-black uppercase tracking-widest">Aviso médico</a>
        <a class="link link-hover text-[10px] font-black uppercase tracking-widest">Política de privacidad</a>
        <a class="link link-hover text-[10px] font-black uppercase tracking-widest underline decoration-blue-500 underline-offset-4 decoration-2">Términos
          del servicio</a>
      </nav>
    </div>
  </footer>
</template>

<style scoped>

</style>