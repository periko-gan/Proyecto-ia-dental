import { GRAPHQL_ENDPOINT } from '@/config/graphql'
import { getAccessToken } from './authService'

// Ejecuta una operación GraphQL con trazas de red y validación de errores.
export async function postGraphQL(query, variables = {}) {
  const headers = {
    'Content-Type': 'application/json',
  }

  // Incluir el token de autorización si está disponible
  const token = getAccessToken()
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  // Normaliza la query para trazas en consola.
  const operationPreview = String(query).trim()



  // Medir latencia total de la petición.
  const startTime = performance.now()

  const response = await fetch(GRAPHQL_ENDPOINT, {
    method: 'POST',
    headers,
    body: JSON.stringify({ query, variables }),
  })

  const endTime = performance.now()
  const duration = (endTime - startTime).toFixed(2)



  // Parseo JSON con control de errores para respuestas inválidas.
  let payload
  try {
    payload = await response.json()

  } catch (error) {
    console.error('❌ Error parseando JSON:', error)
    throw new Error('No se pudo leer la respuesta del servidor.')
  }

  // Errores HTTP fuera de rango 2xx.
  if (!response.ok) {
    const firstError = payload?.errors?.[0]?.message
    console.error(
      `
❌ ERROR HTTP
├─ Status: ${response.status}
├─ Error: ${firstError || 'Fallo la peticion GraphQL.'}
└─ Payload:`,

      payload,
    )
    throw new Error(firstError || 'Fallo la peticion GraphQL.')
  }

  // Errores GraphQL reportados en el payload.
  if (payload?.errors?.length) {
    console.error(
      `
❌ ERROR GraphQL
├─ Cantidad de errores: ${payload.errors.length}
└─ Errores:`,

      payload.errors,
    )
    throw new Error(payload.errors[0].message || 'Error GraphQL no especificado.')
  }



  return payload.data
}
