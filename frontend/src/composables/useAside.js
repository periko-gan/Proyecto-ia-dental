import { computed, ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getSession } from '@/services/authService'
import { useDiagnosticAnalysis } from '@/composables/useDiagnosticAnalysis'

/**
 * Composable para encapsular la lógica del sidebar (Aside).
 */
export function useAside() {
  const route = useRoute()
  const router = useRouter()
  const { clearAnalysis } = useDiagnosticAnalysis()

  const loggedUserName = computed(() => getSession()?.name || 'Usuario sin sesión')

  function navLinkClass(routeName) {
    const baseClass = 'text-slate-500 hover:text-blue-700'
    const activeClass =
      'active bg-blue-50 text-blue-700 font-bold border-r-4 border-blue-700 rounded-noness'
    const inactiveClass = 'text-slate-500 border-transparent hover:text-blue-600'

    return `${baseClass} ${route.name === routeName ? activeClass : inactiveClass}`
  }

  async function handleLogout() {
    clearAnalysis()
    sessionStorage.clear()

    try {
      if (window.indexedDB) {
        window.indexedDB.deleteDatabase('DentalAI-Images')
        window.indexedDB.deleteDatabase('dental-ai-upload-queue')

        if (indexedDB.databases) {
          const dbs = await indexedDB.databases()
          dbs.forEach((db) => {
            if (db.name) {
              window.indexedDB.deleteDatabase(db.name)
            }
          })
        }
      }
    } catch (error) {
      console.warn('Error limpiando IndexedDB en logout:', error)
    }

    router.push('/')
  }

  // Mobile/hamburger drawer state & helpers
  const isOpen = ref(false)
  function openMenu() {
    isOpen.value = true
  }
  function closeMenu() {
    isOpen.value = false
  }

  function onKeydown(e) {
    if (e?.key === 'Escape') closeMenu()
  }
  onMounted(() => window.addEventListener('keydown', onKeydown))
  onUnmounted(() => window.removeEventListener('keydown', onKeydown))

  function logoutAndClose() {
    handleLogout()
    closeMenu()
  }

  return {
    loggedUserName,
    navLinkClass,
    handleLogout,
    isOpen,
    openMenu,
    closeMenu,
    logoutAndClose,
  }
}
