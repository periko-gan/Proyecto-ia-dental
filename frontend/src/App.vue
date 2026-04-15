<script setup>
</script>

<template>
<!--  <main class="min-h-screen bg-slate-950 text-slate-100 grid place-items-center px-6">-->
<!--    <section-->
<!--      class="w-full max-w-xl rounded-2xl border border-slate-800 bg-slate-900/70 p-8 shadow-xl"-->
<!--    >-->
<!--      <h1 class="text-3xl font-bold tracking-tight">Tailwind v4 listo en Vue + Vite</h1>-->
<!--      <p class="mt-3 text-slate-300">-->
<!--        Si ves este bloque con estilos, Tailwind ya estA funcionando sin <code>init -p</code>.-->
<!--      </p>-->
<!--      <a-->
<!--        href="https://tailwindcss.com/docs/installation/using-vite"-->
<!--        target="_blank"-->
<!--        rel="noopener"-->
<!--        class="mt-6 inline-flex rounded-lg bg-cyan-500 px-4 py-2 font-medium text-slate-950 hover:bg-cyan-400"-->
<!--      >-->
<!--        Ver guia oficial-->
<!--      </a>-->
<!--    </section>-->
<!--  </main>-->

  <div class="bg-surface font-body text-on-surface antialiased">
    <aside class="h-screen w-64 fixed left-0 top-0 hidden md:flex flex-col bg-slate-50 dark:bg-slate-950 shadow-[20px_0_40px_rgba(0,86,179,0.04)] z-40">
      <div class="flex flex-col h-full py-8 gap-2">
        <div class="px-6 mb-8">
          <h1 class="text-lg font-bold text-blue-900 dark:text-white font-headline">Dentis AI</h1>
        </div>
        <nav class="flex-1 space-y-1">
          <a class="flex items-center px-6 py-3 text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-900 hover:translate-x-1 transition-transform duration-200 cursor-pointer font-['Inter'] text-sm font-medium" href="#">
            <span class="material-symbols-outlined mr-3" data-icon="dashboard">dashboard</span>
            Dashboard
          </a>
          <a class="flex items-center px-6 py-3 bg-blue-50 dark:bg-cyan-900/20 text-blue-700 dark:text-cyan-400 border-l-4 border-blue-700 dark:border-cyan-500 transition-all font-['Inter'] text-sm font-medium" href="#">
            <span class="material-symbols-outlined mr-3" data-icon="clinical_notes">clinical_notes</span>
            Analyze
          </a>
          <a class="flex items-center px-6 py-3 text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-900 hover:translate-x-1 transition-transform duration-200 cursor-pointer font-['Inter'] text-sm font-medium" href="#">
            <span class="material-symbols-outlined mr-3" data-icon="history">history</span>
            History
          </a>
          <a class="flex items-center px-6 py-3 text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-900 hover:translate-x-1 transition-transform duration-200 cursor-pointer font-['Inter'] text-sm font-medium" href="#">
            <span class="material-symbols-outlined mr-3" data-icon="settings">settings</span>
            Settings
          </a>
        </nav>
        <div class="mt-auto px-6 py-6 border-t border-slate-200/50">
          <div class="flex items-center gap-3 mb-6">
            <div class="avatar">
              <div class="w-10 rounded-full">
                <img data-alt="professional portrait of a male dental surgeon" src="https://lh3.googleusercontent.com/aida-public/AB6AXuD6U4FRC9SmbBNDhZ-tJESgi2UgtW6a-5oylEeWZ1RlnjLegnAFSgs8wYqSAxuMHu9Pemhqne9uOWzjdJUt7yuJ7YmmONlaRKA31C4M8XEBqLX5-R9CLi_tjsn0barAhAp1W_nrctT5LeEMcHrUI4hhPYbeFQMdKkAOFopPQpv6lksBTGlOfe6qVuhvfRlxXmB7s3AnVhpz6o1SNg54GdxjccpXVSVO2b-e3zihYyfB-B0QW06vswwq9CXOIKWlyMqgYGqpFpGZcVOg"/>
              </div>
            </div>
            <div>
              <p class="text-xs font-bold text-on-surface">Dr. Henderson</p>
              <p class="text-[10px] text-slate-500 uppercase tracking-wider">Dental Surgeon</p>
            </div>
          </div>
          <button class="btn btn-primary btn-block btn-sm font-bold shadow-md">
            New Scan
          </button>
        </div>
      </div>
    </aside>
    <!-- TopNavBar (Shared Component) -->
    <header class="fixed top-0 w-full z-50 bg-slate-50/80 dark:bg-slate-900/80 backdrop-blur-md shadow-sm">
      <div class="flex justify-between items-center px-6 py-3 w-full max-w-full md:pl-72">
        <div class="flex items-center gap-8">
          <h2 class="text-xl font-black text-blue-900 dark:text-blue-100 font-['Manrope'] tracking-tight">Analyze</h2>
          <nav class="hidden lg:flex items-center gap-6">
            <a class="text-slate-600 dark:text-slate-400 hover:text-blue-600 dark:hover:text-cyan-300 transition-colors font-bold text-sm" href="#">Dashboard</a>
            <a class="text-blue-700 dark:text-cyan-400 border-b-2 border-blue-700 dark:border-cyan-400 pb-1 font-bold text-sm" href="#">Analyze</a>
            <a class="text-slate-600 dark:text-slate-400 hover:text-blue-600 dark:hover:text-cyan-300 transition-colors font-bold text-sm" href="#">History</a>
          </nav>
        </div>
        <div class="flex items-center gap-4">
          <div class="relative hidden sm:block">
            <input class="input input-bordered input-sm bg-surface-container-high border-none w-64 focus:ring-2 focus:ring-secondary transition-all" placeholder="Search patient data..." type="text"/>
            <span class="material-symbols-outlined absolute right-3 top-1.5 text-slate-400 text-lg" data-icon="search">search</span>
          </div>
          <div class="flex gap-2">
            <button class="btn btn-ghost btn-circle btn-sm text-slate-600">
              <span class="material-symbols-outlined" data-icon="notifications">notifications</span>
            </button>
            <button class="btn btn-ghost btn-circle btn-sm text-slate-600">
              <span class="material-symbols-outlined" data-icon="settings">settings</span>
            </button>
          </div>
        </div>
      </div>
      <div class="bg-slate-200/30 dark:bg-slate-800/30 h-[1px] w-full"></div>
    </header>
    <!-- Main Content Canvas -->
    <main class="pt-20 md:pl-64 min-h-screen flex flex-col lg:flex-row gap-0">
      <!-- Left Analysis Workspace -->
      <section class="flex-1 p-6 md:p-10 flex flex-col items-center">
        <div class="w-full max-w-4xl space-y-8">
          <div class="flex justify-between items-end">
            <div>
              <h3 class="font-headline text-3xl font-extrabold text-primary mb-2">Clinical Image Analysis</h3>
              <p class="text-on-surface-variant font-medium">Upload intraoral photos or radiographic scans for AI diagnostic support.</p>
            </div>
            <div class="flex gap-3">
              <div class="badge badge-secondary badge-outline gap-2 p-3 font-bold uppercase tracking-widest text-[10px]">
                <span class="w-2 h-2 bg-secondary rounded-full animate-pulse"></span>
                AI System Ready
              </div>
            </div>
          </div>
          <!-- Drag & Drop Zone -->
          <div class="relative group">
            <div class="border-2 border-dashed border-outline-variant bg-surface-container-low rounded-xl p-8 flex flex-col items-center justify-center transition-all hover:bg-surface-container-lowest hover:border-primary cursor-pointer min-h-[450px]">
              <!-- Upload Prompt -->
              <div class="flex flex-col items-center text-center space-y-6 w-full max-w-md">
                <div class="w-20 h-20 bg-primary-container/10 rounded-full flex items-center justify-center group-hover:scale-110 transition-transform">
                  <span class="material-symbols-outlined text-primary text-4xl" data-icon="cloud_upload">cloud_upload</span>
                </div>
                <div class="space-y-2">
                  <h4 class="text-xl font-bold text-on-surface font-headline">Drag &amp; Drop clinical media</h4>
                  <p class="text-on-surface-variant text-sm">Support for DICOM, JPEG, and PNG files. Max 25MB per file.</p>
                </div>
                <!-- DaisyUI File Input -->
                <div class="form-control w-full">
                  <input class="file-input file-input-bordered file-input-primary w-full shadow-sm" type="file"/>
                </div>
                <div class="divider text-[10px] font-bold text-slate-400 uppercase tracking-widest">or</div>
                <button class="btn btn-primary btn-wide font-bold gap-2">
                  <span class="material-symbols-outlined" data-icon="upload_file">upload_file</span>
                  Browse Files
                </button>
              </div>
            </div>
          </div>
          <!-- Bento Grid Tools -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="card bg-surface-container-low border-l-4 border-secondary shadow-sm">
              <div class="card-body p-5 flex-row items-center gap-4">
                <div class="p-2 bg-secondary/10 rounded-lg">
                  <span class="material-symbols-outlined text-secondary" data-icon="auto_awesome">auto_awesome</span>
                </div>
                <div>
                  <p class="text-xs font-bold text-on-surface">Precision Scan</p>
                  <p class="text-[10px] text-on-surface-variant">Enhanced caries detection enabled</p>
                </div>
              </div>
            </div>
            <div class="card bg-surface-container-low shadow-sm">
              <div class="card-body p-5 flex-row items-center gap-4">
                <div class="p-2 bg-slate-200 rounded-lg">
                  <span class="material-symbols-outlined text-slate-600" data-icon="history">history</span>
                </div>
                <div>
                  <p class="text-xs font-bold text-on-surface">Patient History</p>
                  <p class="text-[10px] text-on-surface-variant">Comparison mode available</p>
                </div>
              </div>
            </div>
            <div class="card bg-surface-container-low shadow-sm">
              <div class="card-body p-5 flex-row items-center gap-4">
                <div class="p-2 bg-slate-200 rounded-lg">
                  <span class="material-symbols-outlined text-slate-600" data-icon="share">share</span>
                </div>
                <div>
                  <p class="text-xs font-bold text-on-surface">Export Data</p>
                  <p class="text-[10px] text-on-surface-variant">Cloud sync with EMR active</p>
                </div>
              </div>
            </div>
          </div>
          <!-- AI Progress Alert (Hidden by default, shown for logic showcase) -->
          <div class="alert alert-info shadow-lg bg-blue-50 border-blue-100 hidden">
            <span class="material-symbols-outlined text-blue-600" data-icon="info">info</span>
            <div class="flex-1">
              <h3 class="font-bold text-sm text-blue-900">Neural Network Active</h3>
              <div class="text-xs text-blue-700">Analyzing pathology patterns... 78% Complete</div>
              <progress class="progress progress-primary w-full mt-2" max="100" value="78"></progress>
            </div>
            <button class="btn btn-sm btn-ghost">Cancel</button>
          </div>
        </div>
      </section>
      <!-- Right Side Panel: Visual Guide -->
      <aside class="w-full lg:w-[400px] bg-slate-50 dark:bg-slate-900 border-l border-slate-200/50 p-8 space-y-8 lg:min-h-screen">
        <div class="space-y-2">
          <span class="text-[10px] font-bold text-secondary uppercase tracking-widest">Protocol Guide</span>
          <h4 class="font-headline text-2xl font-extrabold text-blue-900">Clinical Visual Guide</h4>
          <p class="text-sm text-on-surface-variant">Ensure high-fidelity analysis by following these imaging protocols.</p>
        </div>
        <!-- DaisyUI Steps -->
        <div class="mt-8">
          <ul class="steps steps-vertical w-full space-y-8">
            <li class="step step-primary" data-content="✓">
              <div class="text-left w-full pl-4">
                <div class="flex justify-between items-center mb-3">
                  <h5 class="text-sm font-bold text-blue-900">Optimal Lighting</h5>
                </div>
                <div class="relative h-32 rounded-lg overflow-hidden shadow-sm mb-3">
                  <img class="w-full h-full object-cover" data-alt="bright clinical lighting setup" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCYRDCzIwcyNHwte-xRrMqAIP5HWcLdPrJjVRLqV-HbJKP4_Hz_z6-rIVc2HkAqJawLWbmwUxqh9jRz32O5zxEeTHAwM9FAbZ4l4UjIOfxK0JyyRLR-DrzQCgpQx0BGyW4kO5pLVa-EusF7u6tTySIywxiHfqZgHIfPxoIoxsWWRJtU1P3jtI_-wohvP7ZO4GUx5g9yvD33s71qh1vvMULPuhuSwZObf2N0ONr9kXpkQ867WaOKd0K30On1N1NO3VUelUAnZcClF3KC"/>
                  <div class="absolute bottom-2 left-2 px-2 py-1 bg-black/60 backdrop-blur-md rounded text-[9px] text-white font-bold uppercase">Soft Neutral Light</div>
                </div>
                <p class="text-[11px] text-on-surface-variant leading-relaxed">Avoid direct flash on shiny surfaces. Use secondary, diffused white light sources.</p>
              </div>
            </li>
            <li class="step">
              <div class="text-left w-full pl-4">
                <div class="flex justify-between items-center mb-3">
                  <h5 class="text-sm font-bold text-blue-900">Correct Angle</h5>
                </div>
                <div class="relative h-32 rounded-lg overflow-hidden shadow-sm mb-3">
                  <img class="w-full h-full object-cover" data-alt="side view macro photography of dental models" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBNiCvKzHNUdRE0SDToBoiq0uv3Igb9XjSlBQXFYzCJ-s-t10M4r8blCDW0fjBpCnQHCOzb3Vd18n_d8eq5S74LF_A46jvnjh7xmLA_ak_WVPPLmfpHchVFek7EY4f6Yy6Loxi3isbpba7r4pZts4QSJEl4NKGnTnOd-02-biXcK0rVgBc52ZKupMsMDtPvKmz6NCjvZe0z1A0a0WkGwy0VsOA9ooYbYQMRNTXMe3SvERE-ygm37stTyfQs_bEq43EC9j3TfTwcHaCj"/>
                  <div class="absolute bottom-2 left-2 px-2 py-1 bg-black/60 backdrop-blur-md rounded text-[9px] text-white font-bold uppercase">Orthogonal View</div>
                </div>
                <p class="text-[11px] text-on-surface-variant leading-relaxed">Capture images perpendicular to the tooth surface. Maintain horizontal occlusal plane.</p>
              </div>
            </li>
            <li class="step">
              <div class="text-left w-full pl-4">
                <div class="flex justify-between items-center mb-3">
                  <h5 class="text-sm font-bold text-blue-900">Focus Calibration</h5>
                </div>
                <div class="alert bg-white/50 border-slate-200 p-3 rounded-lg flex items-center gap-4">
                  <span class="material-symbols-outlined text-primary text-2xl" data-icon="center_focus_weak">center_focus_weak</span>
                  <p class="text-[11px] text-on-surface-variant">The AI requires min 300 DPI. Use optical focus lock.</p>
                </div>
              </div>
            </li>
          </ul>
        </div>
        <!-- Support Module / DaisyUI Alert Style -->
        <div class="card bg-primary text-primary-content shadow-xl mt-8">
          <div class="card-body p-6 gap-4">
            <p class="text-[10px] font-bold uppercase tracking-widest opacity-80">Professional Verification</p>
            <p class="text-sm font-medium leading-relaxed">AI results are advisory. Always cross-reference with tactile clinical exams.</p>
            <div class="card-actions">
              <button class="btn btn-block btn-sm btn-neutral bg-white text-primary border-none hover:bg-slate-100 font-bold uppercase tracking-tight">
                Request Manual Review
              </button>
            </div>
          </div>
        </div>
      </aside>
    </main>
    <!-- Footer (Shared Component) -->
    <footer class="w-full py-8 mt-auto bg-slate-50 dark:bg-slate-950 border-t border-slate-200/50 dark:border-slate-800/50 md:pl-64">
      <div class="flex flex-col md:flex-row justify-between items-center px-8 gap-6">
        <p class="font-['Inter'] text-[10px] uppercase tracking-widest text-slate-400 dark:text-slate-600">
          © 2024 Dentis AI Clinical Systems. All AI diagnostics require professional verification.
        </p>
        <div class="flex gap-6">
          <a class="font-['Inter'] text-[10px] uppercase tracking-widest text-slate-400 hover:text-blue-500 transition-all opacity-80 hover:opacity-100" href="#">Medical Disclaimer</a>
          <a class="font-['Inter'] text-[10px] uppercase tracking-widest text-slate-400 hover:text-blue-500 transition-all opacity-80 hover:opacity-100" href="#">Privacy Policy</a>
          <a class="font-['Inter'] text-[10px] uppercase tracking-widest text-slate-400 hover:text-blue-500 transition-all opacity-80 hover:opacity-100" href="#">Terms of Service</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<style>
.material-symbols-outlined {
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}
.scan-line {
  height: 2px;
  background: linear-gradient(90deg, transparent, #22d3ee, transparent);
  box-shadow: 0 0 15px #22d3ee;
  position: absolute;
  width: 100%;
  top: 0;
  z-index: 20;
}
.glass-panel {
  backdrop-filter: blur(12px);
  background: rgba(15, 23, 42, 0.8);
}
</style>