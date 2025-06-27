import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { resolve } from "path";

export default defineConfig({
  plugins: [react()],

  /* ─────────────── preload deps ─────────────── */
  optimizeDeps: {
    include: ["react-router-dom"],
  },

  /* ─────────────── two HTML entries ───────────── */
  build: {
    rollupOptions: {
      input: {
        index: resolve(__dirname, "index.html"),

        main: resolve(__dirname, "main.html"),
      },
    },
  },

  /* ─────────────── dev server ─────────────── */
  server: {
    allowedHosts: ["localhost", "76ca-79-127-249-67.ngrok-free.app"],
    // proxy: { "/api": "http://backend:8000/api" },
  },
});
