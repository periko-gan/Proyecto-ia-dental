import { createRouter, createWebHistory } from 'vue-router'

import AnalyzeView from '../components/AnalyzeView.vue'
import DashboardView from '../components/DashboardView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: DashboardView,
  },
  {
    path: '/analyze',
    name: 'Analyze',
    component: AnalyzeView,
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
