<script setup>
import { useUploadImagesQueue } from '@/composables/useUploadImagesQueue'

const {
  isDragging,
  fileInputRef,
  droppedFiles,
  validationErrors,
  queueReadyForGraphQL,
  isSendingQueue,
  preparedGraphQLSummary,
  sendResults,
  sendSummaryMessage,
  sendErrorMessage,
  totalFiles,
  totalSizeBytes,
  openFilePicker,
  onDragEnter,
  onDragOver,
  onDragLeave,
  onFileChange,
  onDrop,
  removeDroppedFile,
  prepareGraphQLPayload,
  sendQueuedFiles,
  formatFileSize,

  // Almacenamiento local
  storedImages,
  totalStoredImages,
  totalStoredSizeBytes,
  downloadStoredImage,
  deleteStoredImage,
  clearAllStoredImages,
  exportImageAsJSON,
} = useUploadImagesQueue()


async function handleSendFiles() {
  await sendQueuedFiles()
}

function handleDownload(image) {
  downloadStoredImage(image)
}

async function handleDelete(imageId) {
  if (confirm('¿Eliminar esta imagen del almacenamiento local?')) {
    await deleteStoredImage(imageId)
  }
}

async function handleClearAll() {
  if (confirm('¿Eliminar TODAS las imágenes almacenadas?')) {
    await clearAllStoredImages()
  }
}

function handleExportJSON(image) {
  exportImageAsJSON(image)
}
</script>

<template>
  <div class="space-y-6">
    <!-- Sección de Almacenamiento Local -->
    <div v-if="totalStoredImages > 0" class="rounded-xl border border-info/30 bg-info/5 p-6 space-y-4">
      <div class="flex items-center justify-between">
        <div>
          <p class="text-sm font-semibold uppercase tracking-wide text-info">📁 Almacenamiento Local</p>
          <p class="text-xs text-on-surface-variant mt-1">{{ totalStoredImages }} imagen(es) · {{ formatFileSize(totalStoredSizeBytes) }}</p>
        </div>
        <button
            class="btn btn-error btn-xs"
            type="button"
            @click="handleClearAll"
        >
          Limpiar Todo
        </button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
        <div
            v-for="image in storedImages"
            :key="image.id"
            class="rounded-lg border border-base-300 bg-base-100 p-3 flex items-center gap-3 hover:shadow-md transition-shadow"
        >
          <!-- Thumbnail -->
          <div class="w-16 h-16 shrink-0 rounded bg-gray-100 overflow-hidden flex items-center justify-center">
            <img
                :src="'data:' + image.mimeType + ';base64,' + image.base64"
                :alt="image.fileName"
                class="w-full h-full object-cover"
            />
          </div>

          <!-- Info -->
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium text-on-surface truncate">{{ image.fileName }}</p>
            <p class="text-xs text-on-surface-variant">{{ formatFileSize(image.fileSize) }}</p>
            <p class="text-xs text-on-surface-variant/70">{{ new Date(image.createdAt).toLocaleDateString() }}</p>
          </div>

          <!-- Acciones -->
          <div class="flex gap-1 shrink-0">
            <button
                class="btn btn-ghost btn-xs btn-circle"
                title="Descargar"
                @click="handleDownload(image)"
            >
              <span class="material-symbols-outlined text-base">download</span>
            </button>
            <button
                class="btn btn-ghost btn-xs btn-circle"
                title="Exportar JSON"
                @click="handleExportJSON(image)"
            >
              <span class="material-symbols-outlined text-base">description</span>
            </button>
            <button
                class="btn btn-ghost btn-xs btn-circle text-error"
                title="Eliminar"
                @click="handleDelete(image.id)"
            >
              <span class="material-symbols-outlined text-base">delete</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Upload Prompt & Queue -->
    <div
        class="border-2 border-dashed border-outline-variant bg-surface-container-low rounded-xl p-8 flex flex-col items-center justify-center transition-all hover:bg-surface-container-lowest hover:border-primary min-h-87.5"
        :class="{ 'border-primary bg-surface-container-lowest': isDragging }"
        @dragenter.prevent="onDragEnter"
        @dragover.prevent="onDragOver"
        @dragleave.prevent="onDragLeave"
        @drop.prevent="onDrop"
    >
      <!-- Upload Prompt -->
      <form class="flex flex-col items-center text-center space-y-6 w-full max-w-md">
      <!--      <div-->
      <!--          class="w-20 h-20 bg-primary-container/10 rounded-full flex items-center justify-center group-hover:scale-110 transition-transform">-->
      <!--                  <span class="material-symbols-outlined text-primary text-4xl"-->
      <!--                        data-icon="cloud_upload">cloud_upload</span>-->
      <!--      </div>-->
      <div class="space-y-2">
        <h4 class="text-xl font-bold text-on-surface font-headline">Arrastra y suelta la imagen</h4>
        <p class="text-on-surface-variant text-sm">Compatible con archivos JPG, JPEG y PNG.</p>
