import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../components/stores/authStore';

import LoginPage from '../components/LoginPage.vue';
import DashboardPage from '../components/Dashboard/DashboardPage.vue';
import EntityDetailsPage from '../components/EntityDetails/EntityDetailsPage.vue';

const routes = [
    { path: '/', component: LoginPage },
    { path: '/dashboard', component: DashboardPage, meta: { requiresAuth: true } },
    { path: '/employees', name: 'employeeDetails',component: EntityDetailsPage, meta: { requiresAuth: true } },
    { path: '/specimens', name: 'specimenDetails',component: EntityDetailsPage, meta: { requiresAuth: true } },
    { path: '/origins', name: 'originDetails',component: EntityDetailsPage, meta: { requiresAuth: true } },
    { path: '/missions', name: 'missionDetails',component: EntityDetailsPage, meta: { requiresAuth: true } },
    { path: '/departments', name: 'departmentDetails',component: EntityDetailsPage, meta: { requiresAuth: true } },
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
      next("/"); // Redirect to login if not authenticated
    } else {
      next(); // Continue as normal
    }
  });
  

export default router;