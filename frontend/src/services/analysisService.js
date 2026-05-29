import {postGraphQL} from '@/services/graphqlClient'

// Consulta base para obtener el historial de análisis del usuario.
const MY_ANALYSES_QUERY = `
  query MyAnalyses($limit: Int, $offset: Int) {
    myAnalyses(limit: $limit, offset: $offset) {
      analysisId
      fileName
      filePath
      mimeType
      fileSizeBytes
      status
      createdAt
      detections {
        classId
        className
        confidence
        bboxXyxy
        label
      }
    }
  }
`

// Paginación simple con limit/offset para el historial.
export async function fetchMyAnalyses(limit = 20, offset = 0) {
    const data = await postGraphQL(MY_ANALYSES_QUERY, {limit, offset})
    return data.myAnalyses
}
