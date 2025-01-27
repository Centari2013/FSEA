import { defineConfig } from 'vite';
import { injectEmployeeIdMiddleware } from './middleware/injectEmployeeIdMiddleware';
import vue from '@vitejs/plugin-vue';


const apiKey = process.env.VITE_API_ENDPOINT;
export default defineConfig({
  plugins: [
    vue()
  ],
  define: {
    __API_KEY__: JSON.stringify(apiKey),
  },
  server: {
    setupMiddlewares: (middlewares, { app }) => {
      app.use(injectEmployeeIdMiddleware);
      return middlewares;
    },
  },
});
