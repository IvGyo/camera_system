import path from "path"
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

export default defineConfig({
  base: "/YOUR_APP_SUBDIRECTORY/", // <-- ПРОМЕНЕТЕ ТОВА СПОРЕД НУЖДИТЕ
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
})
