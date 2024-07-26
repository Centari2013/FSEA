import { defineConfig } from 'vite';
import { injectEmployeeIdMiddleware } from './middleware/injectEmployeeIdMiddleware';

export default defineConfig({
  server: {
    port: 5173,
    host: true, // This allows access from external IPs, useful for Docker
  
    setupMiddlewares: (middlewares, { app }) => {
      app.use(injectEmployeeIdMiddleware);
      return middlewares;
    },
  },
});
