import {createApp} from 'vue'

// Punto de entrada: crea la app, registra el router y monta en #app.

import App from './App.vue'
import router from './router'
import './style.css'

const app = createApp(App)

app.use(router)

app.mount('#app')
