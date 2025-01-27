import { createApp } from 'vue';
import './style.css';
import Login from '../../frontend/src/components/Login.vue';
import { router } from './router/router.js'

const app = createApp(Login);
app.use(router)
app.mount('#app'); // Mount the app