<!--        <p-->
<!--            class="text-sm font-semibold text-primary cursor-pointer select-none hover:underline"-->
<!--            role="button"-->
<!--            tabindex="0"-->
<!--            @click="openFilePicker"-->
<!--            @keydown.enter.prevent="openFilePicker"-->
<!--            @keydown.space.prevent="openFilePicker"-->
<!--        >-->
<!--          Haz clic aquí para examinar archivos-->
<!--        </p>-->
      </div>
      <!-- DaisyUI File Input -->
      <div class="form-control w-full hidden">
        <input
            ref="fileInputRef"
            class="hidden"
            type="file"
            accept="image/jpg,image/jpeg,image/png,.dcm,.dicom"
            multiple
            @change="onFileChange"
        />
      </div>

      <div v-if="validationErrors.length" class="alert alert-error w-full text-left py-2">
        <ul class="text-xs space-y-1">
          <li v-for="errorMessage in validationErrors" :key="errorMessage">{{ errorMessage }}</li>
        </ul>
      </div>

      <div v-if="droppedFiles.length" class="w-full text-center space-y-4">
        <div class="flex flex-col gap-2 rounded-xl border border-base-200 bg-base-100 p-4 text-left md:flex-row md:items-center md:justify-between">
          <div>
            <p class="text-xs font-semibold uppercase tracking-wide text-on-surface-variant">Archivos añadidos</p>
            <p class="text-sm text-on-surface-variant">{{ totalFiles }} archivo(s) · {{ formatFileSize(totalSizeBytes) }} en cola</p>
          </div>
          <div class="flex flex-wrap gap-2">
<!--            <button class="btn btn-ghost btn-xs" type="button" @click="clearAllFiles">Vaciar</button>-->
            <button
                class="btn btn-primary btn-xs"
                type="button"
                :disabled="isSendingQueue || !droppedFiles.length"
                @click="handleSendFiles"
            >
              {{ isSendingQueue ? 'Enviando...' : 'Enviar archivos' }}
            </button>
            <button
                class="btn btn-error btn-xs"
                type="button"
                v-if="droppedFiles.length"
                @click="removeDroppedFile(0)"
            >
              Eliminar
            </button>

          </div>
        </div>
        <p class="text-xs text-on-surface-variant">Las imágenes seleccionadas quedan aquí en memoria hasta que se preparen o se envíen por GraphQL.</p>

        <div v-if="queueReadyForGraphQL" class="rounded-xl border border-secondary/30 bg-secondary/5 p-4 text-left space-y-3">
          <div class="flex items-center justify-between gap-2">
            <p class="text-xs font-semibold uppercase tracking-wide text-secondary">Listo para GraphQL</p>
            <span class="badge badge-secondary badge-outline">Preparado</span>
          </div>
          <p class="text-xs text-on-surface-variant">Se generó la estructura temporal que luego se enviará al backend mediante la mutación GraphQL.</p>
          <ul class="space-y-1 text-xs text-on-surface-variant">
            <li v-for="item in preparedGraphQLSummary" :key="`${item.fileName}-${item.mimeType}`">
              {{ item.fileName }} · {{ item.mimeType }} · {{ formatFileSize(item.sizeBytes) }}
            </li>
          </ul>
        </div>

        <div v-if="sendSummaryMessage || sendErrorMessage || sendResults.length" class="rounded-xl border border-base-200 bg-base-100 p-4 text-left space-y-3">
          <p class="text-xs font-semibold uppercase tracking-wide text-on-surface-variant">Resultado del envío</p>
          <p v-if="sendSummaryMessage" class="text-sm text-success">{{ sendSummaryMessage }}</p>
          <p v-if="sendErrorMessage" class="text-sm text-error">{{ sendErrorMessage }}</p>
          <ul v-if="sendResults.length" class="space-y-1 text-xs text-on-surface-variant">
            <li v-for="result in sendResults" :key="`${result.fileName}-${result.analysisId || 'pending'}`">
              {{ result.fileName }} · {{ result.success ? 'OK' : 'Error' }}
              <span v-if="result.message">· {{ result.message }}</span>
            </li>
          </ul>
        </div>
      </div>

      <button class="btn btn-primary btn-wide font-bold gap-2" type="button" @click="openFilePicker">
        <span class="material-symbols-outlined" data-icon="upload_file">upload_file</span>
        Examinar archivo
      </button>
    </form>
    </div>
  </div>
</template>

<style scoped>

</style>
