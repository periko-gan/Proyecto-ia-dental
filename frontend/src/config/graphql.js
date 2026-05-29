// Endpoint GraphQL configurable por .env (Vite) con fallback local.
export const GRAPHQL_ENDPOINT =
    import.meta.env.VITE_GRAPHQL_ENDPOINT || 'http://localhost:8000/graphql'
