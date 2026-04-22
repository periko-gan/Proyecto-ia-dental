<script setup>

import Header from "@/components/parts/all_pages/Header.vue";
import Footer from "@/components/parts/all_pages/Footer.vue";
import Aside from "@/components/parts/all_pages/Aside.vue";
</script>

<template>
<!--  <div class="bg-surface text-on-surface selection:bg-secondary-container/30">-->
  <div class="bg-surface font-body text-on-surface">

    <Header/>

    <Aside/>

    <main class="">
<!--    <section class="hidden md:flex w-1/2 relative overflow-hidden bg-primary items-center justify-center p-12">-->
<!--      <div class="absolute inset-0 z-0">-->
<!--        <img alt="Clinical laboratory environment" class="w-full h-full object-cover opacity-30 grayscale" data-alt="modern dental clinic interior with blue accent lighting, high-tech diagnostic equipment, clinical and sterile aesthetic" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBxVh9KQ-vGzeD_wOXvo_ANiNnIa4bVf-PDQZCxcE0Pb1fiB_BeXOt9HUo46M144mfRJQ9ZVmBDcwRrHR1CgIqynw5DDldvChze3lSNYAFf8_XZPsPQ1vRE_fVsdc9dt2_ZCcihEYuLVZcOD1fM-5HQr9FvCBJhLyHFcOEZx-qHFanY4U3NMj4XzFjZq8NmZBgWImw7OR_J2zDXD-fl5HLTT4xZN-9SsMbgqcxbrC672OeBmnC2rei2qK48k3o6Qs39IUSzNAlGTuVX"/>-->
<!--      </div>-->
<!--      <div class="relative z-10 w-full max-w-lg">-->
<!--        <div class="mb-12">-->
<!--<span class="inline-flex items-center gap-2 px-3 py-1 bg-secondary-container text-on-secondary-container text-[0.6875rem] font-bold tracking-widest uppercase rounded-full mb-6">-->
<!--<span class="material-symbols-outlined text-sm" data-icon="clinical_notes">clinical_notes</span>-->
<!--                        Clinical Precision-->
<!--                    </span>-->
<!--          <h1 class="text-display-lg text-5xl font-extrabold text-white leading-tight tracking-tight mb-6">-->
<!--            Revolutionizing <br/> <span class="text-secondary-container">Radiology</span> with AI.-->
<!--          </h1>-->
<!--          <p class="text-primary-fixed-dim text-lg leading-relaxed max-w-md">-->
<!--            Empower your practice with DentaVision AI's advanced diagnostic suite. Join thousands of clinical professionals today.-->
<!--          </p>-->
<!--        </div>-->
<!--        <div class="grid grid-cols-2 gap-4">-->
<!--          <div class="p-6 bg-white/5 backdrop-blur-md rounded-xl border-l-2 border-secondary-container">-->
<!--            <div class="text-white font-bold text-2xl mb-1">99.8%</div>-->
<!--            <div class="text-primary-fixed-dim text-xs uppercase tracking-wider font-semibold">Scan Accuracy</div>-->
<!--          </div>-->
<!--          <div class="p-6 bg-white/5 backdrop-blur-md rounded-xl border-l-2 border-secondary-container">-->
<!--            <div class="text-white font-bold text-2xl mb-1">2.4s</div>-->
<!--            <div class="text-primary-fixed-dim text-xs uppercase tracking-wider font-semibold">Detection Speed</div>-->
<!--          </div>-->
<!--        </div>-->
<!--      </div>-->
<!--    </section>-->
    <section class="flex-1 flex flex-col justify-center items-center p-6 md:p-16 lg:p-24 bg-surface">
      <div class="w-full max-w-md">
        <div class="mb-10">
          <div class="flex items-center gap-2 mb-8">
            <div class="w-10 h-10 tech-gradient rounded-md flex items-center justify-center">
              <span class="material-symbols-outlined text-white" data-icon="dentistry" style="font-variation-settings: 'FILL' 1;">dentistry</span>
            </div>
            <span class="text-2xl font-extrabold tracking-tighter text-primary">DentaVision AI</span>
          </div>
          <h2 class="text-3xl font-bold text-on-surface mb-2">Create Professional Account</h2>
          <p class="text-on-surface-variant text-sm">Please provide your clinical credentials to begin.</p>
        </div>
        <form class="space-y-5">
          <div class="grid grid-cols-1 gap-5">
            <div class="group">
              <label class="block text-[0.6875rem] font-bold uppercase tracking-wider text-outline mb-1.5 ml-1 transition-colors group-focus-within:text-secondary">Full Name</label>
              <input class="w-full bg-surface-container-high border-0 rounded-lg px-4 py-3.5 text-on-surface placeholder:text-outline/50 focus:ring-0 focus:bg-surface-container-lowest transition-all border-l-2 border-transparent focus:border-secondary" placeholder="Dr. Jane Smith" type="text"/>
            </div>
