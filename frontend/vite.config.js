import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import dotenv from 'dotenv';

dotenv.config();

const apiUrl = process.env.VITE_API_URL;

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
  ],
  define: {
    __API_URL__: JSON.stringify(apiUrl),
  },
  server: {
    port: 5173,
    host: true, // This allows access from external IPs, useful for Docker
  },
})
