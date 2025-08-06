import { defineConfig } from 'vite'

export default defineConfig({
  root: 'static',
  build: {
    outDir: '../dist',
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: 'static/index.html',
        analysis: 'static/analysis.html',
        success: 'static/success.html'
      }
    }
  },
  server: {
    port: 3000,
    proxy: {
      '/tts': 'http://localhost:8000',
      '/tts_stream': 'http://localhost:8000',
      '/voices': 'http://localhost:8000',
      '/chat': 'http://localhost:8000',
      '/chat_stream': 'http://localhost:8000',
      '/analyze_conversation': 'http://localhost:8000',
      '/test_analysis': 'http://localhost:8000',
      '/health': 'http://localhost:8000'
    }
  }
}) 