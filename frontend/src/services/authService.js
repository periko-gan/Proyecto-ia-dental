import { postGraphQL } from '@/services/graphqlClient';

const REGISTER_AND_LOGIN_MUTATION = `
mutation RegisterAndLogin($email: String!, $password: String!) {
  registerUser(email: $email, password: $password) {
    userId
    email
    isActive
    createdAt
    role
  }
  loginUser(email: $email, password: $password) {
    accessToken
    user {
      createdAt
      email
      isActive
      role
      userId
    }
  }
}
`;

const LOGIN_MUTATION = `
mutation LoginUser($email: String!, $password: String!) {
  loginUser(email: $email, password: $password) {
    accessToken
    user {
      createdAt
      email
      isActive
      role
      userId
    }
  }
}
`;

function persistSession(accessToken, user) {
  // Guardar datos de forma individual en sessionStorage para mejor acceso
  sessionStorage.setItem('accessToken', accessToken);
  sessionStorage.setItem('userId', user.userId);
  sessionStorage.setItem('email', user.email);
  sessionStorage.setItem('isActive', user.isActive ? 'true' : 'false');
  sessionStorage.setItem('role', user.role);
}

/**
 * Obtiene los datos de sesión del usuario
 * @returns {Object|null} Datos de sesión o null si no hay sesión
 */
export function getSession() {
  const accessToken = sessionStorage.getItem('accessToken');

  if (!accessToken) {
    return null;
  }

  return {
    accessToken,
    userId: sessionStorage.getItem('userId'),
    email: sessionStorage.getItem('email'),
    isActive: sessionStorage.getItem('isActive') === 'true',
    role: sessionStorage.getItem('role'),
  };
}

/**
 * Verifica si hay una sesión activa
 * @returns {boolean}
 */
export function isAuthenticated() {
  return !!sessionStorage.getItem('accessToken');
}

/**
 * Obtiene el token de acceso desde sessionStorage
 * @returns {string|null}
 */
export function getAccessToken() {
  return sessionStorage.getItem('accessToken');
}

/**
 * Cierra la sesión del usuario
 */
export function logout() {
  sessionStorage.removeItem('accessToken');
  sessionStorage.removeItem('userId');
  sessionStorage.removeItem('email');
  sessionStorage.removeItem('isActive');
  sessionStorage.removeItem('role');
}

export async function registerAndLogin(email, password) {
  const data = await postGraphQL(REGISTER_AND_LOGIN_MUTATION, { email, password });
  const loginPayload = data?.loginUser;

  if (!loginPayload?.accessToken || !loginPayload?.user) {
    throw new Error('No se pudo completar el login después del registro.');
  }

  persistSession(loginPayload.accessToken, loginPayload.user);
  return data;
}

export async function loginAndPersist(email, password) {
  const data = await postGraphQL(LOGIN_MUTATION, { email, password });
  const loginPayload = data?.loginUser;

  if (!loginPayload?.accessToken || !loginPayload?.user) {
    throw new Error('Credenciales invalidas o respuesta incompleta.');
  }

  persistSession(loginPayload.accessToken, loginPayload.user);
  return loginPayload;
}

