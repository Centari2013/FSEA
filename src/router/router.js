import { createRouter, createWebHashHistory } from 'vue-router';
import { useAuthStore } from '../components/stores/authStore';
import { nextTick } from 'vue';
import LoginPage from '../components/LoginPage.vue';
import DashboardPage from '../components/Dashboard/DashboardPage.vue';
import EntityDetailsPage from '../components/EntityDetails/EntityDetailsPage.vue';

const routes = [
    { path: '/', component: LoginPage },
    { path: '/dashboard', component: DashboardPage, meta: { requiresAuth: true, title: 'Dashboard' } },
    { path: '/employees', name: 'employeeDetails',component: EntityDetailsPage, meta: { requiresAuth: true, title: 'Employee Details' } },
    { path: '/specimens', name: 'specimenDetails',component: EntityDetailsPage, meta: { requiresAuth: true, title: 'Specimen Details' } },
    { path: '/origins', name: 'originDetails',component: EntityDetailsPage, meta: { requiresAuth: true, title: 'Origin Details' } },
    { path: '/missions', name: 'missionDetails',component: EntityDetailsPage, meta: { requiresAuth: true, title: 'Mission Details' } },
    { path: '/departments', name: 'departmentDetails',component: EntityDetailsPage, meta: { requiresAuth: true, title: 'Department Details' } },
]

const router = createRouter({
    routes,
    history: createWebHashHistory(),
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

  router.afterEach( async (to, from) => {
    nextTick(() => {
      document.title = to.meta.title || 'FSEA';
  });
  });

export default router;