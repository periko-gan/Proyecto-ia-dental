# Configuración de Vite optimizada para Vercel
import {fileURLToPath, URL} from 'node:url'
import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
    plugins: [
        vue(),
        vueDevTools(),
        tailwindcss(),
    ],
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url))
        },
    },
    build: {
        // Optimizaciones para Vercel
        outDir: 'dist',
        assetsDir: '_assets',
        rollupOptions: {
            output: {
                manualChunks: {
                    'vue': ['vue', 'vue-router'],
                    'apollo': ['@apollo/client', '@vue/apollo-composable', 'graphql'],
                }
            }
        }
    },
    server: {
        proxy: {
            '/api': {
                target: process.env.VITE_GRAPHQL_ENDPOINT || 'http://localhost:8000',
                changeOrigin: true,
            }
        }
    }
})

