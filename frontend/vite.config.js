import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    port: 5173,
    host: true, // This allows access from external IPs, useful for Docker

  },
});
