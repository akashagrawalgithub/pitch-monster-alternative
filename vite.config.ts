import { defineConfig } from 'vite'

export default defineConfig({
  root: 'static',
  build: {
    outDir: '../dist',
    emptyOutDir: true,
    target: 'es2020',
    cssCodeSplit: true,
    sourcemap: false,
    modulePreload: { polyfill: false },
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules')) {
            return 'vendor'
          }
        },
        chunkFileNames: 'assets/[name]-[hash].js',
        entryFileNames: 'assets/[name]-[hash].js',
        assetFileNames: 'assets/[name]-[hash][extname]'
      },
      input: {
        main: 'static/index.html',
        analysis: 'static/analysis.html',
        success: 'static/success.html',
        login: 'static/login.html',
        agents: 'static/index.html',
        'agent-info': 'static/agent-info.html',
        conversation: 'static/conversation.html',
        'past-conversations': 'static/past-conversations.html',
        users: 'static/users.html',
        marketing: 'static/marketing.html'
      }
    }
  },
  server: {
    port: 3000,
    proxy: {
      '/tts': 'http://localhost:8000',
      '/tts_stream': 'http://localhost:8000',
      '/chat': 'http://localhost:8000',
      '/chat_stream': 'http://localhost:8000',
      '/analyze_conversation': 'http://localhost:8000',
      '/best-pitch': 'http://localhost:8000',
      '/test-perfect-pitch': 'http://localhost:8000',
      '/login': 'http://localhost:8000',
      '/auth': 'http://localhost:8000',
      '/api/db': 'http://localhost:8000',
      '/api/get_agent_prompt': 'http://localhost:8000',
      '/api/openai-realtime-token': 'http://localhost:8000'
    }
  }
}) 