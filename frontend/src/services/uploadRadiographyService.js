import { postGraphQL } from '@/services/graphqlClient'

const UPLOAD_RADIOGRAPHY_MUTATION = `
mutation UploadRadiography($fileBase64: String!, $fileName: String!, $mimeType: String!) {
  uploadRadiography(fileBase64: $fileBase64 fileName: $fileName mimeType: $mimeType) {
    success
    message
    analysis {
      analysisId
      status
      fileName
      mimeType
      inferenceTimeMs
      modelVersion
      createdAt
      detections {
        bboxXyxy
        classId
        className
        confidence
        label
      }
      errorMessage
      filePath
      fileSizeBytes
      updatedAt
      userId
    }
  }
}
`

export async function uploadRadiography({ fileBase64, fileName, mimeType }) {
  console.log('📤 Iniciando envío de radiografía al backend...')
  console.log(`   📄 Archivo: ${fileName}`)
  console.log(`   🖼️  Tipo MIME: ${mimeType}`)
  console.log(`   📊 Tamaño base64: ${fileBase64.length} caracteres`)

  try {
    console.log('🔄 Enviando mutación GraphQL...')
    const data = await postGraphQL(UPLOAD_RADIOGRAPHY_MUTATION, {
      fileBase64,
      fileName,
      mimeType,
    })

    console.log('✅ Respuesta recibida del backend:')
    console.log('─'.repeat(60))
    console.log(JSON.stringify(data.uploadRadiography, null, 2))
    console.log('─'.repeat(60))

    if (data.uploadRadiography?.success) {
      console.log(`
✨ ¡ÉXITO! ✨
├─ Análisis ID: ${data.uploadRadiography.analysis?.analysisId}
├─ Estado: ${data.uploadRadiography.analysis?.status}
├─ Tiempo inferencia: ${data.uploadRadiography.analysis?.inferenceTimeMs}ms
├─ Versión modelo: ${data.uploadRadiography.analysis?.modelVersion}
└─ Mensaje: ${data.uploadRadiography.message}
      `)
    } else {
      console.warn(`
⚠️ ERROR en la respuesta:
├─ Success: ${data.uploadRadiography?.success}
└─ Mensaje: ${data.uploadRadiography?.message}
      `)
    }

    return data.uploadRadiography
  } catch (error) {
    console.error('❌ Error al enviar radiografía:')
    console.error({
      errorName: error.name,
      errorMessage: error.message,
      errorStack: error.stack,
      fullError: error
    })
    throw error
  }
}

