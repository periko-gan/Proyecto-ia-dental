<script setup>
import {ref} from 'vue'

// Restricciones de carga permitidas por el flujo clínico.
const MAX_FILE_SIZE_BYTES = 25 * 1024 * 1024
const allowedMimeTypes = new Set(['image/jpeg', 'image/png'])
const allowedExtensions = new Set(['dcm', 'dicom', 'jpg', 'jpeg', 'png'])

const isDragging = ref(false)
const dragDepth = ref(0)
const fileInputRef = ref(null)
const droppedFiles = ref([])
const validationErrors = ref([])

function openFilePicker() {
  fileInputRef.value?.click()
}

function clearInputSelection() {
  if (fileInputRef.value) {
    fileInputRef.value.value = ''
  }
}

function onDragEnter() {
  dragDepth.value += 1
  isDragging.value = true
}

function onDragOver() {
  isDragging.value = true
}

function onDragLeave() {
  dragDepth.value = Math.max(0, dragDepth.value - 1)
  if (dragDepth.value === 0) {
    isDragging.value = false
  }
}

function getFileExtension(fileName) {
  const parts = fileName.split('.')
  return parts.length > 1 ? parts.pop().toLowerCase() : ''
}

function isAllowedType(file) {
  const extension = getFileExtension(file.name)
  return allowedMimeTypes.has(file.type) || allowedExtensions.has(extension)
}

function validateFiles(files) {
  // Filtra archivos no válidos y acumula mensajes para mostrarlos en UI.
  const validFiles = []
  const errors = []

  for (const file of files) {
    if (!isAllowedType(file)) {
      errors.push(`"${file.name}" no tiene un formato permitido.`)
      continue
    }

    if (file.size > MAX_FILE_SIZE_BYTES) {
      errors.push(`"${file.name}" supera el limite de 25MB.`)
      continue
    }

    validFiles.push(file)
  }

  return {validFiles, errors}
}

function setInputFiles(files) {
  if (!fileInputRef.value) {
    return
  }

  const transfer = new DataTransfer()
  for (const file of files) {
    transfer.items.add(file)
  }
  fileInputRef.value.files = transfer.files
}

function processIncomingFiles(rawFiles, options = {syncInput: true, source: 'input'}) {
  // Unifica el procesamiento para input manual y drag & drop.
  const files = Array.from(rawFiles ?? [])
  const {validFiles, errors} = validateFiles(files)

  validationErrors.value = errors

  if (options.syncInput) {
    setInputFiles(validFiles)
  } else {
    clearInputSelection()
  }

  if (options.source === 'drop') {
    droppedFiles.value = validFiles
  }
}

function onFileChange(event) {
  processIncomingFiles(event.target?.files, {syncInput: true, source: 'input'})
}

function onDrop(event) {
  dragDepth.value = 0
  isDragging.value = false
  processIncomingFiles(event.dataTransfer?.files, {syncInput: false, source: 'drop'})
}

function removeDroppedFile(index) {
  droppedFiles.value = droppedFiles.value.filter((_, itemIndex) => itemIndex !== index)
}

function formatFileSize(bytes) {
  if (!Number.isFinite(bytes)) return '0 B'
  if (bytes < 1024) return `${bytes} B`
  const kb = bytes / 1024
  if (kb < 1024) return `${kb.toFixed(1)} KB`
  return `${(kb / 1024).toFixed(1)} MB`
}
</script>

<template>
  <div
      class="border-2 border-dashed border-outline-variant bg-surface-container-low rounded-xl p-8 flex flex-col items-center justify-center transition-all hover:bg-surface-container-lowest hover:border-primary cursor-pointer min-h-[350px]"
      :class="{ 'border-primary bg-surface-container-lowest': isDragging }"
      @dragenter.prevent="onDragEnter"
      @dragover.prevent="onDragOver"
      @dragleave.prevent="onDragLeave"
      @drop.prevent="onDrop"
  >
    <!-- Upload Prompt -->
    <div class="flex flex-col items-center text-center space-y-6 w-full max-w-md">
      <!--      <div-->
      <!--          class="w-20 h-20 bg-primary-container/10 rounded-full flex items-center justify-center group-hover:scale-110 transition-transform">-->
      <!--                  <span class="material-symbols-outlined text-primary text-4xl"-->
      <!--                        data-icon="cloud_upload">cloud_upload</span>-->
      <!--      </div>-->
      <div class="space-y-2">
        <h4 class="text-xl font-bold text-on-surface font-headline">Arrastra y suelta material clínico</h4>
        <p class="text-on-surface-variant text-sm">Compatible con archivos JPG, JPEG y PNG. Maximo 25 MB por
          archivo.</p>
      </div>
      <!-- DaisyUI File Input -->
      <div class="form-control w-full">
        <input
            ref="fileInputRef"
            class="file-input file-input-bordered file-input-primary w-full shadow-sm"
            type="file"
            accept=".dcm,.dicom,image/jpeg,image/png"
            multiple
            @change="onFileChange"
        />
      </div>

      <div v-if="validationErrors.length" class="alert alert-error w-full text-left py-2">
        <ul class="text-xs space-y-1">
          <li v-for="errorMessage in validationErrors" :key="errorMessage">{{ errorMessage }}</li>
        </ul>
      </div>

      <div v-if="droppedFiles.length" class="w-full text-center space-y-2">
        <p class="text-xs font-semibold uppercase tracking-wide text-on-surface-variant">Archivos arrastrados</p>
        <ul class="space-y-2">
          <li
              v-for="(file, index) in droppedFiles"
              :key="`${file.name}-${file.lastModified}`"
              class="mx-auto w-full flex items-center justify-between gap-2 bg-base-100 border border-base-200 rounded-lg px-3 py-2"
          >
            <div class="min-w-0 text-left">
              <p class="truncate text-sm font-medium">{{ file.name }}</p>
              <p class="text-xs opacity-70">{{ formatFileSize(file.size) }}</p>
            </div>
            <button class="btn btn-ghost btn-xs" type="button" @click="removeDroppedFile(index)">Eliminar</button>
          </li>
        </ul>
      </div>

<!--      <button class="btn btn-primary btn-wide font-bold gap-2" type="button" @click="openFilePicker">-->
<!--        <span class="material-symbols-outlined" data-icon="upload_file">upload_file</span>-->
<!--        Seleccionar archivos-->
<!--      </button>-->
    </div>
  </div>
</template>

<style scoped>

</style>
