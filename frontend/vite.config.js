import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // Proxy API calls during development so no CORS issues
      '/auth': 'http://localhost:5000',
      '/upload': 'http://localhost:5000',
      '/transactions': 'http://localhost:5000',
      '/health': 'http://localhost:5000',
    },
  },
});
