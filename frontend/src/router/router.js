import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../components/stores/authStore';

import LoginPage from '../components/LoginPage.vue';
import DashboardPage from '../components/Dashboard/DashboardPage.vue';
import EntityDetailsPage from '../components/EntityDetailsPage.vue';

const routes = [
    { path: '/', component: LoginPage },
    { path: '/dashboard', component: DashboardPage, meta: { requiresAuth: true } },
    { path: '/employees/:id', component: EntityDetailsPage, meta: { requiresAuth: true } },
    { path: '/specimens/:id', component: EntityDetailsPage, meta: { requiresAuth: true } },
    { path: '/origins/:id', component: EntityDetailsPage, meta: { requiresAuth: true } },
    { path: '/missions/:id', component: EntityDetailsPage, meta: { requiresAuth: true } },
    { path: '/departments/:id', component: EntityDetailsPage, meta: { requiresAuth: true } },
]

const router = createRouter({
    routes,
    history: createWebHistory(),
})

router.beforeEach(async (to, from, next) => {
    const authStore = useAuthStore();
  
    if (authStore.loading) {
      await authStore.verifyToken();
    }
  
    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
      next("/login"); // Redirect to login if not authenticated
    } else {
      next(); // Continue as normal
    }
  });
  

export default router;