import {postGraphQL} from '@/services/graphqlClient'

// Mutación de carga de radiografía con retorno del análisis asociado.
const UPLOAD_RADIOGRAPHY_MUTATION = `
mutation UploadRadiography($fileBase64: String!, $fileName: String!, $mimeType: String!) {
  uploadRadiography(fileBase64: $fileBase64, fileName: $fileName, mimeType: $mimeType) {
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

// Escapa caracteres conflictivos para mostrar la mutación en logs.
function escapeGraphQLString(value) {
    return String(value)
        .replaceAll('\\', '\\\\')
        .replaceAll('"', '\\"')
        .replaceAll('\n', '\\n')
        .replaceAll('\r', '\\r')
}

// Genera una vista previa acotada de la mutación para depuración.
function buildMutationPreview({fileBase64, fileName, mimeType}) {
    const previewBase64 = fileBase64.length > 120 ? `${fileBase64.slice(0, 120)}…` : fileBase64

    return `mutation UploadRadiography {
  uploadRadiography(
    fileBase64: "${escapeGraphQLString(previewBase64)}",
    fileName: "${escapeGraphQLString(fileName)}",
    mimeType: "${escapeGraphQLString(mimeType)}"
  ) {
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
}`
}

export async function uploadRadiography({fileBase64, fileName, mimeType}) {
    // Logs de diagnóstico para validar el payload enviado.


    try {

        const data = await postGraphQL(UPLOAD_RADIOGRAPHY_MUTATION, {
            fileBase64,
            fileName,
            mimeType,
        })


        if (data.uploadRadiography?.success) {

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
            fullError: error,
        })
        throw error
    }
}
