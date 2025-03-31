import { createRouter, createWebHistory } from "vue-router";
import HomePage from "@/components/HomePage.vue";
import LoginForm from "@/components/LoginForm.vue";
import SignupForm from "@/components/SignupForm.vue";
import CustomerDashboard from "@/components/CustomerDashboard.vue";
import ProfessionalDashboard from "@/components/ProfessionalDashboard.vue";
import AdminDashboard from "@/components/AdminDashboard.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: HomePage
  },
  {
    path: "/login",
    name: "Login",
    component: LoginForm
  },
  {
    path: "/signup",
    name: "Signup",
    component: SignupForm
  },
  {
    path: "/customer-dashboard",
    name: "CustomerDashboard",
    component: CustomerDashboard,
    meta: { requiresAuth: true, role: "customer" }
  },
  {
    path: "/professional-dashboard",
    name: "ProfessionalDashboard",
    component: ProfessionalDashboard,
    meta: { requiresAuth: true, role: "professional" }
  },
  {
    path: "/admin-dashboard",
    name: "AdminDashboard",
    component: AdminDashboard,
    meta: { requiresAuth: true, role: "admin" }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("jwt");
  const userRole = localStorage.getItem("userRole");

  console.log("Navigation guard - To:", to.path);
  console.log("Navigation guard - Token:", token);
  console.log("Navigation guard - Role:", userRole);

  // Allow public access to home, login, and signup
  if (!to.meta.requiresAuth) {
    console.log("Public route, allowing access");
    next();
    return;
  }

  // Check authentication and role for protected routes
  if (!token) {
    console.log("No token found, redirecting to login");
    next("/login");
    return;
  }

  if (to.meta.role && to.meta.role !== userRole) {
    console.log("Role mismatch, redirecting to appropriate dashboard");
    // Redirect to appropriate dashboard based on role
    switch (userRole) {
      case "customer":
        next("/customer-dashboard");
        break;
      case "professional":
        next("/professional-dashboard");
        break;
      case "admin":
        next("/admin-dashboard");
        break;
      default:
        next("/login");
    }
    return;
  }

  console.log("Access granted");
  next();
});

export default router;