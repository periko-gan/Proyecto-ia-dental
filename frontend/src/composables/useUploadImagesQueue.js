import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { uploadRadiography } from '@/services/uploadRadiographyService'
import imageStorageService from '@/services/imageStorageService'
import { useDiagnosticAnalysis } from './useDiagnosticAnalysis'

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

  // Almacenamiento local
  const storedImages = ref([])
  const isLoadingStoredImages = ref(false)
  const storageInitError = ref(null)
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

  const totalStoredImages = computed(() => storedImages.value.length)
  const totalStoredSizeBytes = computed(() =>
    storedImages.value.reduce((sum, image) => sum + (image.fileSize || 0), 0),
  )

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

  // ========== Funciones de Almacenamiento Local ==========

  async function loadStoredImages() {
    isLoadingStoredImages.value = true
    try {
      await imageStorageService.init()
      const images = await imageStorageService.getAllImages()
      storedImages.value = images
      storageInitError.value = null
    } catch (error) {
      console.error('Error cargando imágenes almacenadas:', error)
      storageInitError.value = error?.message || 'Error cargando almacenamiento'
    } finally {
      isLoadingStoredImages.value = false
    }
  }

  async function saveImageToStorage(file, base64Content) {
    try {
      const savedImage = await imageStorageService.saveImage(file, base64Content)
      storedImages.value.unshift(savedImage)
      return savedImage
    } catch (error) {
      console.error('Error guardando imagen:', error)
      throw error
    }
  }

  async function deleteStoredImage(imageId) {
    try {
      await imageStorageService.deleteImage(imageId)
      storedImages.value = storedImages.value.filter((img) => img.id !== imageId)
    } catch (error) {
      console.error('Error eliminando imagen:', error)
      throw error
    }
  }

  async function clearAllStoredImages() {
    try {
      await imageStorageService.clearAll()
      storedImages.value = []
    } catch (error) {
      console.error('Error limpiando almacenamiento:', error)
      throw error
    }
  }

  function downloadStoredImage(image) {
    try {
      return imageStorageService.downloadImage(image)
    } catch (error) {
      console.error('Error descargando imagen:', error)
      return false
    }
  }

  function exportImageAsJSON(image) {
    try {
      imageStorageService.exportAsJSON(image)
    } catch (error) {
      console.error('Error exportando imagen:', error)
    }
  }

  async function processIncomingFiles(rawFiles) {
    const files = Array.from(rawFiles ?? [])
    const { validFiles, errors } = validateFiles(files)

    validationErrors.value = errors
    queueReadyForGraphQL.value = false
    preparedGraphQLPayload.value = []
    sendResults.value = []
    sendSummaryMessage.value = ''
    sendErrorMessage.value = ''

    // Guardar archivos en almacenamiento local mientras se añaden a la cola
    for (const file of validFiles) {
      try {
        const base64Content = await readFileAsBase64(file)
        await saveImageToStorage(file, base64Content)
      } catch (error) {
        console.warn(`Error guardando ${file.name} en almacenamiento local:`, error)
      }
    }

    const nextEntries = mergeFiles(droppedFiles.value, validFiles)

    for (const entry of droppedFiles.value) {
      if (!nextEntries.some((candidate) => candidate.id === entry.id)) {
        revokeQueueEntry(entry)
      }
    }

    droppedFiles.value = nextEntries
    clearInputSelection()
  }

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
├─ Archivos: ${payload.map(p => p.fileName).join(', ')}
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

      console.log(`
✅ RESUMEN DEL ENVÍO
├─ Total procesado: ${results.length}
├─ Exitosos: ${results.filter(r => r.success).length}
├─ Fallidos: ${results.filter(r => !r.success).length}
└─ Resultados:`, results)

      if (allSucceeded) {
        sendSummaryMessage.value = `Se enviaron ${results.length} archivo(s) correctamente.`
        console.log(`🎉 ¡TODOS LOS ARCHIVOS SE ENVIARON EXITOSAMENTE!`)

        // Guardar el análisis del primer resultado exitoso
        const firstSuccessfulResult = results.find(r => r.success)
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

   function formatFileSize(bytes) {
     if (!Number.isFinite(bytes)) return '0 B'
     if (bytes < 1024) return `${bytes} B`
     const kb = bytes / 1024
     if (kb < 1024) return `${kb.toFixed(1)} KB`
     return `${(kb / 1024).toFixed(1)} MB`
   }

   onMounted(() => {
     loadStoredImages()
   })

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

     // Estado del almacenamiento local
     storedImages,
     isLoadingStoredImages,
     storageInitError,
     totalStoredImages,
     totalStoredSizeBytes,

     // Funciones de la cola
     openFilePicker,
     onDragEnter,
     onDragOver,
     onDragLeave,
     onFileChange,
     onDrop,
     removeDroppedFile,
     clearAllFiles,
     prepareGraphQLPayload,
     sendQueuedFiles,
     formatFileSize,

     // Funciones del almacenamiento
     loadStoredImages,
     saveImageToStorage,
     deleteStoredImage,
     clearAllStoredImages,
     downloadStoredImage,
     exportImageAsJSON,
   }
 }

