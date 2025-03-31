<template>
  <div class="container mt-5">
    <h2 class="text-center">Signup</h2>
    <div class="card p-4">
      <input v-model="email" class="form-control mb-2" placeholder="Email" type="email" required />
      <input v-model="password" type="password" class="form-control mb-2" placeholder="Password" required />
      <select v-model="role" class="form-select mb-2">
        <option value="customer">Customer</option>
        <option value="professional">Professional</option>
      </select>
      <div v-if="role !== 'admin'">
        <select v-model="city_id" class="form-select mb-2" required>
          <option value="">Select City</option>
          <option v-for="city in cities" :key="city.id" :value="city.id">
            {{ city.name }} ({{ city.pincode }})
          </option>
        </select>
      </div>
      <div v-if="role === 'customer'">
        <input v-model="name" class="form-control mb-2" placeholder="Full Name" required />
        <input v-model="phone" class="form-control mb-2" placeholder="Phone Number" required />
        <input v-model="address" class="form-control mb-2" placeholder="Address" required />
      </div>
      <div v-if="role === 'professional'">
        <input v-model="name" class="form-control mb-2" placeholder="Full Name" required />
        <input v-model="phone" class="form-control mb-2" placeholder="Phone Number" required />
        <select v-model="service_id" class="form-select mb-2" required>
          <option value="">Select Service</option>
          <option v-for="service in services" :key="service.id" :value="service.id">
            {{ service.name }} - ₹{{ service.base_price }} ({{ service.time_required }} mins)
          </option>
        </select>
        <input v-model="experience" type="number" class="form-control mb-2" placeholder="Experience (years)" required />
      </div>
      <button class="btn btn-primary w-100" @click="signup" :disabled="loading">
        {{ loading ? "Signing Up..." : "Signup" }}
      </button>
      <p v-if="message" class="text-danger mt-2">{{ message }}</p>
    </div>
  </div>
</template>
<script>
import api from "@/services/api";
import { useRouter } from "vue-router";
import { ref, onMounted } from "vue";
export default {
  setup() {
    const email = ref("");
    const password = ref("");
    const role = ref("customer");
    const name = ref("");
    const phone = ref("");
    const address = ref("");
    const service_id = ref("");
    const experience = ref(0);
    const city_id = ref("");
    const cities = ref([]);
    const services = ref([]);
    const message = ref("");
    const loading = ref(false);
    const router = useRouter();
    const fetchCities = async () => {
      try {
        const response = await api.get("/cities");
        cities.value = response.data.cities;
      } catch (error) {
        console.error("Failed to fetch cities:", error);
      }
    };
    const fetchServices = async () => {
      try {
        const response = await api.get("/services");
        services.value = response.data.services;
      } catch (error) {
        console.error("Failed to fetch services:", error);
      }
    };
    onMounted(() => {
      fetchCities();
      fetchServices();
    });
    const signup = async () => {
      try {
        message.value = "";
        loading.value = true;
        const signupData = {
          email: email.value,
          password: password.value,
          role: role.value,
        };
        if (role.value === "customer") {
          signupData.name = name.value;
          signupData.phone = phone.value;
          signupData.address = address.value;
          signupData.city_id = city_id.value;
        } else if (role.value === "professional") {
          signupData.name = name.value;
          signupData.phone = phone.value;
          signupData.service_type = services.value.find(s => s.id === service_id.value)?.name || "General";
          signupData.experience = experience.value;
          signupData.city_id = city_id.value;
        }
        await api.post("/signup", signupData);
        alert("Signup successful! Please login.");
        router.push("/login");
      } catch (error) {
        message.value = error.response?.data?.message || "Signup failed!";
      } finally {
        loading.value = false;
      }
    };
    return {
      email, password, role, name, phone, address, service_id, experience, city_id, cities, services, message, loading, signup
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
