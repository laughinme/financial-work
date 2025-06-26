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
    allowedHosts: ["localhost", "612c-185-77-216-38.ngrok-free.app"],
  },
});
