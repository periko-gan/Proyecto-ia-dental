import { createRouter, createWebHistory } from 'vue-router'
import { isAuthenticated } from '@/services/authService'

import AnalyzeView from '@/components/AnalyzeView.vue'
import DashboardView from '@/components/DashboardView.vue'
import DiagnosticView from "@/components/DiagnosticView.vue";
import EvolutionView from "@/components/EvolutionView.vue";
import LandingView from "@/components/LandingView.vue";
import LoginView from "@/components/LoginView.vue";
import RegisterView from "@/components/RegisterView.vue";

// Mapa principal de navegación de la SPA.
const routes = [
    {
        path: '/',
        name: 'Landing',
        component: LandingView,
    },
    {
        path: '/dashboard',
        name: 'Dashboard',
        component: DashboardView,
        meta: { requiresAuth: true },
    },
    {
        path: '/analyze',
        name: 'Analyze',
        component: AnalyzeView,
        meta: { requiresAuth: true },
    },
    {
        path: '/diagnostic',
        name: 'Diagnostic',
        component: DiagnosticView,
        meta: { requiresAuth: true },
    },
    {
        path: '/evolution',
        name: 'Evolution',
        component: EvolutionView,
        meta: { requiresAuth: true },
    },
    {
        path: '/login',
        name: 'Login',
        component: LoginView,
    },
    {
        path: '/register',
        name: 'Register',
        component: RegisterView,
    },
    {
        path: '/:pathMatch(.*)*',
        redirect: '/',
    },
]

const router = createRouter({
    // Usa el BASE_URL de Vite para soportar despliegues en subrutas.
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
})

// Guard de navegación para proteger rutas que requieren autenticación
router.beforeEach((to, from, next) => {
    const hasAuth = isAuthenticated()
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth)

    // Si la ruta requiere autenticación y no hay sesión activa
    if (requiresAuth && !hasAuth) {
        // Redirigir a login
        next({ name: 'Login' })
    }
    // Si intenta acceder a login o registro estando autenticado
    else if ((to.name === 'Login' || to.name === 'Register') && hasAuth) {
        // Redirigir a dashboard
        next({ name: 'Dashboard' })
    }
    else {
        next()
    }
})

export default router
