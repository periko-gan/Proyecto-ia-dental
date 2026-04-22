import {createRouter, createWebHistory} from 'vue-router'

import AnalyzeView from '@/components/AnalyzeView.vue'
import DashboardView from '@/components/DashboardView.vue'
import DiagnosticView from "@/components/DiagnosticView.vue";
import EvolutionView from "@/components/EvolutionView.vue";
import LandingView from "@/components/LandingView.vue";
import FormularioView from "@/components/FormularioView.vue";

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
        path: '/formulario',
        name: 'Formulario',
        component: FormularioView,
    },
    {
        path: '/:pathMatch(.*)*',
        redirect: '/',
    },
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
})

export default router
