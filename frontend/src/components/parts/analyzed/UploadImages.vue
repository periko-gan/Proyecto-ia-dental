<script setup>

</script>

<template>
  <div
      class="border-2 border-dashed border-outline-variant bg-surface-container-low rounded-xl p-8 flex flex-col items-center justify-center transition-all hover:bg-surface-container-lowest hover:border-primary cursor-pointer min-h-[450px]">
    <!-- Upload Prompt -->
    <div class="flex flex-col items-center text-center space-y-6 w-full max-w-md">
      <div
          class="w-20 h-20 bg-primary-container/10 rounded-full flex items-center justify-center group-hover:scale-110 transition-transform">
                  <span class="material-symbols-outlined text-primary text-4xl"
                        data-icon="cloud_upload">cloud_upload</span>
      </div>
      <div class="space-y-2">
        <h4 class="text-xl font-bold text-on-surface font-headline">Drag &amp; Drop clinical media</h4>
        <p class="text-on-surface-variant text-sm">Support for DICOM, JPEG, and PNG files. Max 25MB per
          file.</p>
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
</template>

<style scoped>

</style>