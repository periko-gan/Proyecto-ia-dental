# 🧪 Guía de Prueba Rápida - Sistema de Login

## ⚡ Prueba Rápida (5 minutos)

### Paso 1: Verificar que el backend está corriendo
```bash
# En otra terminal
cd backend
python main.py
# Debe mostrar: Uvicorn running on http://127.0.0.1:8000
```

### Paso 2: Iniciar el frontend
```bash
# En otra terminal  
cd frontend
npm run dev
# Acceder a http://localhost:5173
```

### Paso 3: Prueba de Login

#### Opción A: Con usuario ya registrado
```
1. Acceder a http://localhost:5173/login
2. Introducir email: pepe@pepon.com
3. Introducir contraseña: 12345678
4. Clickear "Iniciar sesión"
5. ✅ Debe redirigir a /dashboard
```

#### Opción B: Registrarse primero (si no existe)
```
1. Acceder a http://localhost:5173/register
2. Completar formulario con email y contraseña
3. Clickear "Registrarse"
4. ✅ Debe redirigir a /dashboard
5. Abrir /login en otra pestaña
6. Introducir mismas credenciales
7. ✅ Debe redirigir a /dashboard
```

---

## 🔍 Verificaciones en DevTools (F12)

### ✅ Verificación 1: SessionStorage
```javascript
// En DevTools → Console
console.table(Object.entries(sessionStorage).map(([k,v]) => ({key: k, value: v})))
```

**Debe mostrar 5 filas:**
```
┌─────────────┬──────────────────────────────────────────┐
│ (index)     │ key        value                          │
├─────────────┼──────────────────────────────────────────┤
│ 0           │ accessToken eyJhbGciOiJIUzI1NiIsInR5... │
│ 1           │ userId     f7a0e2b5-b422-456f-95f7-... │
│ 2           │ email      pepe@pepon.com                 │
│ 3           │ isActive   true                           │
│ 4           │ role       USER                           │
└─────────────┴──────────────────────────────────────────┘
```

### ✅ Verificación 2: Token en Headers
```
1. DevTools → Network
2. Hacer una petición GraphQL (ej: refrescar página en dashboard)
3. Clickear en la petición
4. Ir a Headers
5. Buscar "Authorization"
6. Debe mostrar: Bearer eyJhbGciOiJIUzI1NiIsInR5...
```

### ✅ Verificación 3: Protección de Rutas
```javascript
// En console, ejecutar:
sessionStorage.clear()

// Luego acceder a http://localhost:5173/dashboard
// ✅ Debe redirigir automáticamente a http://localhost:5173/login
```

### ✅ Verificación 4: Redirección de Autenticados
```javascript
// En console, simular sesión:
sessionStorage.setItem('accessToken', 'test')

// Luego acceder a http://localhost:5173/login
// ✅ Debe redirigir automáticamente a http://localhost:5173/dashboard
```

---

## 📡 Prueba en GraphQL Playground

### Acceder al Playground
- URL: `http://localhost:8000/graphql`

### Test 1: Login
```graphql
mutation {
  loginUser(email: "pepe@pepon.com", password: "12345678") {
    accessToken
    user {
      userId
      email
      isActive
      role
    }
  }
}
```

**Respuesta esperada:**
```json
{
  "data": {
    "loginUser": {
      "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "user": {
        "userId": "f7a0e2b5-b422-456f-95f7-23aa6c45c075",
        "email": "pepe@pepon.com",
        "isActive": true,
        "role": "USER"
      }
    }
  }
}
```

### Test 2: Credenciales Inválidas
```graphql
mutation {
  loginUser(email: "pepe@pepon.com", password: "contraseñaInvalida") {
    accessToken
    user {
      userId
      email
      isActive
      role
    }
  }
}
```

**Respuesta esperada:**
```json
{
  "errors": [
    {
      "message": "Invalid credentials"
    }
  ]
}
```

---

## 🎯 Flujo Completo de Prueba

### Escenario 1: Nuevo Usuario
```
1. ✅ Abrir http://localhost:5173/register
2. ✅ Llenar formulario con nuevo email
3. ✅ Clickear Registrarse → Redirige a /dashboard
4. ✅ Verificar sessionStorage tiene los 5 campos
5. ✅ Abrir DevTools → Network
6. ✅ Refrescar página (F5)
7. ✅ Verificar que las peticiones tienen "Authorization: Bearer..."
8. ✅ Clickear logout (si existe el botón)
9. ✅ Verificar sessionStorage está vacío
10. ✅ Intentar acceder a /dashboard → Redirige a /login
```