<!--            <div class="group">-->
<!--              <label class="block text-[0.6875rem] font-bold uppercase tracking-wider text-outline mb-1.5 ml-1 transition-colors group-focus-within:text-secondary">Clinic Name</label>-->
<!--              <input class="w-full bg-surface-container-high border-0 rounded-lg px-4 py-3.5 text-on-surface placeholder:text-outline/50 focus:ring-0 focus:bg-surface-container-lowest transition-all border-l-2 border-transparent focus:border-secondary" placeholder="City Dental Associates" type="text"/>-->
<!--            </div>-->
<!--            <div class="group">-->
<!--              <label class="block text-[0.6875rem] font-bold uppercase tracking-wider text-outline mb-1.5 ml-1 transition-colors group-focus-within:text-secondary">Professional License Number</label>-->
<!--              <input class="w-full bg-surface-container-high border-0 rounded-lg px-4 py-3.5 text-on-surface placeholder:text-outline/50 focus:ring-0 focus:bg-surface-container-lowest transition-all border-l-2 border-transparent focus:border-secondary" placeholder="DEN-091823-X" type="text"/>-->
<!--            </div>-->
<!--            <div class="group">-->
<!--              <label class="block text-[0.6875rem] font-bold uppercase tracking-wider text-outline mb-1.5 ml-1 transition-colors group-focus-within:text-secondary">Specialization</label>-->
<!--              <div class="relative">-->
<!--                <select class="w-full bg-surface-container-high border-0 rounded-lg px-4 py-3.5 text-on-surface focus:ring-0 focus:bg-surface-container-lowest appearance-none transition-all border-l-2 border-transparent focus:border-secondary">-->
<!--                  <option disabled="" selected="" value="">Select practice area</option>-->
<!--                  <option value="general">General Dentistry</option>-->
<!--                  <option value="orthodontics">Orthodontics</option>-->
<!--                  <option value="periodontics">Periodontics</option>-->
<!--                  <option value="endodontics">Endodontics</option>-->
<!--                  <option value="radiology">Oral &amp; Maxillofacial Radiology</option>-->
<!--                </select>-->
<!--                <span class="material-symbols-outlined absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-outline-variant" data-icon="keyboard_arrow_down">keyboard_arrow_down</span>-->
<!--              </div>-->
<!--            </div>-->
            <div class="group">
              <label class="block text-[0.6875rem] font-bold uppercase tracking-wider text-outline mb-1.5 ml-1 transition-colors group-focus-within:text-secondary">Email Address</label>
              <input class="w-full bg-surface-container-high border-0 rounded-lg px-4 py-3.5 text-on-surface placeholder:text-outline/50 focus:ring-0 focus:bg-surface-container-lowest transition-all border-l-2 border-transparent focus:border-secondary" placeholder="professional@clinic.com" type="email"/>
            </div>
            <div class="group">
              <label class="block text-[0.6875rem] font-bold uppercase tracking-wider text-outline mb-1.5 ml-1 transition-colors group-focus-within:text-secondary">Password</label>
              <div class="relative">
                <input class="w-full bg-surface-container-high border-0 rounded-lg px-4 py-3.5 text-on-surface placeholder:text-outline/50 focus:ring-0 focus:bg-surface-container-lowest transition-all border-l-2 border-transparent focus:border-secondary" placeholder="••••••••" type="password"/>
                <span class="material-symbols-outlined absolute right-4 top-1/2 -translate-y-1/2 cursor-pointer text-outline-variant hover:text-secondary transition-colors" data-icon="visibility">visibility</span>
              </div>
            </div>
          </div>
          <div class="flex items-center gap-3 pt-2">
            <input class="rounded-sm border-outline-variant text-primary focus:ring-primary h-4 w-4" id="terms" type="checkbox"/>
            <label class="text-xs text-on-surface-variant" for="terms">I agree to the <a class="text-primary font-semibold hover:underline" href="#">Terms of Service</a> and <a class="text-primary font-semibold hover:underline" href="#">Clinical Data Protocols</a>.</label>
          </div>
          <div class="pt-4">
            <button class="w-full bg-primary text-on-primary py-4 px-6 rounded-lg font-bold clinical-shadow hover:bg-primary-container active:scale-[0.98] transition-all flex items-center justify-center gap-2 group" type="submit">
              Sign Up
              <span class="material-symbols-outlined group-hover:translate-x-1 transition-transform" data-icon="arrow_forward">arrow_forward</span>
            </button>
          </div>
        </form>
        <div class="mt-8 pt-8 border-t border-outline-variant/15 text-center">
          <p class="text-sm text-on-surface-variant">
            Already have an account?
            <a class="text-secondary font-bold hover:text-on-secondary-container transition-colors ml-1" href="#">Log in</a>
          </p>
        </div>
      </div>
    </section>
  </main>

    <Footer/>

  </div>
</template>

<style scoped>

</style>