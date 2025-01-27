import { createRouter, createWebHistory } from 'vue-router';

import Login from '../../../frontend/src/components/Login.vue';

const routes = [
    { path: '/', component: Login },
]

const router = createRouter({
    routes,
    history: createWebHistory(),
})