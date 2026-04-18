<script setup>

import Aside from "@/components/parts/all_pages/Aside.vue";
</script>

<template>
  <footer class="fixed bottom-0 footer footer-center bg-slate-100 text-slate-400 border-t border-slate-200/60 mt-20">
    <div class="max-w-6xl w-full flex flex-col md:flex-row justify-between items-center gap-6">
      <aside class="text-left">
        <p class="text-[10px] uppercase tracking-[0.2em] font-medium max-w-lg">
          © 2024 Dentis AI Clinical Systems. All AI diagnostics require professional dental verification.
        </p>
      </aside>
      <nav class="flex flex-wrap justify-center gap-6">
        <a class="link link-hover text-[10px] font-black uppercase tracking-widest">Medical Disclaimer</a>
        <a class="link link-hover text-[10px] font-black uppercase tracking-widest">Privacy Policy</a>
        <a class="link link-hover text-[10px] font-black uppercase tracking-widest underline decoration-blue-500 underline-offset-4 decoration-2">Terms
          of Service</a>
      </nav>
    </div>
  </footer>
</template>

<style scoped>

</style>