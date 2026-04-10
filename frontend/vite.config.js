import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/ask':      { target: 'http://localhost:8000', changeOrigin: true },
      '/answer':   { target: 'http://localhost:8000', changeOrigin: true },
      '/review':   { target: 'http://localhost:8000', changeOrigin: true },
      '/sessions': { target: 'http://localhost:8000', changeOrigin: true },
      '/session':  { target: 'http://localhost:8000', changeOrigin: true },
    }
  }
})
