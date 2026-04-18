<script setup>

</script>

<template>
  <aside
      class="w-64 h-full  fixed top-20 left-0 hidden md:flex flex-col bg-white border-r border-slate-200 z-40 transition-all">
    <div class="px-6 py-6 border-t border-slate-200/50">
      <div class="flex items-center gap-3 mb-6">
        <div class="avatar">
          <div class="w-10 rounded-full">
            <img data-alt="professional portrait of a male dental surgeon"
                 src="https://lh3.googleusercontent.com/aida-public/AB6AXuD6U4FRC9SmbBNDhZ-tJESgi2UgtW6a-5oylEeWZ1RlnjLegnAFSgs8wYqSAxuMHu9Pemhqne9uOWzjdJUt7yuJ7YmmONlaRKA31C4M8XEBqLX5-R9CLi_tjsn0barAhAp1W_nrctT5LeEMcHrUI4hhPYbeFQMdKkAOFopPQpv6lksBTGlOfe6qVuhvfRlxXmB7s3AnVhpz6o1SNg54GdxjccpXVSVO2b-e3zihYyfB-B0QW06vswwq9CXOIKWlyMqgYGqpFpGZcVOg"/>
          </div>
        </div>
        <div>
          <p class="text-xs font-bold text-on-surface">Dr. Henderson</p>
          <p class="text-[10px] text-slate-500 uppercase tracking-wider">Dental Surgeon</p>
        </div>
      </div>
    </div>
    <nav class="p-6">
      <ul class="menu menu-md w-full p-0 gap-1">
        <li>
          <router-link :to="{name: 'Dashboard'}"
                       class="active bg-blue-50 text-blue-700 font-bold border-r-4 border-blue-700 rounded-none">
            <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">Dashboard</span>
          </router-link>
        </li>
        <li>
          <router-link :to="{name: 'Analyze'}" class="text-slate-500 hover:text-blue-700">
            <span class="material-symbols-outlined">Analyze</span>
          </router-link>
        </li>
        <li>
          <router-link :to="{name: 'Diagnostic'}" class="text-slate-500 hover:text-blue-700">
            <span class="material-symbols-outlined">Diagnostic</span>
          </router-link>
        </li>
        <li>
          <router-link :to="{name: 'Evolution'}" class="text-slate-500 hover:text-blue-700">
            <span class="material-symbols-outlined">Evolution</span>
          </router-link>
        </li>
      </ul>
    </nav>

  </aside>
</template>

<style scoped>

</style>