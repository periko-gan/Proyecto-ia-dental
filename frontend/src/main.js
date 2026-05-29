import {createApp} from 'vue'

// Punto de entrada: crea la app, registra el router y monta en #app.
import App from './App.vue'
import router from './router'
import './style.css'

// Refuerzo: fija el tema claro antes de montar la aplicación.
document.documentElement.classList.remove('dark')
document.documentElement.setAttribute('data-theme', 'light')

const app = createApp(App)

app.use(router)

app.mount('#app')
