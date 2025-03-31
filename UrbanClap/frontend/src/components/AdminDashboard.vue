<template>
  <div class="container-fluid">
    <div class="row my-4">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center my-4">
          <h1 class="text-center">Admin Dashboard</h1>
          <button class="btn btn-danger" @click="logout">Logout</button>
        </div>
        <ul class="nav nav-tabs mb-4">
          <li class="nav-item">
            <a class="nav-link" :class="{ active: activeTab === 'home' }" @click.prevent="activeTab = 'home'"
              href="#">Home</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" :class="{ active: activeTab === 'completedServices' }"
              @click.prevent="activeTab = 'completedServices'" href="#">Completed Services</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" :class="{ active: activeTab === 'customers' }" @click.prevent="activeTab = 'customers'"
              href="#">Customers</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" :class="{ active: activeTab === 'professionals' }"
              @click.prevent="activeTab = 'professionals'" href="#">Professionals</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" :class="{ active: activeTab === 'services' }" @click.prevent="activeTab = 'services'"
              href="#">Service Management</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" :class="{ active: activeTab === 'cities' }" @click.prevent="activeTab = 'cities'"
              href="#">City Management</a>
          </li>
        </ul>
        <div v-if="activeTab === 'home'" class="mb-5">
          <h2>Home</h2>
          <div class="table-responsive">
            <table class="table table-striped table-bordered">
              <thead class="table-light">
                <tr>
                  <th>Service Name</th>
                  <th>Customer Name</th>
                  <th>Professional Name</th>
                  <th>Status</th>
                  <th>Requested Date</th>
                  <th>Amount</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="service in homeServices" :key="service.id">
                  <td>{{ service.service_name }}</td>
                  <td>{{ service.customer_name }}</td>
                  <td>{{ service.professional_name }}</td>
                  <td>{{ service.status }}</td>
                  <td>{{ service.requested_date }}</td>
                  <td>{{ service.amount }}</td>
                </tr>
                <tr v-if="homeServices.length === 0">
                  <td colspan="6" class="text-center">No services found</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div v-if="activeTab === 'completedServices'" class="mb-5">
          <h2>Completed Services</h2>
          <div class="mb-3">
            <button class="btn btn-success" @click="exportCompletedServices">
              <i class="fas fa-download"></i> Export as CSV
            </button>
          </div>
          <div class="table-responsive">
            <table class="table table-striped table-bordered">
              <thead class="table-light">
                <tr>
                  <th>Service Name</th>
                  <th>Customer Name</th>
                  <th>Professional Name</th>
                  <th>Rating</th>
                  <th>Review</th>
                  <th>Date of Service</th>
                  <th>Amount</th>
                  <th>Payment Status</th>
                  <th>Payment Method</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="service in completedServices" :key="service.id">
                  <td>{{ service.service_name }}</td>
                  <td>{{ service.customer_name }}</td>
                  <td>{{ service.professional_name }}</td>
                  <td>{{ service.review?.rating || 'No rating' }}</td>
                  <td>{{ service.review?.comment || 'No review' }}</td>
                  <td>{{ service.date_of_completion }}</td>
                  <td>{{ service.amount }}</td>
                  <td>{{ service.payment_status }}</td>
                  <td>{{ service.payment_method }}</td>
                </tr>
                <tr v-if="completedServices.length === 0">
                  <td colspan="9" class="text-center">No completed services found</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div v-if="activeTab === 'customers'" class="mb-5">
          <h2>Customers</h2>
          <div class="table-responsive">
            <table class="table table-striped table-bordered">
              <thead class="table-light">
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Phone</th>
                  <th>City</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="customer in customers" :key="customer.user_id">
                  <td>{{ customer.name }}</td>
                  <td>{{ customer.email }}</td>
                  <td>{{ customer.phone }}</td>
                  <td>{{ customer.city }}</td>
                  <td>
                    <span :class="customer.is_blocked ? 'badge bg-danger' : 'badge bg-success'">
                      {{ customer.is_blocked ? 'Blocked' : 'Active' }}
                    </span>
                  </td>
                  <td>
                    <button class="btn btn-sm" :class="customer.is_blocked ? 'btn-success' : 'btn-danger'"
                      @click="toggleBlockStatus(customer)">
                      {{ customer.is_blocked ? 'Unblock' : 'Block' }}
                    </button>
                  </td>
                </tr>
                <tr v-if="customers.length === 0">
                  <td colspan="6" class="text-center">No customers found</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div v-if="activeTab === 'professionals'" class="mb-5">
          <h2>Professionals</h2>
          <div class="table-responsive">
            <table class="table table-striped table-bordered">
              <thead class="table-light">
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Phone</th>
                  <th>Service Type</th>
                  <th>City</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="professional in professionals" :key="professional.user_id">
                  <td>{{ professional.name }}</td>
                  <td>{{ professional.email }}</td>
                  <td>{{ professional.phone }}</td>
                  <td>{{ professional.service_type }}</td>
                  <td>{{ professional.city }}</td>
                  <td>
                    <span v-if="professional.is_blocked" class="badge bg-danger">Blocked</span>
                    <span v-else-if="professional.is_verified" class="badge bg-success">Verified</span>
                    <span v-else class="badge bg-warning text-dark">Unverified</span>
                  </td>
                  <td>
                    <button v-if="!professional.is_verified && !professional.is_blocked"
                      class="btn btn-sm btn-primary me-1" @click="verifyProfessional(professional)">
                      Verify
                    </button>
                    <button class="btn btn-sm" :class="professional.is_blocked ? 'btn-success' : 'btn-danger'"
                      @click="toggleBlockStatus(professional)">
                      {{ professional.is_blocked ? 'Unblock' : 'Block' }}
                    </button>
                  </td>
                </tr>
                <tr v-if="professionals.length === 0">
                  <td colspan="7" class="text-center">No professionals found</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div v-if="activeTab === 'services'" class="mb-5">
          <h2>Service Management</h2>
          <div class="table-responsive">
            <table class="table table-striped table-bordered">
              <thead class="table-light">
                <tr>
                  <th>Service Name</th>
                  <th>Description</th>
                  <th>Base Price</th>
                  <th>Time Required</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="service in services" :key="service.id">
                  <td>{{ service.name }}</td>
                  <td>{{ service.description }}</td>
                  <td>{{ service.base_price }}</td>
                  <td>{{ service.time_required }}</td>
                  <td>
                    <button class="btn btn-sm btn-primary me-1" @click="openEditServiceModal(service)">Edit</button>
                    <button class="btn btn-sm btn-danger" @click="deleteService(service.id)">Delete</button>
                  </td>
                </tr>
                <tr v-if="services.length === 0">
                  <td colspan="5" class="text-center">No services found</td>
                </tr>
              </tbody>
            </table>
          </div>
          <button class="btn btn-primary mt-3" @click="openAddServiceModal">Add New Service</button>
        </div>
        <div v-if="activeTab === 'cities'" class="mb-5">
          <h2>City Management</h2>
          <div class="table-responsive">
            <table class="table table-striped table-bordered">
              <thead class="table-light">
                <tr>
                  <th>City Name</th>
                  <th>Pincode</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="city in cities" :key="city.id">
                  <td>{{ city.name }}</td>
                  <td>{{ city.pincode }}</td>
                  <td>
                    <button class="btn btn-sm btn-primary me-1" @click="openEditCityModal(city)">Edit</button>
                    <button class="btn btn-sm btn-danger" @click="deleteCity(city.id)">Delete</button>
                  </td>
                </tr>
                <tr v-if="cities.length === 0">
                  <td colspan="3" class="text-center">No cities found</td>
                </tr>
              </tbody>
            </table>
          </div>
          <button class="btn btn-primary mt-3" @click="openAddCityModal">Add New City</button>
        </div>
      </div>
    </div>
    <div class="modal fade" id="editCityModal" tabindex="-1" aria-labelledby="editCityModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="editCityModalLabel">Edit City</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveCity">
              <div class="mb-3">
                <label for="cityName" class="form-label">City Name</label>
                <input type="text" class="form-control" id="cityName" v-model="editingCity.name" required>
              </div>
              <div class="mb-3">
                <label for="cityPincode" class="form-label">Pincode</label>
                <input type="text" class="form-control" id="cityPincode" v-model="editingCity.pincode" required>
              </div>
              <button type="submit" class="btn btn-primary">Save Changes</button>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div class="modal fade" id="addCityModal" tabindex="-1" aria-labelledby="addCityModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="addCityModalLabel">Add New City</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="addCity">
              <div class="mb-3">
                <label for="newCityName" class="form-label">City Name</label>
                <input type="text" class="form-control" id="newCityName" v-model="newCity.name" required>
              </div>
              <div class="mb-3">
                <label for="newCityPincode" class="form-label">Pincode</label>
                <input type="text" class="form-control" id="newCityPincode" v-model="newCity.pincode" required>
              </div>
              <button type="submit" class="btn btn-primary">Add City</button>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div class="modal fade" id="addServiceModal" tabindex="-1" aria-labelledby="addServiceModalLabel"
      aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="addServiceModalLabel">Add New Service</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="addService">
              <div class="mb-3">
                <label for="serviceName" class="form-label">Service Name</label>
                <input type="text" class="form-control" id="serviceName" v-model="newService.name" required>
              </div>
              <div class="mb-3">
                <label for="serviceDescription" class="form-label">Description</label>
                <textarea class="form-control" id="serviceDescription" v-model="newService.description"
                  required></textarea>
              </div>
              <div class="mb-3">
                <label for="servicePrice" class="form-label">Base Price</label>
                <input type="number" class="form-control" id="servicePrice" v-model="newService.base_price" required>
              </div>
              <div class="mb-3">
                <label for="serviceTime" class="form-label">Time Required</label>
                <input type="text" class="form-control" id="serviceTime" v-model="newService.time_required" required>
              </div>
              <button type="submit" class="btn btn-primary">Add Service</button>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div class="modal fade" id="editServiceModal" tabindex="-1" aria-labelledby="editServiceModalLabel"
      aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="editServiceModalLabel">Edit Service</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveService">
              <div class="mb-3">
                <label for="editServiceName" class="form-label">Service Name</label>
                <input type="text" class="form-control" id="editServiceName" v-model="editingService.name" required>
              </div>
              <div class="mb-3">
                <label for="editServiceDescription" class="form-label">Description</label>
                <textarea class="form-control" id="editServiceDescription" v-model="editingService.description"
                  required></textarea>
              </div>
              <div class="mb-3">
                <label for="editServicePrice" class="form-label">Base Price</label>
                <input type="number" class="form-control" id="editServicePrice" v-model="editingService.base_price"
                  required>
              </div>
              <div class="mb-3">
                <label for="editServiceTime" class="form-label">Time Required</label>
                <input type="text" class="form-control" id="editServiceTime" v-model="editingService.time_required"
                  required>
              </div>
              <button type="submit" class="btn btn-primary">Save Changes</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import api from '@/services/api';
