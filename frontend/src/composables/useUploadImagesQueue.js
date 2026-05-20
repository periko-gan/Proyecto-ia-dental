import { computed, onBeforeUnmount, ref } from 'vue'
import { useRouter } from 'vue-router'
import { uploadRadiography } from '@/services/uploadRadiographyService'
import { useDiagnosticAnalysis } from './useDiagnosticAnalysis'

// Límite de peso y formatos permitidos para radiografías.
const MAX_FILE_SIZE_BYTES = 25 * 1024 * 1024
const allowedMimeTypes = new Set(['image/jpeg', 'image/png'])
const allowedExtensions = new Set(['dcm', 'dicom', 'jpg', 'jpeg', 'png'])

function getFileExtension(fileName) {
  const parts = fileName.split('.')
  return parts.length > 1 ? parts.pop().toLowerCase() : ''
}

function isAllowedType(file) {
  const extension = getFileExtension(file.name)
  return allowedMimeTypes.has(file.type) || allowedExtensions.has(extension)
}

// Genera un id estable para evitar duplicados en cola.
function getFileKey(file) {
  return `${file.name}-${file.size}-${file.lastModified}-${file.type}`
}

function createQueueEntry(file, createdAt = Date.now()) {
  return {
    id: getFileKey(file),
    file,
    createdAt,
    previewUrl: file.type.startsWith('image/') ? URL.createObjectURL(file) : '',
  }
}

function revokeQueueEntry(entry) {
  if (entry?.previewUrl) {
    URL.revokeObjectURL(entry.previewUrl)
  }
}

// Convierte un File a base64 para enviarlo por GraphQL.
function readFileAsBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => {
      const result = String(reader.result ?? '')
      resolve(result.includes(',') ? result.split(',').pop() : result)
    }
    reader.onerror = () => reject(reader.error ?? new Error('No se pudo leer el archivo.'))
    reader.readAsDataURL(file)
  })
}

