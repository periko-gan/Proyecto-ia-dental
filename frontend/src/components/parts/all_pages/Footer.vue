<script setup>
// Pie global con disclaimer clínico y enlaces legales.

const anyoActual = new Date().getFullYear()
</script>

<template>
  <footer
      class="fixed z-99 bottom-0 footer footer-center bg-slate-100 text-slate-400 border-t border-slate-200/60 mt-20"
  >
    <div class="max-w-6xl w-full">
      <p class="text-[10px] uppercase tracking-[0.2em] font-medium max-w-lg p-1">
        <a
            class="font-extrabold"
            href="https://creativecommons.org/licenses/by/4.0/deed.es"
            target="_blank"
        >CC-BY</a
        >
        {{ anyoActual }} Sistemas Clínicos Dentis AI. Todos los diagnósticos de IA requieren
        verificación profesional odontológica.
      </p>
    </div>
  </footer>
</template>

<style scoped></style>
