import { defineConfig } from 'vite';
import { injectEmployeeIdMiddleware } from './middleware/injectEmployeeIdMiddleware';
import vue from '@vitejs/plugin-vue';
import svgLoader from 'vite-svg-loader';


const apiKey = process.env.VITE_API_ENDPOINT;
export default defineConfig({
  plugins: [
    vue(),
    svgLoader(),
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
