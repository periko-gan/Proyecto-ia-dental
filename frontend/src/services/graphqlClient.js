import { GRAPHQL_ENDPOINT } from '@/config/graphql';
import { getAccessToken } from './authService';

export async function postGraphQL(query, variables = {}) {
  const headers = {
    'Content-Type': 'application/json',
  };

  // Incluir el token de autorización si está disponible
  const token = getAccessToken();
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const operationPreview = String(query).trim();

  console.log(`
🌐 SOLICITUD GraphQL
├─ Endpoint: ${GRAPHQL_ENDPOINT}
├─ Método: POST
├─ Headers:`, headers)
  console.log('├─ Operación GraphQL completa:\n' + operationPreview)
  console.log('└─ Variables:', variables)

  const startTime = performance.now();

  const response = await fetch(GRAPHQL_ENDPOINT, {
    method: 'POST',
    headers,
    body: JSON.stringify({ query, variables }),
  });

  const endTime = performance.now();
  const duration = (endTime - startTime).toFixed(2);

  console.log(`
📥 RESPUESTA HTTP
├─ Status Code: ${response.status}
├─ Status Text: ${response.statusText}
├─ Tiempo respuesta: ${duration}ms
└─ Content-Type: ${response.headers.get('content-type')}
  `)

  let payload;
  try {
    payload = await response.json();
    console.log('✅ Payload JSON parseado:')
    console.log(JSON.stringify(payload, null, 2))
  } catch (error) {
    console.error('❌ Error parseando JSON:', error);
    throw new Error('No se pudo leer la respuesta del servidor.');
  }

  if (!response.ok) {
    const firstError = payload?.errors?.[0]?.message;
    console.error(`
❌ ERROR HTTP
├─ Status: ${response.status}
├─ Error: ${firstError || 'Fallo la peticion GraphQL.'}
└─ Payload:`, payload)
    throw new Error(firstError || 'Fallo la peticion GraphQL.');
  }

  if (payload?.errors?.length) {
    console.error(`
❌ ERROR GraphQL
├─ Cantidad de errores: ${payload.errors.length}
└─ Errores:`, payload.errors)
    throw new Error(payload.errors[0].message || 'Error GraphQL no especificado.');
  }

  console.log('✨ Respuesta completada exitosamente')

  return payload.data;
}

