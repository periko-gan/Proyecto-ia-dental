import {postGraphQL} from '@/services/graphqlClient'

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

export async function fetchMyAnalyses(limit = 20, offset = 0) {
    const data = await postGraphQL(MY_ANALYSES_QUERY, {limit, offset})
    return data.myAnalyses
}