export default {
  name: 'AdminDashboard',
  data() {
    return {
      activeTab: 'home',
      customers: [],
      professionals: [],
      services: [],
      cities: [],
      completedServices: [],
      homeServices: [],
      requestedServices: [],
      acceptedServices: [],
      rejectedServices: [],
      scheduledTodayServices: [],
      ongoingServices: [],
      editingCity: { id: null, name: '', pincode: '' },
      newCity: { name: '', pincode: '' },
      editingService: { id: null, name: '', description: '', base_price: '', time_required: '' },
      newService: { name: '', description: '', base_price: '', time_required: '' },
      loading: true,
      error: null
    };
  },
  mounted() {
    this.fetchUserData();
    this.fetchServices();
    this.fetchCities();
    this.fetchServiceRequests();
  },
  methods: {
    async fetchUserData() {
      try {
        console.log("Fetching user data...");
        const token = localStorage.getItem("jwt");
        if (!token) {
          console.error("No token found. Redirecting to login.");
          this.$router.push("/login");
          return;
        }
        const response = await api.get('/admin/users', {
          headers: { Authorization: `Bearer ${token}` }
        });
        console.log('User data response:', response.data);
        this.customers = response.data.customers || [];
        this.professionals = response.data.professionals || [];
        this.loading = false;
      } catch (error) {
        console.error('Error fetching user data:', error);
        this.error = 'Failed to load user data';
        this.loading = false;
      }
    },
    async fetchServices() {
      try {
        const token = localStorage.getItem("jwt");
        if (!token) {
          console.error("No token found. Redirecting to login.");
          this.$router.push("/login");
          return;
        }
        const response = await api.get('/services', {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.services = response.data.services || [];
      } catch (error) {
        console.error('Error fetching services:', error);
      }
    },
    async fetchCities() {
      try {
        const token = localStorage.getItem("jwt");
        if (!token) {
          console.error("No token found. Redirecting to login.");
          this.$router.push("/login");
          return;
        }
        const response = await api.get('/cities', {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.cities = response.data.cities || [];
      } catch (error) {
        console.error('Error fetching cities:', error);
      }
    },
    async fetchServiceRequests() {
      try {
        const token = localStorage.getItem("jwt");
        if (!token) {
          console.error("No token found. Redirecting to login.");
          this.$router.push("/login");
          return;
        }
        const response = await api.get('/admin/service-requests', {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        // Process completed services to ensure unique entries
        this.completedServices = response.data.completed_services.reduce((unique, service) => {
          const exists = unique.find(item => item.id === service.id);
          if (!exists) {
            unique.push(service);
          }
          return unique;
        }, []);
        
        this.requestedServices = response.data.requested_services;
        this.acceptedServices = response.data.accepted_services;
        this.rejectedServices = response.data.rejected_services;
        this.scheduledTodayServices = response.data.scheduled_today;
        this.ongoingServices = response.data.ongoing_services;
        this.homeServices = [
          ...this.scheduledTodayServices,
          ...this.ongoingServices,
          ...this.requestedServices,
          ...this.acceptedServices,
          ...this.rejectedServices
        ];
      } catch (error) {
        console.error('Error fetching service requests:', error);
      }
    },
    async toggleBlockStatus(user) {
      try {
        const newStatus = user.is_blocked ? 'unblocked' : 'blocked';
        console.log(`Updating user ${user.user_id} to status: ${newStatus}`);
        const token = localStorage.getItem("jwt");
        if (!token) {
          console.error("No token found. Redirecting to login.");
          this.$router.push("/login");
          return;
        }
        await api.patch(`/admin/users/${user.user_id}`, { status: newStatus }, {
          headers: { Authorization: `Bearer ${token}` }
        });
        console.log(`User ${user.user_id} updated successfully to ${newStatus}`);
        user.is_blocked = !user.is_blocked;
      } catch (error) {
        console.error(`Error updating user status:`, error);
        alert(`Failed to update user status: ${error.response?.data?.message || error.message}`);
      }
    },
    async verifyProfessional(professional) {
      try {
        console.log(`Verifying professional with user_id: ${professional.user_id}`);
        const token = localStorage.getItem("jwt");
        if (!token) {
          console.error("No token found. Redirecting to login.");
          this.$router.push("/login");
          return;
        }
        await api.patch(`/admin/users/${professional.user_id}`, { status: 'verified' }, {
          headers: { Authorization: `Bearer ${token}` }
        });
        console.log(`Professional ${professional.user_id} verified successfully`);
        professional.is_verified = true;
      } catch (error) {
        console.error('Error verifying professional:', error);
        alert(`Failed to verify professional: ${error.response?.data?.message || error.message}`);
      }
    },
    openAddServiceModal() {
      this.newService = { name: '', description: '', base_price: '', time_required: '' };
      const modal = new bootstrap.Modal(document.getElementById('addServiceModal'));
      modal.show();
    },
    openEditServiceModal(service) {
      this.editingService = { ...service };
      const modal = new bootstrap.Modal(document.getElementById('editServiceModal'));
      modal.show();
    },
    async addService() {
      try {
        const token = localStorage.getItem("jwt");
        if (!token) {
          console.error("No token found. Redirecting to login.");
          this.$router.push("/login");
          return;
        }
        await api.post('/manageservices', this.newService, {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.fetchServices();
        const modal = bootstrap.Modal.getInstance(document.getElementById('addServiceModal'));
        modal.hide();
      } catch (error) {
        console.error('Error adding service:', error);
      }
    },
    async saveService() {
      try {
        const token = localStorage.getItem("jwt");
        if (!token) {
          console.error("No token found. Redirecting to login.");
          this.$router.push("/login");
          return;
        }
        await api.put(`/manageservices/${this.editingService.id}`, this.editingService, {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.fetchServices();
        const modal = bootstrap.Modal.getInstance(document.getElementById('editServiceModal'));
        modal.hide();
      } catch (error) {
        console.error('Error saving service:', error);
      }
    },
    async deleteService(serviceId) {
      try {
        const token = localStorage.getItem("jwt");
        if (!token) {
          console.error("No token found. Redirecting to login.");
          this.$router.push("/login");
          return;
        }
        await api.delete(`/manageservices/${serviceId}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.services = this.services.filter(service => service.id !== serviceId);
      } catch (error) {
        console.error('Error deleting service:', error);
      }
    },
    openAddCityModal() {
      this.newCity = { name: '', pincode: '' };
      const modal = new bootstrap.Modal(document.getElementById('addCityModal'));
      modal.show();
    },
    openEditCityModal(city) {
      this.editingCity = { ...city };
      const modal = new bootstrap.Modal(document.getElementById('editCityModal'));
      modal.show();
    },
    async addCity() {
      try {
        const token = localStorage.getItem("jwt");
        if (!token) {
          console.error("No token found. Redirecting to login.");
          this.$router.push("/login");
          return;
        }
        await api.post('/cities', this.newCity, {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.fetchCities();
        const modal = bootstrap.Modal.getInstance(document.getElementById('addCityModal'));
        modal.hide();
      } catch (error) {
        console.error('Error adding city:', error);
      }
    },
    async saveCity() {
      try {
        const token = localStorage.getItem("jwt");
        if (!token) {
          console.error("No token found. Redirecting to login.");
          this.$router.push("/login");
          return;
        }
        await api.put(`/cities/${this.editingCity.id}`, this.editingCity, {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.fetchCities();
        const modal = bootstrap.Modal.getInstance(document.getElementById('editCityModal'));
        modal.hide();
      } catch (error) {
        console.error('Error saving city:', error);
      }
    },
    async deleteCity(cityId) {
      try {
        const token = localStorage.getItem("jwt");
        if (!token) {
          console.error("No token found. Redirecting to login.");
          this.$router.push("/login");
          return;
        }
        await api.delete(`/cities/${cityId}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.cities = this.cities.filter(city => city.id !== cityId);
      } catch (error) {
        console.error('Error deleting city:', error);
      }
    },
    async exportCompletedServices() {
      try {
        const token = localStorage.getItem("jwt");
        if (!token) {
          console.error("No token found. Redirecting to login.");
          this.$router.push("/login");
          return;
        }
        
        const response = await api.get('/admin/export-service-requests', {
          headers: { 
            Authorization: `Bearer ${token}`,
            'Accept': 'text/csv'
          },
          responseType: 'blob'
        });
        
        // Create a blob from the response data
        const blob = new Blob([response.data], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'completed_services.csv';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      } catch (error) {
        console.error('Error exporting completed services:', error);
        alert('Failed to export completed services');
      }
    },
    logout() {
      localStorage.removeItem("jwt");
      this.$router.push("/");
    }
  }
};
</script>
<style scoped>
.table th {
  font-weight: 600;
}

.table-responsive {
  overflow-x: auto;
}

@media (max-width: 992px) {
  .table {
    font-size: 0.9rem;
  }
}
</style>