export function useUploadImagesQueue() {
  const router = useRouter()
  const { setAnalysis } = useDiagnosticAnalysis()

  const isDragging = ref(false)
  const dragDepth = ref(0)
  const fileInputRef = ref(null)
  const droppedFiles = ref([])
  const validationErrors = ref([])
  const queueReadyForGraphQL = ref(false)
  const isPreparingGraphQL = ref(false)
  const isSendingQueue = ref(false)
  const preparedGraphQLPayload = ref([])
  const sendResults = ref([])
  const sendSummaryMessage = ref('')
  const sendErrorMessage = ref('')

  const preparedGraphQLSummary = computed(() =>
    preparedGraphQLPayload.value.map((item) => ({
      fileName: item.fileName,
      mimeType: item.mimeType,
      sizeBytes: item.sizeBytes,
    })),
  )

  const totalFiles = computed(() => droppedFiles.value.length)
  const totalSizeBytes = computed(() =>
    droppedFiles.value.reduce((sum, entry) => sum + entry.file.size, 0),
  )
  const hasFiles = computed(() => droppedFiles.value.length > 0)

  function openFilePicker() {
    if (hasFiles.value) return
    fileInputRef.value?.click()
  }

  function clearInputSelection() {
    if (fileInputRef.value) {
      fileInputRef.value.value = ''
    }
  }

  function onDragEnter() {
    if (hasFiles.value) return
    dragDepth.value += 1
    isDragging.value = true
  }

  function onDragOver() {
    if (hasFiles.value) return
    isDragging.value = true
  }

  function onDragLeave() {
    dragDepth.value = Math.max(0, dragDepth.value - 1)
    if (dragDepth.value === 0) {
      isDragging.value = false
    }
  }

  // Valida formato y tamaño de archivos entrantes.
  function validateFiles(files) {
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

    return { validFiles, errors }
  }

  // Une lista previa con nuevos archivos evitando duplicados.
  function mergeFiles(existingFiles, incomingFiles) {
    const seen = new Set(existingFiles.map((entry) => entry.id))
    const merged = [...existingFiles]

    for (const file of incomingFiles) {
      const entry = createQueueEntry(file)
      if (seen.has(entry.id)) {
        revokeQueueEntry(entry)
        continue
      }

      seen.add(entry.id)
      merged.push(entry)
    }

    return merged
  }

  function onFileChange(event) {
    return processIncomingFiles(event.target?.files)
  }

  function onDrop(event) {
    dragDepth.value = 0
    isDragging.value = false
    return processIncomingFiles(event.dataTransfer?.files)
  }

  async function removeDroppedFile(index) {
    const removedEntry = droppedFiles.value[index]
    revokeQueueEntry(removedEntry)
    droppedFiles.value = droppedFiles.value.filter((_, itemIndex) => itemIndex !== index)
    queueReadyForGraphQL.value = false
    preparedGraphQLPayload.value = []
    sendResults.value = []
    sendSummaryMessage.value = ''
    sendErrorMessage.value = ''
    clearInputSelection()
  }

  async function clearAllFiles(options = {}) {
    const { preserveSendState = false } = options

    for (const entry of droppedFiles.value) {
      revokeQueueEntry(entry)
    }
    droppedFiles.value = []
    validationErrors.value = []
    queueReadyForGraphQL.value = false
    preparedGraphQLPayload.value = []
    if (!preserveSendState) {
      sendResults.value = []
      sendSummaryMessage.value = ''
      sendErrorMessage.value = ''
    }
    clearInputSelection()
  }

  // No local storage: removed imageStorageService usage

  async function processIncomingFiles(rawFiles) {
    if (hasFiles.value) {
      clearInputSelection()
      return
    }

    const files = Array.from(rawFiles ?? []).slice(0, 1)
    const { validFiles, errors } = validateFiles(files)

    validationErrors.value = errors
    queueReadyForGraphQL.value = false
    preparedGraphQLPayload.value = []
    sendResults.value = []
    sendSummaryMessage.value = ''
    sendErrorMessage.value = ''

    for (const entry of droppedFiles.value) {
      revokeQueueEntry(entry)
    }
    droppedFiles.value = []

    if (validFiles.length > 0) {
      droppedFiles.value = mergeFiles([], validFiles)
    }

    clearInputSelection()
  }

  // Envia la cola actual (o la prepara si no está lista).
  async function sendQueuedFiles() {
    if (!droppedFiles.value.length) {
      sendErrorMessage.value = 'No hay archivos para enviar.'
      sendSummaryMessage.value = ''
      console.warn('⚠️ No hay archivos en la cola para enviar')
      return []
    }

    sendErrorMessage.value = ''
    sendSummaryMessage.value = ''

    const payload = preparedGraphQLPayload.value.length
      ? preparedGraphQLPayload.value
      : await prepareGraphQLPayload()

    if (!payload.length) {
      sendErrorMessage.value = 'No se pudo preparar la cola para enviar.'
      console.error('❌ La cola de GraphQL está vacía')
      return []
    }

    console.log(`
📦 INICIANDO ENVÍO DE COLA
├─ Total de archivos: ${payload.length}
├─ Archivos: ${payload.map((p) => p.fileName).join(', ')}
└─ Tamaño total: ${payload.reduce((sum, p) => sum + p.sizeBytes, 0)} bytes
    `)

    isSendingQueue.value = true
    const results = []

    try {
      for (let index = 0; index < payload.length; index++) {
        const item = payload[index]
        console.log(`
⏳ Enviando archivo ${index + 1}/${payload.length}...
├─ Nombre: ${item.fileName}
├─ Tipo: ${item.mimeType}
└─ Tamaño: ${item.sizeBytes} bytes
        `)

        const response = await uploadRadiography(item)

        results.push({
          fileName: item.fileName,
          success: Boolean(response?.success),
          message: response?.message ?? '',
          analysisId: response?.analysis?.analysisId ?? null,
          status: response?.analysis?.status ?? null,
          analysis: response?.analysis ?? null,
          file: item,
        })
      }

      sendResults.value = results

      const allSucceeded = results.length > 0 && results.every((item) => item.success)

      console.log(
        `
✅ RESUMEN DEL ENVÍO
├─ Total procesado: ${results.length}
├─ Exitosos: ${results.filter((r) => r.success).length}
├─ Fallidos: ${results.filter((r) => !r.success).length}
└─ Resultados:`,
        results,
      )

      if (allSucceeded) {
        sendSummaryMessage.value = `Se enviaron ${results.length} archivo(s) correctamente.`
        console.log(`🎉 ¡TODOS LOS ARCHIVOS SE ENVIARON EXITOSAMENTE!`)

        // Guardar el análisis del primer resultado exitoso
        const firstSuccessfulResult = results.find((r) => r.success)
        if (firstSuccessfulResult?.analysis) {
          const mimeType = firstSuccessfulResult.file?.mimeType || 'image/jpeg'
          const imageSrc = firstSuccessfulResult.file?.fileBase64
            ? `data:${mimeType};base64,${firstSuccessfulResult.file.fileBase64}`
            : ''

          const imageData = {
            fileName: firstSuccessfulResult.fileName,
            mimeType,
            imageSrc,
          }
          setAnalysis(firstSuccessfulResult.analysis, imageData)

          // Redirigir a diagnóstico
          console.log('🔄 Redirigiendo a /diagnostic...')
          await router.push('/diagnostic')
        }

        await clearAllFiles({ preserveSendState: true })
      } else {
        sendErrorMessage.value = 'Algunos archivos no pudieron enviarse. Revisa los resultados.'
        console.warn('⚠️ Algunos archivos fallaron en el envío')
      }

      return results
    } catch (error) {
      sendResults.value = results
      sendErrorMessage.value = error?.message || 'No se pudo enviar la cola de archivos.'
      console.error('❌ Error durante el envío de la cola:', error)
      return results
    } finally {
      isSendingQueue.value = false
      console.log('════════════════════════════════════════════════════════════')
    }
  }

  // Prepara la cola para enviar: base64 + metadatos mínimos.
  async function prepareGraphQLPayload() {
    if (!droppedFiles.value.length) {
      preparedGraphQLPayload.value = []
      queueReadyForGraphQL.value = false
      return []
    }

    isPreparingGraphQL.value = true
    try {
      const payload = await Promise.all(
        droppedFiles.value.map(async (entry) => ({
          fileBase64: await readFileAsBase64(entry.file),
          fileName: entry.file.name,
          mimeType: entry.file.type || 'image/jpeg',
          sizeBytes: entry.file.size,
        })),
      )

      preparedGraphQLPayload.value = payload
      queueReadyForGraphQL.value = true
      return payload
    } finally {
      isPreparingGraphQL.value = false
    }
  }

  // Formateo corto de tamaño de archivo.
  function formatFileSize(bytes) {
    if (!Number.isFinite(bytes)) return '0 B'
    if (bytes < 1024) return `${bytes} B`
    const kb = bytes / 1024
    if (kb < 1024) return `${kb.toFixed(1)} KB`
    return `${(kb / 1024).toFixed(1)} MB`
  }

  // no onMounted storage initialization required

  onBeforeUnmount(() => {
    for (const entry of droppedFiles.value) {
      revokeQueueEntry(entry)
    }
  })

  return {
    // Estado de la cola
    isDragging,
    dragDepth,
    fileInputRef,
    droppedFiles,
    validationErrors,
    queueReadyForGraphQL,
    isPreparingGraphQL,
    isSendingQueue,
    preparedGraphQLPayload,
    preparedGraphQLSummary,
    sendResults,
    sendSummaryMessage,
    sendErrorMessage,
    totalFiles,
    totalSizeBytes,
    hasFiles,

    // (sin almacenamiento local)

    // Funciones de la cola
    openFilePicker,
    onDragEnter,
    onDragOver,
    onDragLeave,
    onFileChange,
    onDrop,
    removeDroppedFile,
    sendQueuedFiles,
    formatFileSize,

    // (sin funciones de almacenamiento local)
  }
}
