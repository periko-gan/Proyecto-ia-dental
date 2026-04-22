<script setup>
import Header from "@/components/parts/all_pages/Header.vue";
import Footer from "@/components/parts/all_pages/Footer.vue";
</script>

<template>
  <div class="bg-surface font-body text-on-surface">
    <!-- Top Navigation Shell -->
    <Header/>
    <main class="pt-20">
      <!-- Hero Section -->
      <section class="relative min-h-[921px] flex items-center overflow-hidden bg-surface">
        <div class="absolute inset-0 z-0 opacity-10">
          <div
              class="absolute top-0 right-0 w-[800px] h-[800px] bg-secondary-container rounded-full blur-[120px] -translate-y-1/2 translate-x-1/3"></div>
          <div
              class="absolute bottom-0 left-0 w-[600px] h-[600px] bg-primary-fixed rounded-full blur-[100px] translate-y-1/3 -translate-x-1/4"></div>
        </div>
        <div class="max-w-7xl mx-auto px-8 w-full grid grid-cols-1 lg:grid-cols-12 gap-12 items-center relative z-10">
          <div class="lg:col-span-7 space-y-8">
            <div
                class="inline-flex items-center gap-2 px-3 py-1 bg-secondary-container/30 text-secondary font-bold text-[0.6875rem] uppercase tracking-[0.1em] rounded-full border border-secondary/20">
                <span class="relative flex h-2 w-2">
                  <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-secondary opacity-75"></span>
                  <span class="relative inline-flex rounded-full h-2 w-2 bg-secondary"></span>
                </span>
              Next-Gen Clinical Intelligence
            </div>
            <h1 class="font-headline text-5xl lg:text-7xl font-extrabold text-primary leading-[1.1] tracking-tight">
              AI-Driven Precision <br/> For Every <span class="text-secondary">Diagnosis.</span>
            </h1>
            <p class="font-body text-xl text-on-surface-variant max-w-xl leading-relaxed">
              Elevate your practice with clinical-grade AI that identifies pathologies with 98% accuracy.
              Streamline workflows and enhance patient trust through visual evidence.
            </p>
            <div class="flex flex-wrap gap-4">
              <button
                  class="bg-primary text-on-primary px-8 py-4 rounded-md font-bold text-lg active:scale-95 transform transition-transform duration-150 shadow-[0_10px_25px_rgba(0,63,135,0.25)] flex items-center gap-2">
                Request Demo
                <span class="material-symbols-outlined" data-icon="arrow_forward">arrow_forward</span>
              </button>
              <button
                  class="bg-surface-container-lowest text-primary border border-outline-variant/30 px-8 py-4 rounded-md font-bold text-lg hover:bg-surface-container-low transition-colors">
                Watch Video
              </button>
            </div>
          </div>
          <div class="lg:col-span-5 relative">
            <div
                class="relative rounded-xl overflow-hidden shadow-[0_30px_60px_rgba(0,86,179,0.12)] border border-outline-variant/40">
              <img alt="Modern dental clinic with high-tech equipment and digital screens"
                   class="w-full h-[500px] object-cover"
                   data-alt="high-tech dental surgery room with professional digital diagnostic screens displaying 3D dental scans in soft surgical blue lighting"
                   src="https://lh3.googleusercontent.com/aida-public/AB6AXuBCDqTOppee_a9O-r6fA179lZaNXP66th7gFZXYWYNl14V7cDq_G1LCnow1iJqnnA297d_gj5E9ZbhH8DzZM4a93XPLxyC1HezaPsizaAthIkF7JD1sP6JZqBcw8watujlk-HnCKrRek-sGJxYFM5iaaDZf9paanSM1DtQ01rA1dgbRMDW00KTJ_nGrqpUyEqP1Osll82axgLBTReSGOIWnkgyY8KY4rBufRu_Ex8xr6NxaGCEMNWDbwqn2NMQuZNHfFb0Lg_H2bytt"/>
              <div class="absolute inset-0 bg-gradient-to-t from-primary/35 to-transparent"></div>
              <!-- AI Overlay Mockup -->
              <div class="absolute top-6 left-6 right-6">
                <div class="glass-panel p-4 rounded-lg border border-white/40 shadow-xl">
                  <div class="flex items-center justify-between mb-3">
                    <div class="flex items-center gap-2">
                      <div class="w-2 h-2 rounded-full bg-secondary animate-pulse"></div>
                      <span
                          class="text-[10px] font-bold text-on-surface tracking-widest uppercase">AI Scanning Active</span>
                    </div>
                    <span class="text-[10px] font-bold text-secondary">98.4% Confidence</span>
                  </div>
                  <div class="h-1 bg-surface-container-high rounded-full overflow-hidden">
                    <div class="h-full bg-secondary w-4/5"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
      <!-- Trust Bar -->
      <section class="py-12 bg-surface-container-low border-y border-outline-variant/10">
        <div class="max-w-7xl mx-auto px-8">
          <div
              class="flex flex-col md:flex-row items-center justify-between gap-12 opacity-60 grayscale hover:grayscale-0 transition-all duration-500">
            <div class="flex items-center gap-3">
              <div class="bg-primary/10 p-2 rounded-md">
                        <span class="material-symbols-outlined text-primary"
                              data-icon="verified_user">verified_user</span>
              </div>
              <span class="font-bold text-primary tracking-tight">HIPAA COMPLIANT</span>
            </div>
            <div class="flex flex-wrap justify-center items-center gap-12">
              <div class="text-xl font-black text-on-surface-variant font-manrope">DENTACLOUD</div>
              <div class="text-xl font-black text-on-surface-variant font-manrope">ORALTECH</div>
              <div class="text-xl font-black text-on-surface-variant font-manrope">PRECISIONMED</div>
              <div class="text-xl font-black text-on-surface-variant font-manrope">VITALSCAN</div>
            </div>
          </div>
        </div>
      </section>
      <!-- Features Section -->
      <section class="py-24 bg-surface">
        <div class="max-w-7xl mx-auto px-8">
          <div class="mb-16 max-w-2xl">
            <h2 class="font-headline text-3xl font-bold text-primary mb-4">Precision Engineering for Modern
              Clinics</h2>
            <p class="text-on-surface-variant font-medium">Industry-leading diagnostic tools designed to minimize human
              error
              and maximize patient outcome.</p>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <!-- Feature 1 -->
            <div
                class="group p-8 rounded-xl bg-surface-container-lowest border border-outline-variant/30 hover:border-secondary/40 transition-all duration-300 shadow-[0_10px_30px_rgba(0,0,0,0.02)]">
              <div
                  class="w-14 h-14 bg-secondary-container/20 rounded-lg flex items-center justify-center mb-6 text-secondary">
                        <span class="material-symbols-outlined text-3xl" data-icon="query_stats" data-weight="fill"
                              style="font-variation-settings: 'FILL' 1;">query_stats</span>
              </div>
              <h3 class="font-headline text-xl font-bold text-primary mb-3">Automated Analysis</h3>
              <p class="text-on-surface-variant leading-relaxed text-sm">Real-time detection of caries, bone loss, and
                periapical lesions from standard X-rays and 3D scans.</p>
            </div>
            <!-- Feature 2 -->
            <div
                class="group p-8 rounded-xl bg-surface-container-lowest border border-outline-variant/30 hover:border-secondary/40 transition-all duration-300 shadow-[0_10px_30px_rgba(0,0,0,0.02)]">
              <div
                  class="w-14 h-14 bg-secondary-container/20 rounded-lg flex items-center justify-center mb-6 text-secondary">
                        <span class="material-symbols-outlined text-3xl" data-icon="timeline" data-weight="fill"
                              style="font-variation-settings: 'FILL' 1;">timeline</span>
              </div>
              <h3 class="font-headline text-xl font-bold text-primary mb-3">Patient Evolution Tracking</h3>
              <p class="text-on-surface-variant leading-relaxed text-sm">Visual time-lapse comparison showing disease
                progression or recovery markers over multiple visits.</p>
            </div>
            <!-- Feature 3 -->
            <div
                class="group p-8 rounded-xl bg-surface-container-lowest border border-outline-variant/30 hover:border-secondary/40 transition-all duration-300 shadow-[0_10px_30px_rgba(0,0,0,0.02)]">
              <div
                  class="w-14 h-14 bg-secondary-container/20 rounded-lg flex items-center justify-center mb-6 text-secondary">
                        <span class="material-symbols-outlined text-3xl" data-icon="encrypted" data-weight="fill"
                              style="font-variation-settings: 'FILL' 1;">encrypted</span>
              </div>
              <h3 class="font-headline text-xl font-bold text-primary mb-3">Secure Data Management</h3>
              <p class="text-on-surface-variant leading-relaxed text-sm">Enterprise-grade encryption with multi-region
                cloud storage ensuring total HIPAA and GDPR compliance.</p>
            </div>
          </div>
        </div>
      </section>
      <!-- Clinical Workflow Section -->
      <section class="py-24 bg-surface-container-low relative overflow-hidden">
        <div class="max-w-7xl mx-auto px-8 relative z-10">
          <div class="text-center mb-20">
            <span
                class="font-label text-xs font-bold text-secondary tracking-widest uppercase mb-4 block">The Workflow</span>
            <h2 class="font-headline text-4xl font-bold text-primary">Seamless Integration</h2>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-16 relative">
            <!-- Connector Line (Desktop Only) -->
            <div
                class="hidden md:block absolute top-12 left-[15%] right-[15%] h-px bg-gradient-to-r from-transparent via-outline-variant/30 to-transparent"></div>
            <!-- Step 1 -->
            <div class="flex flex-col items-center text-center group">
              <div
                  class="w-24 h-24 rounded-full bg-surface-container-lowest border-4 border-surface shadow-xl flex items-center justify-center mb-8 relative z-10 group-hover:scale-110 transition-transform">
                <span class="material-symbols-outlined text-4xl text-primary" data-icon="upload_file">upload_file</span>
              </div>
              <h4 class="font-headline text-lg font-bold text-primary mb-3">1. Upload</h4>
              <p class="text-on-surface-variant text-sm max-w-[240px]">Direct integration with your current imaging
                software for instant upload.</p>
            </div>
            <!-- Step 2 -->
            <div class="flex flex-col items-center text-center group">
              <div
                  class="w-24 h-24 rounded-full bg-primary border-4 border-surface shadow-[0_0_40px_rgba(0,63,135,0.3)] flex items-center justify-center mb-8 relative z-10 group-hover:scale-110 transition-transform">
                <span class="material-symbols-outlined text-4xl text-on-primary" data-icon="memory">memory</span>
              </div>
              <h4 class="font-headline text-lg font-bold text-primary mb-3">2. AI Processing</h4>
              <p class="text-on-surface-variant text-sm max-w-[240px]">Proprietary neural networks analyze scans in
                under
                10 seconds with clinical precision.</p>
            </div>
            <!-- Step 3 -->
            <div class="flex flex-col items-center text-center group">
              <div
                  class="w-24 h-24 rounded-full bg-surface-container-lowest border-4 border-surface shadow-xl flex items-center justify-center mb-8 relative z-10 group-hover:scale-110 transition-transform">
                <span class="material-symbols-outlined text-4xl text-primary" data-icon="rate_review">rate_review</span>
              </div>
              <h4 class="font-headline text-lg font-bold text-primary mb-3">3. Professional Review</h4>
              <p class="text-on-surface-variant text-sm max-w-[240px]">Review findings on a clear dashboard and finalize
                treatment plans with confidence.</p>
            </div>
          </div>
        </div>
      </section>
      <!-- Testimonial Section -->
      <section class="py-24 bg-surface">
        <div class="max-w-5xl mx-auto px-8">
          <div
              class="glass-panel p-12 rounded-2xl border border-outline-variant/20 shadow-2xl relative overflow-hidden">
            <div class="absolute -top-10 -left-10 text-9xl text-primary/5 font-serif">“</div>
            <div class="relative z-10">
              <div class="flex items-center gap-1 mb-8">
                        <span class="material-symbols-outlined text-secondary" data-icon="star" data-weight="fill"
                              style="font-variation-settings: 'FILL' 1;">star</span>
                <span class="material-symbols-outlined text-secondary" data-icon="star" data-weight="fill"
                      style="font-variation-settings: 'FILL' 1;">star</span>
                <span class="material-symbols-outlined text-secondary" data-icon="star" data-weight="fill"
                      style="font-variation-settings: 'FILL' 1;">star</span>
                <span class="material-symbols-outlined text-secondary" data-icon="star" data-weight="fill"
                      style="font-variation-settings: 'FILL' 1;">star</span>
                <span class="material-symbols-outlined text-secondary" data-icon="star" data-weight="fill"
                      style="font-variation-settings: 'FILL' 1;">star</span>
              </div>
              <p class="font-headline text-2xl lg:text-3xl text-primary font-medium leading-snug mb-8 italic">
                "Dentis AI has transformed how I communicate findings to my patients. The automated analysis
                provides a level of technical rigor and visual proof that builds immediate trust. It’s no longer
                just my opinion—it’s verified clinical data."
              </p>
              <div class="flex items-center gap-4">
                <div class="w-16 h-16 rounded-full overflow-hidden border-2 border-secondary-container">
                  <img alt="Dr. Julian Reed, Oral Surgeon" class="w-full h-full object-cover"
                       data-alt="headshot of a middle-aged male dental surgeon in clinical blue scrubs with a professional and friendly expression"
                       src="https://lh3.googleusercontent.com/aida-public/AB6AXuBmrNQFpbGqJaw0caD0DcKS95Ks0hzY4aPhh9JZEdTbZKDa7QcKu0xdGcbWLirWDnXJrVU9ZhBl8fSb_BmO5TAQqQleytQHDIdGHQXunkjQI7zxxj4FYJ2NdlaZW6f4ppKKhnhIsyGAD5TIosOSTybTQEvI6leVoOPWkKZF1dKgEchbu6OsYXdiLLVPEmDJ9hz0jvz-hWZ5QuYdD5tVHpOKNCQzKEruH9647Y16rB5iKfMPkwQeI88mXrzqQNzXgxRkTMSj9AhwrKv2"/>
                </div>
                <div>
                  <h5 class="font-headline font-bold text-primary">Dr. Julian Reed, DDS</h5>
                  <p class="text-sm text-on-surface-variant font-medium">Chief of Oral Surgery, Metro Dental
                    Specialists</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
      <!-- CTA Section -->
      <section class="py-24 bg-primary text-on-primary">
        <div class="max-w-7xl mx-auto px-8 text-center">
          <h2 class="font-headline text-4xl lg:text-5xl font-bold mb-6">Ready to upgrade your clinical workflow?</h2>
          <p class="text-on-primary/80 text-xl mb-12 max-w-2xl mx-auto">Join over 1,200 clinics worldwide who trust
            Dentis AI for their diagnostic precision.</p>
          <div class="flex flex-col sm:flex-row justify-center gap-4">
            <button
                class="bg-secondary-container text-on-secondary-container px-10 py-5 rounded-md font-bold text-lg shadow-xl hover:scale-105 transition-transform">
              Schedule Personal Demo
            </button>
            <button
                class="bg-transparent border-2 border-on-primary/30 hover:bg-on-primary/10 px-10 py-5 rounded-md font-bold text-lg transition-colors">
              View Case Studies
            </button>
          </div>
        </div>
      </section>
    </main>
    <!-- Footer -->
    <Footer/>
  </div>
</template>

<style scoped>
</style>

