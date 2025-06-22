import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig({
  plugins: [react()],

  /* ─────────────── preload deps ─────────────── */
  optimizeDeps: {
    include: ['react-router-dom'],
  },

  /* ─────────────── two HTML entries ───────────── */
  build: {
    rollupOptions: {
      input: {
  
        index: resolve(__dirname, 'index.html'),

  
        main: resolve(__dirname, 'main.html'),
      },
    },
  },

  /* ─────────────── dev server ─────────────── */
  server: {
    allowedHosts: [
      'localhost',
      '6e97-84-17-55-197.ngrok-free.app',
    ],
  },
});
