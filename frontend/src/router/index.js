import {createRouter, createWebHistory} from 'vue-router'

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
    },
    {
        path: '/analyze',
        name: 'Analyze',
        component: AnalyzeView,
    },
    {
        path: '/diagnostic',
        name: 'Diagnostic',
        component: DiagnosticView,
    },
    {
        path: '/evolution',
        name: 'Evolution',
        component: EvolutionView,
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

export default router
