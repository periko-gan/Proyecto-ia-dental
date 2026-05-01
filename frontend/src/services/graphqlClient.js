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

  const response = await fetch(GRAPHQL_ENDPOINT, {
    method: 'POST',
    headers,
    body: JSON.stringify({ query, variables }),
  });

  let payload;
  try {
    payload = await response.json();
  } catch {
    throw new Error('No se pudo leer la respuesta del servidor.');
  }

  if (!response.ok) {
    const firstError = payload?.errors?.[0]?.message;
    throw new Error(firstError || 'Fallo la peticion GraphQL.');
  }

  if (payload?.errors?.length) {
    throw new Error(payload.errors[0].message || 'Error GraphQL no especificado.');
  }

  return payload.data;
}

