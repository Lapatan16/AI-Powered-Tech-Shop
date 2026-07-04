import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/static': {
        target: 'http://localhost:9061',
        changeOrigin: true,
        secure: false,
      }
    }
  }
})