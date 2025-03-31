<template>
  <div class="container">
    <div class="d-flex justify-content-between align-items-center my-4">
      <h1 class="text-center">Customer Dashboard</h1>
      <button class="btn btn-danger" @click="logout">Logout</button>
    </div>
    <ul class="nav nav-tabs">
      <li class="nav-item">
        <a class="nav-link" :class="{ active: activeTab === 'services' }" @click.prevent="activeTab = 'services'"
          href="#">Browse Services</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{ active: activeTab === 'myRequests' }" @click.prevent="activeTab = 'myRequests'"
          href="#">My Service Requests</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{ active: activeTab === 'profile' }" @click.prevent="activeTab = 'profile'"
          href="#">Profile</a>
      </li>
    </ul>
    <div v-if="activeTab === 'services'" class="mt-4">
      <h2>Available Services</h2>
      <div class="mb-3">
        <input type="text" class="form-control" v-model="searchQuery" placeholder="Search services..."
          @input="filterServices" />
      </div>
      <div class="row">
        <div v-for="service in filteredServices" :key="service.id" class="col-md-4 mb-4">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">{{ service.name }}</h5>
              <p class="card-text">{{ service.description }}</p>
              <p><strong>Base Price:</strong> ₹{{ service.base_price }}</p>
              <p><strong>Time Required:</strong> {{ service.time_required }} mins</p>
              <button class="btn btn-primary w-100" @click="openProfessionalsModal(service)">View Professionals</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-if="activeTab === 'myRequests'" class="mt-4">
      <h2>My Service Requests</h2>
      <div v-if="requestedServices.length > 0" class="mb-4">
        <h3 class="h5 mb-3">Requested Services</h3>
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>Service</th>
                <th>City</th>
                <th>Status</th>
                <th>Requested Date</th>
                <th>Date of Service</th>
                <th>PIN</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in requestedServices" :key="request.id">
                <td>{{ request.service_name }}</td>
                <td>{{ request.city }}</td>
                <td><span class="badge bg-warning text-dark">{{ request.status }}</span></td>
                <td>{{ request.requested_date }}</td>
                <td>{{ request.date_of_completion }}</td>
                <td>{{ request.pin }}</td>
                <td>
                  <button class="btn btn-sm btn-primary me-2" @click="openUpdateModal(request)">Update</button>
                  <button class="btn btn-sm btn-danger" @click="deleteRequest(request.id)">Cancel</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div v-if="acceptedServices.length > 0" class="mb-4">
        <h3 class="h5 mb-3">Accepted Services</h3>
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>Service</th>
                <th>City</th>
                <th>Status</th>
                <th>Requested Date</th>
                <th>Date of Service</th>
                <th>PIN</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in acceptedServices" :key="request.id">
                <td>{{ request.service_name }}</td>
                <td>{{ request.city }}</td>
                <td><span class="badge bg-success">{{ request.status }}</span></td>
                <td>{{ request.requested_date }}</td>
                <td>{{ request.date_of_completion }}</td>
                <td>{{ request.pin }}</td>
                <td>
                  <button class="btn btn-sm btn-primary me-2" @click="openUpdateModal(request)">Update</button>
                  <button class="btn btn-sm btn-danger" @click="deleteRequest(request.id)">Cancel</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div v-if="rejectedServices.length > 0" class="mb-4">
        <h3 class="h5 mb-3">Rejected Services</h3>
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>Service</th>
                <th>City</th>
                <th>Status</th>
                <th>Requested Date</th>
                <th>Date of Service</th>
                <th>PIN</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in rejectedServices" :key="request.id">
                <td>{{ request.service_name }}</td>
                <td>{{ request.city }}</td>
                <td><span class="badge bg-danger">{{ request.status }}</span></td>
                <td>{{ request.requested_date }}</td>
                <td>{{ request.date_of_completion }}</td>
                <td>{{ request.pin }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div v-if="scheduledToday.length > 0" class="mb-4">
        <h3 class="h5 mb-3">Scheduled for Today</h3>
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>Service</th>
                <th>City</th>
                <th>Status</th>
                <th>Requested Date</th>
                <th>Date of Service</th>
                <th>PIN</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in scheduledToday" :key="request.id">
                <td>{{ request.service_name }}</td>
                <td>{{ request.city }}</td>
                <td><span class="badge bg-info">{{ request.status }}</span></td>
                <td>{{ request.requested_date }}</td>
                <td>{{ request.date_of_completion }}</td>
                <td>{{ request.pin }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div v-if="ongoingServices.length > 0" class="mb-4">
        <h3 class="h5 mb-3">Ongoing Services</h3>
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>Service</th>
                <th>City</th>
                <th>Status</th>
                <th>Requested Date</th>
                <th>Date of Service</th>
                <th>PIN</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in ongoingServices" :key="request.id">
                <td>{{ request.service_name }}</td>
                <td>{{ request.city }}</td>
                <td><span class="badge bg-primary">{{ request.status }}</span></td>
                <td>{{ request.requested_date }}</td>
                <td>{{ request.date_of_completion }}</td>
                <td>{{ request.pin }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div v-if="completedServices.length > 0" class="mb-4">
        <h3 class="h5 mb-3">Completed Services</h3>
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>Service</th>
                <th>City</th>
                <th>Status</th>
                <th>Requested Date</th>
                <th>Date of Service</th>
                <th>PIN</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in completedServices" :key="request.id">
                <td>{{ request.service_name }}</td>
                <td>{{ request.city }}</td>
                <td><span class="badge bg-success">{{ request.status }}</span></td>
                <td>{{ request.requested_date }}</td>
                <td>{{ request.date_of_completion }}</td>
                <td>{{ request.pin }}</td>
                <td>
                  <button v-if="isReviewPending(request.id)" class="btn btn-sm btn-secondary"
                    @click="openReviewModal(request)">Write Review</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <div v-if="activeTab === 'profile'" class="mt-4">
      <h2>Customer Profile</h2>
      <form @submit.prevent="updateProfile">
        <div class="mb-3">
          <label class="form-label">Name</label>
          <input type="text" class="form-control" v-model="profile.name" required />
        </div>
        <div class="mb-3">
          <label class="form-label">Email</label>
          <input type="email" class="form-control" v-model="profile.email" required />
        </div>
        <div class="mb-3">
          <label class="form-label">Phone</label>
          <input type="tel" class="form-control" v-model="profile.phone" required />
        </div>
        <div class="mb-3">
          <label class="form-label">Address</label>
          <input type="text" class="form-control" v-model="profile.address" required />
        </div>
        <div class="mb-3">
          <label class="form-label">City</label>
          <select class="form-select" v-model="profile.city_id" required>
            <option v-for="city in cities" :key="city.id" :value="city.id">{{ city.name }}</option>
          </select>
        </div>
        <button type="submit" class="btn btn-primary">Update Profile</button>
        <button type="button" class="btn btn-danger ms-2" @click="deleteProfile">Delete Profile</button>
      </form>
    </div>
    <div v-if="showModal" class="modal-wrapper">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Available Professionals</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <div v-if="loadingProfessionals" class="text-center my-4">
              <div class="spinner-border text-primary"></div>
            </div>
            <div v-else>
              <div v-if="professionals.length === 0" class="text-center text-muted">No professionals available.</div>
              <ul class="list-group" v-else>
                <li class="list-group-item" v-for="prof in professionals" :key="prof.id">
                  <div>
                    <h6>{{ prof.name }} ({{ prof.service_type }})</h6>
                    <p><strong>Experience:</strong> {{ prof.experience }} years</p>
                    <p><strong>Rating:</strong> {{ prof.rating || "No rating" }}</p>
                  </div>
                  <div class="date-picker-wrapper">
                    <label class="form-label">Select Date and Time</label>
                    <input type="datetime-local" v-model="completionDates[prof.id]" class="form-control"
                      :min="minDate" />
                  </div>
                  <button class="btn btn-success mt-2" @click="requestService(prof)">Request Service</button>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <div class="modal-backdrop" @click="closeModal"></div>
    </div>
    <div v-if="showUpdateModal" class="modal-wrapper">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Update Service Request</h5>
            <button type="button" class="btn-close" @click="closeUpdateModal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Select New Date and Time</label>
              <input type="datetime-local" v-model="updateForm.date_of_completion" class="form-control"
                :min="minDate" />
            </div>
            <button class="btn btn-primary" @click="updateRequest">Update</button>
          </div>
        </div>
      </div>
      <div class="modal-backdrop" @click="closeUpdateModal"></div>
    </div>
    <div v-if="showReviewModal" class="modal-wrapper">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Write a Review</h5>
            <button type="button" class="btn-close" @click="closeReviewModal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Rating</label>
              <select class="form-select" v-model="reviewForm.rating" required>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label">Comment</label>
              <textarea class="form-control" v-model="reviewForm.comment" rows="3"></textarea>
            </div>
            <button class="btn btn-primary" @click="submitReview">Submit Review</button>
          </div>
        </div>
      </div>
      <div class="modal-backdrop" @click="closeReviewModal"></div>
    </div>
  </div>
</template>
<script>
import api from "@/services/api";
export default {
  name: "CustomerDashboard",
  data() {
    return {
      activeTab: "services",
      services: [],
      professionals: [],
      selectedService: null,
      showModal: false,
      showUpdateModal: false,
      showReviewModal: false,
      loadingProfessionals: false,
      completionDates: {},
      updateForm: {
        request_id: null,
        date_of_completion: null
      },
      reviewForm: {
        request_id: null,
        rating: null,
        comment: ""
      },
      requestedServices: [],
      acceptedServices: [],
      rejectedServices: [],
      scheduledToday: [],
      ongoingServices: [],
      completedServices: [],
      pendingReviews: [],
      profile: {
        name: "",
        email: "",
        phone: "",
        address: "",
        city_id: null
      },
      cities: [],
      searchQuery: ""
    };
  },
  computed: {
    minDate() {
      const now = new Date();
      return now.toISOString().slice(0, 16);
    },
    filteredServices() {
      if (!this.searchQuery) {
        return this.services;
      }
      return this.services.filter(service =>
        service.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  },
  mounted() {
    this.fetchServices();
    this.fetchRequests();
    this.fetchProfile();
    this.fetchCities();
  },
  methods: {
    async fetchServices() {
      try {
        const response = await api.get("/services");
        this.services = response.data.services;
      } catch (error) {
        console.error("❌ Failed to fetch services:", error);
      }
    },
    async fetchRequests() {
      try {
        const token = localStorage.getItem("jwt");
        if (!token) {
          alert("⚠️ You need to login first!");
          this.$router.push("/login");
          return;
        }
        const response = await api.get("/service-requests", {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.requestedServices = response.data.requested_services || [];
        this.acceptedServices = response.data.accepted_services || [];
        this.rejectedServices = response.data.rejected_services || [];
        this.scheduledToday = response.data.scheduled_today || [];
        this.ongoingServices = response.data.ongoing_services || [];
        this.completedServices = response.data.completed_services || [];
        const reviewResponse = await api.get("/reviews", {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.pendingReviews = reviewResponse.data.pending_reviews || [];
      } catch (error) {
        console.error("❌ Failed to fetch service requests:", error);
      }
    },
    isReviewPending(requestId) {
      return this.pendingReviews.some(review => review.service_request_id === requestId);
    },
    async openProfessionalsModal(service) {
      this.selectedService = service;
      this.showModal = true;
      this.loadingProfessionals = true;
      this.completionDates = {};
      try {
        const token = localStorage.getItem("jwt");
        if (!token) {
          alert("⚠️ You need to login first!");
          this.$router.push("/login");
          return;
        }
        const response = await api.post("/professionals",
          { service_type: service.name },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        this.professionals = response.data.professionals;
      } catch (error) {
        console.error("❌ Failed to fetch professionals:", error);
        this.professionals = [];
      } finally {
        this.loadingProfessionals = false;
      }
    },
    formatDateTime(dateTimeStr) {
      if (!dateTimeStr) return null;
      const date = new Date(dateTimeStr);
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, "0");
      const day = String(date.getDate()).padStart(2, "0");
      const hours = String(date.getHours()).padStart(2, "0");
      const minutes = String(date.getMinutes()).padStart(2, "0");
      const seconds = "00";
      return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    },
    async requestService(professional) {
      try {
        const selectedDate = this.completionDates[professional.id];
        if (!selectedDate) {
          alert("⚠️ Please select a completion date and time.");
          return;
        }
        const token = localStorage.getItem("jwt");
        if (!token) {
          alert("⚠️ You need to login first!");
          this.$router.push("/login");
          return;
        }
        const formattedDate = this.formatDateTime(selectedDate);
        const requestData = {
          service_id: this.selectedService.id,
          professional_id: professional.id,
          date_of_completion: formattedDate
        };
        const response = await api.post("/service-requests", requestData, {
          headers: { Authorization: `Bearer ${token}` }
        });
        if (response.data) {
          alert("🎉 Service request created successfully!");
          this.fetchRequests();
          this.closeModal();
        }
      } catch (error) {
        console.error("❌ Failed to request service:", error.response?.data || error.message);
        alert(error.response?.data?.message || "❌ Failed to request service. Please try again.");
      }
    },
    closeModal() {
      this.showModal = false;
      this.professionals = [];
      this.completionDates = {};
    },
    openUpdateModal(request) {
      this.updateForm = {
        request_id: request.id,
        date_of_completion: request.date_of_completion
      };
      this.showUpdateModal = true;
    },
    closeUpdateModal() {
      this.showUpdateModal = false;
      this.updateForm = {
        request_id: null,
        date_of_completion: null
      };
    },
    async updateRequest() {
      try {
        if (!this.updateForm.date_of_completion) {
          alert("⚠️ Please select a completion date and time.");
          return;
        }
        const token = localStorage.getItem("jwt");
        if (!token) {
          alert("⚠️ You need to login first!");
          this.$router.push("/login");
          return;
        }
        const formattedDate = this.formatDateTime(this.updateForm.date_of_completion);
        await api.put(`/service-requests/${this.updateForm.request_id}`, {
          date_of_completion: formattedDate
        }, {
          headers: { Authorization: `Bearer ${token}` }
        });
        alert("✅ Service request updated successfully!");
        this.fetchRequests();
        this.closeUpdateModal();
      } catch (error) {
        console.error("❌ Failed to update service request:", error);
        alert(error.response?.data?.message || "❌ Failed to update service request.");
      }
    },
    async deleteRequest(requestId) {
      if (!confirm("❌ Are you sure you want to cancel this service request?")) {
        return;
      }
      try {
        const token = localStorage.getItem("jwt");
        if (!token) {
          alert("⚠️ You need to login first!");
          this.$router.push("/login");
          return;
        }
        await api.delete(`/service-requests/${requestId}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        alert("✅ Service request cancelled successfully!");
        this.fetchRequests();
      } catch (error) {
        console.error("❌ Failed to cancel service request:", error);
        alert(error.response?.data?.message || "❌ Failed to cancel service request.");
      }
    },
    async fetchProfile() {
      try {
        const token = localStorage.getItem("jwt");
        if (!token) {
          alert("⚠️ You need to login first!");
          this.$router.push("/login");
          return;
        }
        const response = await api.get("/customer/profile", {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.profile = response.data;
      } catch (error) {
        console.error("❌ Failed to fetch profile:", error);
      }
    },
    async updateProfile() {
      try {
        const token = localStorage.getItem("jwt");
        if (!token) {
          alert("⚠️ You need to login first!");
          this.$router.push("/login");
          return;
        }
        const response = await api.put("/customer/profile", this.profile, {
          headers: { Authorization: `Bearer ${token}` }
        });
        alert("✅ Profile updated successfully!");
      } catch (error) {
        console.error("❌ Failed to update profile:", error);
        alert(error.response?.data?.message || "❌ Failed to update profile.");
      }
    },
    async deleteProfile() {
      if (!confirm("❌ Are you sure you want to delete your profile?")) {
        return;
      }
      try {
        const token = localStorage.getItem("jwt");
        if (!token) {
          alert("⚠️ You need to login first!");
          this.$router.push("/login");
          return;
        }
        await api.delete("/customer/profile", {
          headers: { Authorization: `Bearer ${token}` }
        });
        alert("✅ Profile deleted successfully!");
        this.$router.push("/login");
      } catch (error) {
        console.error("❌ Failed to delete profile:", error);
        alert(error.response?.data?.message || "❌ Failed to delete profile.");
      }
    },
    async fetchCities() {
      try {
        const response = await api.get("/cities");
        this.cities = response.data.cities;
      } catch (error) {
        console.error("❌ Failed to fetch cities:", error);
      }
    },
    openReviewModal(request) {
      this.reviewForm = {
        request_id: request.id,
        rating: null,
        comment: ""
      };
      this.showReviewModal = true;
    },
    closeReviewModal() {
      this.showReviewModal = false;
      this.reviewForm = {
        request_id: null,
        rating: null,
        comment: ""
      };
    },
    async submitReview() {
      try {
        const token = localStorage.getItem("jwt");
        if (!token) {
          alert("⚠️ You need to login first!");
          this.$router.push("/login");
          return;
        }
        const response = await api.post(`/reviews/${this.reviewForm.request_id}`, this.reviewForm, {
          headers: { Authorization: `Bearer ${token}` }
        });
        alert("✅ Review submitted successfully!");
        this.fetchRequests();
        this.closeReviewModal();
      } catch (error) {
        console.error("❌ Failed to submit review:", error);
        alert(error.response?.data?.message || "❌ Failed to submit review.");
      }
    },
    filterServices() {
    },
    logout() {
      localStorage.removeItem("jwt");
      this.$router.push("/");
    }
  }
};
</script>
<style scoped>
.badge {
  font-size: 0.9rem;
  padding: 0.5em;
}

.modal-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: -1;
}

.modal-dialog {
  z-index: 1051;
  margin: 1.75rem auto;
}

.date-picker-wrapper {
  margin: 10px 0;
}

.table-responsive {
  margin-bottom: 1rem;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.table {
  margin-bottom: 0;
}
</style>
