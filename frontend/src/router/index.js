import {createRouter, createWebHistory} from 'vue-router'

import AnalyzeView from '@/components/AnalyzeView.vue'
import DashboardView from '@/components/DashboardView.vue'
import DiagnosticView from "@/components/DiagnosticView.vue";
import EvolutionView from "@/components/EvolutionView.vue";

const routes = [
    {
        path: '/',
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
        path: '/:pathMatch(.*)*',
        redirect: '/',
    },
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
})

export default router
