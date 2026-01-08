import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    // This is the critical part that is missing or broken
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // Points to your Python backend
        changeOrigin: true,
        secure: false,
      }
    }
  }
})