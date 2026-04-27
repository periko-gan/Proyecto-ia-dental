<script setup>
// Contenedor de login: reutiliza Formulario indicando page="login".

import Header from "@/components/parts/all_pages/Header.vue";
import Footer from "@/components/parts/all_pages/Footer.vue";
import Aside from "@/components/parts/all_pages/Aside.vue";
import Formulario from "@/components/parts/Formulario.vue";
</script>

<template>
  <!--  <div class="bg-surface text-on-surface selection:bg-secondary-container/30">-->
  <div class="bg-surface font-body text-on-surface">

    <Header/>

    <Aside/>

    <Formulario page="login"/>

    <Footer/>

  </div>
</template>

<style scoped>

</style>
