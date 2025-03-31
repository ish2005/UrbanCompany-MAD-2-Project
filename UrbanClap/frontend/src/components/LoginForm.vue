<template>
  <div class="container mt-5">
    <h2 class="text-center">Login</h2>
    <div class="card p-4">
      <input v-model="email" class="form-control mb-2" placeholder="Email" type="email" required />
      <input v-model="password" type="password" class="form-control mb-2" placeholder="Password" required />
      <button class="btn btn-primary w-100" @click="login" :disabled="loading">
        {{ loading ? "Logging in..." : "Login" }}
      </button>
      <p v-if="message" class="text-danger mt-2">{{ message }}</p>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
import { useRouter } from "vue-router";
import { ref } from "vue";

export default {
  setup() {
    const email = ref("");
    const password = ref("");
    const message = ref("");
    const loading = ref(false);
    const router = useRouter();

    const login = async () => {
      try {
        message.value = "";
        loading.value = true;
        const response = await api.post("/login", {
          email: email.value,
          password: password.value,
        });

        const user = response.data.user;
        console.log("Login successful:", user);
        localStorage.setItem("jwt", user.token);
        localStorage.setItem("userRole", user.role);
        localStorage.setItem("userId", user.id);
        
        console.log("Stored token:", localStorage.getItem("jwt"));
        console.log("Stored role:", localStorage.getItem("userRole"));
        
        if (user.role === "customer") {
          router.replace("/customer-dashboard");
        } else if (user.role === "professional") {
          router.replace("/professional-dashboard");
        } else if (user.role === "admin") {
          router.replace("/admin-dashboard");
        }
      } catch (error) {
        message.value = error.response?.data?.message || "Login failed!";
      } finally {
        loading.value = false;
      }
    };

    return {
      email,
      password,
      message,
      loading,
      login,
    };
  },
};
</script>

<style scoped>
.container {
  max-width: 400px;
}

button {
  margin-top: 10px;
}
</style>