### Escenario 2: Usuario Existente
```
1. ✅ Abrir http://localhost:5173/login
2. ✅ Introducir email y contraseña de usuario existente
3. ✅ Clickear Iniciar sesión → Redirige a /dashboard
4. ✅ Verificar mismos 5 campos en sessionStorage
5. ✅ Mismo flujo que después del paso 4 del Escenario 1
```

### Escenario 3: Protección de Rutas
```
1. ✅ sessionStorage.clear() en console
2. ✅ Acceder a http://localhost:5173/dashboard
3. ✅ Debe redirigir a http://localhost:5173/login
4. ✅ Acceder a http://localhost:5173/analyze
5. ✅ Debe redirigir a http://localhost:5173/login
6. ✅ Hacer login
7. ✅ Intentar acceder a http://localhost:5173/login
8. ✅ Debe redirigir a http://localhost:5173/dashboard
```

---

## 🐛 Solución Rápida de Problemas

### Problema: "Error: No se pudo conectar al servidor"
```
✗ Solución:
1. Verificar que backend está corriendo: http://localhost:8000
2. Verificar que GRAPHQL_ENDPOINT en frontend apunta a http://localhost:8000/graphql
3. Reiniciar ambos servidores
```

### Problema: "Credenciales invalidas"
```
✗ Solución:
1. Verificar que el email existe en la base de datos
2. Verificar que la contraseña es correcta
3. Crear un nuevo usuario si no existe
```

### Problema: "No se redirige a /dashboard"
```
✗ Solución:
1. Abrir DevTools Console
2. Ver si hay errores de JavaScript
3. Verificar que sessionStorage se está guardando
4. Verificar que el router está correctamente importado
```

### Problema: "SessionStorage está vacío después de login"
```
✗ Solución:
1. Verificar que persistSession() se está llamando
2. Revisar respuesta de GraphQL en Network tab
3. Verificar que getAccessToken() no retorna null
```

### Problema: "No se incluye el token en peticiones"
```
✗ Solución:
1. Verificar que getAccessToken() está implementado
2. Verificar que graphqlClient.js importa getAccessToken
3. En DevTools Network → Headers → buscar "Authorization"
4. Si está vacío, revisar la consola para errores
```

---

## 📝 Comandos Útiles para Debug

```javascript
// Ver toda la sesión
console.log(sessionStorage)

// Ver un campo específico
console.log(sessionStorage.getItem('email'))

// Limpar sesión
sessionStorage.clear()

// Simular sesión (para pruebas)
sessionStorage.setItem('accessToken', 'test-token')
sessionStorage.setItem('userId', 'test-user-id')

// Ver rutas actuales
console.log(router.getRoutes())

// Ver ruta actual
console.log(router.currentRoute.value)

// Ir a una ruta
router.push('/login')
```

---

## ✅ Checklist Final

Después de completar todas las pruebas:

- [ ] Login redirige a /dashboard
- [ ] SessionStorage contiene 5 campos
- [ ] Token está en los headers de peticiones
- [ ] Logout limpia sessionStorage
- [ ] Rutas protegidas redirigen a /login sin sesión
- [ ] /login y /register redirigen a /dashboard con sesión
- [ ] Los datos del usuario se muestran correctamente
- [ ] Mensaje de error aparece con credenciales inválidas
- [ ] Al refrescar página se mantiene la sesión
- [ ] Documentación README fue actualizada

---

## 🎓 Ambiente de Prueba Recomendado

```bash
# Terminal 1: Backend
cd backend
python -m venv 3.12  # Si no existe
source 3.12/Scripts/activate  # Windows: 3.12\Scripts\activate
pip install -r requirements.txt
python main.py

# Terminal 2: Frontend
cd frontend
npm install  # Si es primera vez
npm run dev

# Terminal 3: DevTools
- Abrir navegador: http://localhost:5173
- Presionar F12 para DevTools
- Ir a Application → Local Storage / Session Storage
```

---

## 🚀 Siguientes Pasos

Una vez que el login funciona correctamente:

1. **Implementar Logout** en componentes
2. **Crear perfil de usuario** en `/dashboard/profile`
3. **Mostrar información del usuario** en la barra de navegación
4. **Implementar refresh token** para sesiones más largas
5. **Agregar roles y permisos** basados en `role` del usuario
6. **Integrar con Kafka** para eventos de login/logout

---

**¡Listo! La implementación del login está completa y lista para usar. 🎉**

