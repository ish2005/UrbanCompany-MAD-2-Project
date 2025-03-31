<template>
  <div class="container">
    <div class="d-flex justify-content-between align-items-center my-4">
      <h1 class="text-center">Professional Dashboard</h1>
      <button class="btn btn-danger" @click="logout">Logout</button>
    </div>
    <div class="mb-4">
      <button class="btn btn-primary" @click="openProfileModal">View/Edit Profile</button>
    </div>
    <ul class="nav nav-tabs">
      <li class="nav-item">
        <a class="nav-link" :class="{ active: activeTab === 'home' }" @click.prevent="activeTab = 'home'"
          href="#">Home</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{ active: activeTab === 'requests' }" @click.prevent="activeTab = 'requests'"
          href="#">Service Requests</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{ active: activeTab === 'services' }" @click.prevent="activeTab = 'services'"
          href="#">Services</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{ active: activeTab === 'serviceRequests' }"
          @click.prevent="activeTab = 'serviceRequests'" href="#">Service Addition Requests</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{ active: activeTab === 'profile' }" @click.prevent="activeTab = 'profile'"
          href="#">Profile</a>
      </li>
    </ul>
    <div v-if="activeTab === 'home'" class="mt-4">
      <div v-if="scheduledToday.length > 0" class="mb-4">
        <h3 class="h5 mb-3">Scheduled Today</h3>
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>Service</th>
                <th>City</th>
                <th>Address</th>
                <th>Status</th>
                <th>Service Request Date</th>
                <th>Amount (₹)</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in scheduledToday" :key="request.id">
                <td>{{ request.service_name }}</td>
                <td>{{ request.city }}</td>
                <td>{{ request.address }}</td>
                <td><span class="badge bg-info">{{ request.status }}</span></td>
                <td>{{ request.requested_date }}</td>
                <td>₹{{ request.amount }}</td>
                <td>
                  <button v-if="request.status === 'scheduled'" class="btn btn-sm btn-primary me-2"
                    @click="updateRequestStatus(request.id, 'mark_reached')">
                    Mark Reached
                  </button>
                </td>
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
                <th>Address</th>
                <th>Status</th>
                <th>Service Request Date</th>
                <th>Amount (₹)</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in ongoingServices" :key="request.id">
                <td>{{ request.service_name }}</td>
                <td>{{ request.city }}</td>
                <td>{{ request.address }}</td>
                <td><span class="badge bg-primary">{{ request.status }}</span></td>
                <td>{{ request.requested_date }}</td>
                <td>₹{{ request.amount }}</td>
                <td>
                  <button v-if="request.status === 'in_progress'" class="btn btn-sm btn-success me-2"
                    @click="openStartServiceModal(request)">
                    Start Service
                  </button>
                  <button v-if="request.status === 'started'" class="btn btn-sm btn-success"
                    @click="updateRequestStatus(request.id, 'complete')">
                    Complete Service
                  </button>
                </td>
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
                <th>Address</th>
                <th>Status</th>
                <th>Service Request Date</th>
                <th>Date of Service</th>
                <th>Amount (₹)</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in completedServices" :key="request.id">
                <td>{{ request.service_name }}</td>
                <td>{{ request.city }}</td>
                <td>{{ request.address }}</td>
                <td><span class="badge bg-success">{{ request.status }}</span></td>
                <td>{{ request.requested_date }}</td>
                <td>{{ request.date_of_completion || 'N/A' }}</td>
                <td>₹{{ request.amount }}</td>
                <td>
                  <button v-if="request.status === 'completed'" class="btn btn-sm btn-primary"
                    @click="openTransactionModal(request)">
                    Complete Transaction
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div v-if="requestedServices.length > 0" class="mb-4">
        <h3 class="h5 mb-3">New Service Requests</h3>
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>Service</th>
                <th>City</th>
                <th>Address</th>
                <th>Status</th>
                <th>Service Request Date</th>
                <th>Amount (₹)</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in requestedServices" :key="request.id">
                <td>{{ request.service_name }}</td>
                <td>{{ request.city }}</td>
                <td>{{ request.address }}</td>
                <td><span class="badge bg-warning text-dark">{{ request.status }}</span></td>
                <td>{{ request.requested_date }}</td>
                <td>₹{{ request.amount }}</td>
                <td>
                  <button class="btn btn-sm btn-success me-2"
                    @click="updateRequestStatus(request.id, 'accept')">Accept</button>
                  <button class="btn btn-sm btn-danger"
                    @click="updateRequestStatus(request.id, 'reject')">Reject</button>
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
                <th>Address</th>
                <th>Status</th>
                <th>Service Request Date</th>
                <th>Amount (₹)</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in acceptedServices" :key="request.id">
                <td>{{ request.service_name }}</td>
                <td>{{ request.city }}</td>
                <td>{{ request.address }}</td>
                <td><span class="badge bg-success">{{ request.status }}</span></td>
                <td>{{ request.requested_date }}</td>
                <td>₹{{ request.amount }}</td>
                <td>
                  <button class="btn btn-sm btn-danger" @click="updateRequestStatus(request.id, 'reject')">
                    Reject
                  </button>
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
                <th>Address</th>
                <th>Status</th>
                <th>Service Request Date</th>
                <th>Amount (₹)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in rejectedServices" :key="request.id">
                <td>{{ request.service_name }}</td>
                <td>{{ request.city }}</td>
                <td>{{ request.address }}</td>
                <td><span class="badge bg-danger">{{ request.status }}</span></td>
                <td>{{ request.requested_date }}</td>
                <td>₹{{ request.amount }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div v-if="!hasAnyRequests" class="text-center text-muted mt-4">
        No service requests found.
      </div>
    </div>
    <div v-if="activeTab === 'requests'" class="mt-4">
      <div v-if="requestedServices.length > 0" class="mb-4">
        <h3 class="h5 mb-3">New Service Requests</h3>
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>Service</th>
                <th>City</th>
                <th>Address</th>
                <th>Status</th>
                <th>Service Request Date</th>
                <th>Amount (₹)</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in requestedServices" :key="request.id">
                <td>{{ request.service_name }}</td>
                <td>{{ request.city }}</td>
                <td>{{ request.address }}</td>
                <td><span class="badge bg-warning text-dark">{{ request.status }}</span></td>
                <td>{{ request.requested_date }}</td>
                <td>₹{{ request.amount }}</td>
                <td>
                  <button class="btn btn-sm btn-success me-2"
                    @click="updateRequestStatus(request.id, 'accept')">Accept</button>
                  <button class="btn btn-sm btn-danger"
                    @click="updateRequestStatus(request.id, 'reject')">Reject</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div v-if="scheduledToday.length > 0" class="mb-4">
        <h3 class="h5 mb-3">Scheduled Today</h3>
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>Service</th>
                <th>City</th>
                <th>Address</th>
                <th>Status</th>
                <th>Service Request Date</th>
                <th>Amount (₹)</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in scheduledToday" :key="request.id">
                <td>{{ request.service_name }}</td>
                <td>{{ request.city }}</td>
                <td>{{ request.address }}</td>
                <td><span class="badge bg-info">{{ request.status }}</span></td>
                <td>{{ request.requested_date }}</td>
                <td>₹{{ request.amount }}</td>
                <td>
                  <button v-if="request.status === 'scheduled'" class="btn btn-sm btn-primary me-2"
                    @click="updateRequestStatus(request.id, 'mark_reached')">
                    Mark Reached
                  </button>
                </td>
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
                <th>Address</th>
                <th>Status</th>
                <th>Service Request Date</th>
                <th>Amount (₹)</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in ongoingServices" :key="request.id">
                <td>{{ request.service_name }}</td>
                <td>{{ request.city }}</td>
                <td>{{ request.address }}</td>
                <td><span class="badge bg-primary">{{ request.status }}</span></td>
                <td>{{ request.requested_date }}</td>
                <td>₹{{ request.amount }}</td>
                <td>
                  <button v-if="request.status === 'in_progress'" class="btn btn-sm btn-success me-2"
                    @click="openStartServiceModal(request)">
                    Start Service
                  </button>
                  <button v-if="request.status === 'started'" class="btn btn-sm btn-success"
                    @click="updateRequestStatus(request.id, 'complete')">
                    Complete Service
                  </button>
                </td>
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
                <th>Address</th>
                <th>Status</th>
                <th>Service Request Date</th>
                <th>Date of Service</th>
                <th>Amount (₹)</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in completedServices" :key="request.id">
                <td>{{ request.service_name }}</td>
                <td>{{ request.city }}</td>
                <td>{{ request.address }}</td>
                <td><span class="badge bg-success">{{ request.status }}</span></td>
                <td>{{ request.requested_date }}</td>
                <td>{{ request.date_of_completion || 'N/A' }}</td>
                <td>₹{{ request.amount }}</td>
                <td>
                  <button v-if="request.status === 'completed'" class="btn btn-sm btn-primary"
                    @click="openTransactionModal(request)">
                    Complete Transaction
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div v-if="!hasAnyRequests" class="text-center text-muted mt-4">
        No service requests found.
      </div>
    </div>
    <div v-if="activeTab === 'services'" class="mt-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>Available Services</h2>
        <div class="search-box">
          <input type="text" v-model="searchQuery" @input="searchServices" class="form-control"
            placeholder="Search services...">
        </div>
      </div>
      <div class="row">
        <div v-for="service in services" :key="service.id" class="col-md-4 mb-4">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">{{ service.name }}</h5>
              <p class="card-text">{{ service.description }}</p>
              <p><strong>Base Price:</strong> ₹{{ service.base_price }}</p>
              <p><strong>Time Required:</strong> {{ service.time_required }} mins</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-if="activeTab === 'serviceRequests'" class="mt-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>Service Addition Requests</h2>
        <button class="btn btn-primary" @click="openServiceRequestModal">Add New Service Request</button>
      </div>
      <div class="table-responsive">
        <table class="table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Description</th>
              <th>Base Price</th>
              <th>Time Required</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in serviceRequests" :key="request.id">
              <td>{{ request.name }}</td>
              <td>{{ request.description }}</td>
              <td>₹{{ request.base_price }}</td>
              <td>{{ request.time_required }} mins</td>
              <td><span :class="getStatusBadgeClass(request.status)">{{ request.status }}</span></td>
              <td>
                <button v-if="request.status === 'pending'" class="btn btn-sm btn-primary me-2"
                  @click="openEditServiceRequestModal(request)">
                  Edit
                </button>
                <button v-if="request.status === 'pending'" class="btn btn-sm btn-danger"
                  @click="deleteServiceRequest(request.id)">
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div v-if="activeTab === 'profile'" class="mt-4">
      <h2>Professional Profile</h2>
      <form @submit.prevent="updateProfile">
        <div class="mb-3">
          <label class="form-label">Name</label>
          <input type="text" v-model="profileForm.name" class="form-control" required>
        </div>
        <div class="mb-3">
          <label class="form-label">Phone</label>
          <input type="tel" v-model="profileForm.phone" class="form-control" required>
        </div>
        <div class="mb-3">
          <label class="form-label">Service Type</label>
          <input type="text" v-model="profileForm.service_type" class="form-control" required>
        </div>
        <div class="mb-3">
          <label class="form-label">Experience (years)</label>
          <input type="number" v-model="profileForm.experience" class="form-control" required>
        </div>
        <div class="mb-3">
          <label class="form-label">City</label>
          <select class="form-select" v-model="profileForm.city_id" required>
            <option v-for="city in cities" :key="city.id" :value="city.id">{{ city.name }}</option>
          </select>
        </div>
        <div class="d-flex justify-content-between">
          <button type="submit" class="btn btn-primary">Update Profile</button>
          <button type="button" class="btn btn-danger" @click="deleteProfile">Delete Profile</button>
        </div>
      </form>
    </div>
    <div v-if="showProfileModal" class="modal-wrapper">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Professional Profile</h5>
            <button type="button" class="btn-close" @click="closeProfileModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="updateProfile">
              <div class="mb-3">
                <label class="form-label">Name</label>
                <input type="text" v-model="profileForm.name" class="form-control" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Phone</label>
                <input type="tel" v-model="profileForm.phone" class="form-control" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Service Type</label>
                <input type="text" v-model="profileForm.service_type" class="form-control" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Experience (years)</label>
                <input type="number" v-model="profileForm.experience" class="form-control" required>
              </div>
              <div class="mb-3">
                <label class="form-label">City</label>
                <select class="form-select" v-model="profileForm.city_id" required>
                  <option v-for="city in cities" :key="city.id" :value="city.id">{{ city.name }}</option>
                </select>
              </div>
              <div class="d-flex justify-content-between">
                <button type="submit" class="btn btn-primary">Update Profile</button>
                <button type="button" class="btn btn-danger" @click="deleteProfile">Delete Profile</button>
              </div>
            </form>
          </div>
        </div>
      </div>
      <div class="modal-backdrop" @click="closeProfileModal"></div>
    </div>
    <div v-if="showStartServiceModal" class="modal-wrapper">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Start Service</h5>
            <button type="button" class="btn-close" @click="closeStartServiceModal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Enter PIN</label>
              <input type="number" v-model="startServiceForm.pin" class="form-control" placeholder="Enter 4-digit PIN"
                min="1000" max="9999" />
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeStartServiceModal">Cancel</button>
            <button type="button" class="btn btn-primary" @click="startService">Start Service</button>
          </div>
        </div>
      </div>
      <div class="modal-backdrop" @click="closeStartServiceModal"></div>
    </div>
    <div v-if="showTransactionModal" class="modal-wrapper">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Complete Transaction</h5>
            <button type="button" class="btn-close" @click="closeTransactionModal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Payment Method</label>
              <select v-model="transactionForm.method" class="form-select">
                <option value="cash">Cash</option>
                <option value="upi">UPI</option>
                <option value="card">Card</option>
              </select>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeTransactionModal">Cancel</button>
            <button type="button" class="btn btn-primary" @click="completeTransaction">Complete Transaction</button>
          </div>
        </div>
      </div>
      <div class="modal-backdrop" @click="closeTransactionModal"></div>
    </div>
    <div v-if="showServiceRequestModal" class="modal-wrapper">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ serviceRequestForm.id ? 'Edit' : 'Add' }} Service Request</h5>
            <button type="button" class="btn-close" @click="closeServiceRequestModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitServiceRequest">
              <div class="mb-3">
                <label class="form-label">Service Name</label>
                <input type="text" v-model="serviceRequestForm.name" class="form-control" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea v-model="serviceRequestForm.description" class="form-control" rows="3" required></textarea>
              </div>
              <div class="mb-3">
                <label class="form-label">Base Price (₹)</label>
                <input type="number" v-model="serviceRequestForm.base_price" class="form-control" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Time Required (minutes)</label>
                <input type="number" v-model="serviceRequestForm.time_required" class="form-control" required>
              </div>
              <div class="text-end">
                <button type="button" class="btn btn-secondary me-2" @click="closeServiceRequestModal">Cancel</button>
                <button type="submit" class="btn btn-primary">{{ serviceRequestForm.id ? 'Update' : 'Submit' }}</button>
              </div>
            </form>
          </div>
        </div>
      </div>
      <div class="modal-backdrop" @click="closeServiceRequestModal"></div>
    </div>
  </div>
</template>
<script>
import api from "@/services/api";
export default {
  name: "ProfessionalDashboard",
  data() {
    return {
      activeTab: "home",
      searchQuery: "",
      services: [],
      serviceRequests: [],
      scheduledToday: [],
      ongoingServices: [],
      completedServices: [],
      requestedServices: [],
      acceptedServices: [],
      rejectedServices: [],
      showProfileModal: false,
      showStartServiceModal: false,
      showTransactionModal: false,
      showServiceRequestModal: false,
      selectedRequest: null,
      profileForm: {
        name: "",
        phone: "",
        service_type: "",
        experience: 0,
        city_id: null
      },
      startServiceForm: {
        request_id: null,
        pin: null
      },
      transactionForm: {
        request_id: null,
        method: "cash"
      },
      serviceRequestForm: {
        id: null,
        name: "",
        description: "",
        base_price: 0,
        time_required: 0
      },
      cities: []
    };
  },
  computed: {
    hasAnyRequests() {
      return (
        this.scheduledToday.length > 0 ||
        this.ongoingServices.length > 0 ||
        this.completedServices.length > 0 ||
        this.requestedServices.length > 0 ||
        this.acceptedServices.length > 0 ||
        this.rejectedServices.length > 0
      );
    }
  },
  mounted() {
    this.fetchProfile();
    this.fetchRequests();
    this.fetchServices();
    this.fetchServiceRequests();
    this.fetchCities();
  },
  methods: {
    getStatusBadgeClass(status) {
      const classes = {
        pending: "badge bg-warning",
        approved: "badge bg-success",
        rejected: "badge bg-danger"
      };
      return classes[status] || "badge bg-secondary";
    },
    async fetchProfile() {
      try {
        const response = await api.get("/professionalprofile");
        this.profileForm = response.data;
      } catch (error) {
        console.error("❌ Failed to fetch profile:", error);
      }
    },
    async fetchRequests() {
      try {
        const response = await api.get("/service-requests");
        const data = response.data;
        console.log("Fetched service requests:", data);
        this.scheduledToday = data.scheduled_today || [];
        this.ongoingServices = data.ongoing_services || [];
        this.completedServices = data.completed_services || [];
        this.requestedServices = data.requested_services || [];
        this.acceptedServices = data.accepted_services || [];
        this.rejectedServices = data.rejected_services || [];
      } catch (error) {
        console.error("❌ Failed to fetch service requests:", error);
      }
    },
    async fetchServices() {
      try {
        const response = await api.get("/services");
        this.services = response.data.services;
      } catch (error) {
        console.error("❌ Failed to fetch services:", error);
      }
    },
    async fetchServiceRequests() {
      try {
        const response = await api.get("/manageservices");
        this.serviceRequests = response.data.requests;
      } catch (error) {
        console.error("❌ Failed to fetch service requests:", error);
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
    async updateProfile() {
      try {
        const token = localStorage.getItem("jwt");
        if (!token) {
          alert("You need to login first!");
          this.$router.push("/login");
          return;
        }
        await api.put("/professionalprofile", this.profileForm, {
          headers: { Authorization: `Bearer ${token}` }
        });
        alert("Profile updated successfully!");
        this.closeProfileModal();
      } catch (error) {
        console.error("❌ Failed to update profile:", error);
        alert(error.response?.data?.message || "Failed to update profile");
      }
    },
    async deleteProfile() {
      if (!confirm("Are you sure you want to delete your profile? This action cannot be undone.")) {
        return;
      }
      try {
        const token = localStorage.getItem("jwt");
        if (!token) {
          alert("You need to login first!");
          this.$router.push("/login");
          return;
        }
        await api.delete("/professionalprofile", {
          headers: { Authorization: `Bearer ${token}` }
        });
        alert("Profile deleted successfully!");
        this.$router.push("/login");
      } catch (error) {
        console.error("❌ Failed to delete profile:", error);
        alert(error.response?.data?.message || "Failed to delete profile");
      }
    },
    async updateRequestStatus(requestId, action) {
      try {
        const token = localStorage.getItem("jwt");
        if (!token) {
          alert("You need to login first!");
          this.$router.push("/login");
          return;
        }
        await api.patch(`/service-requests/${requestId}`, { action }, {
          headers: { Authorization: `Bearer ${token}` }
        });
        alert(`Service request ${action}ed successfully!`);
        this.fetchRequests();
      } catch (error) {
        console.error("❌ Failed to update service request:", error);
        alert(error.response?.data?.message || "Failed to update service request");
      }
    },
    openStartServiceModal(request) {
      this.startServiceForm.request_id = request.id;
      this.showStartServiceModal = true;
    },
    async startService() {
      try {
        const token = localStorage.getItem("jwt");
        if (!token) {
          alert("You need to login first!");
          this.$router.push("/login");
          return;
        }
        const { request_id, pin } = this.startServiceForm;
        await api.patch(`/service-requests/${request_id}`, { action: 'start', pin }, {
          headers: { Authorization: `Bearer ${token}` }
        });
        alert("Service started successfully!");
        this.fetchRequests();
        this.closeStartServiceModal();
      } catch (error) {
        console.error("❌ Failed to start service:", error);
        alert(error.response?.data?.message || "Failed to start service");
      }
    },
    openTransactionModal(request) {
      this.transactionForm.request_id = request.id;
      this.showTransactionModal = true;
    },
    async completeTransaction() {
      try {
        const token = localStorage.getItem("jwt");
        if (!token) {
          alert("You need to login first!");
          this.$router.push("/login");
          return;
        }
        const { request_id, method } = this.transactionForm;
        await api.patch(`/service-requests/${request_id}`, { action: 'transaction_complete', method }, {
          headers: { Authorization: `Bearer ${token}` }
        });
        alert("Transaction completed successfully!");
        this.fetchRequests();
        this.closeTransactionModal();
      } catch (error) {
        console.error("❌ Failed to complete transaction:", error);
        alert(error.response?.data?.message || "Failed to complete transaction");
      }
    },
    async submitServiceRequest() {
      try {
        const token = localStorage.getItem("jwt");
        if (!token) {
          alert("You need to login first!");
          this.$router.push("/login");
          return;
        }
        if (this.serviceRequestForm.id) {
          await api.put(`/manageservices/${this.serviceRequestForm.id}`,
            this.serviceRequestForm,
            { headers: { Authorization: `Bearer ${token}` } }
          );
        } else {
          await api.post("/manageservices",
            this.serviceRequestForm,
            { headers: { Authorization: `Bearer ${token}` } }
          );
        }
        alert(this.serviceRequestForm.id ? "Service request updated!" : "Service request submitted!");
        await this.fetchServiceRequests();
        this.closeServiceRequestModal();
      } catch (error) {
        console.error("❌ Failed to submit service request:", error);
        alert(error.response?.data?.message || "Failed to submit service request");
      }
    },
    async deleteServiceRequest(requestId) {
      if (!confirm("Are you sure you want to delete this service request?")) {
        return;
      }
      try {
        const token = localStorage.getItem("jwt");
        if (!token) {
          alert("You need to login first!");
          this.$router.push("/login");
          return;
        }
        await api.delete(`/manageservices/${requestId}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        alert("Service request deleted successfully!");
        await this.fetchServiceRequests();
      } catch (error) {
        console.error("❌ Failed to delete service request:", error);
        alert(error.response?.data?.message || "Failed to delete service request");
      }
    },
    openProfileModal() {
      this.showProfileModal = true;
    },
    closeProfileModal() {
      this.showProfileModal = false;
    },
    closeStartServiceModal() {
      this.showStartServiceModal = false;
      this.startServiceForm = {
        request_id: null,
        pin: null
      };
    },
    closeTransactionModal() {
      this.showTransactionModal = false;
      this.transactionForm = {
        request_id: null,
        method: "cash"
      };
    },
    openServiceRequestModal() {
      this.serviceRequestForm = {
        id: null,
        name: "",
        description: "",
        base_price: 0,
        time_required: 0
      };
      this.showServiceRequestModal = true;
    },
    openEditServiceRequestModal(request) {
      this.serviceRequestForm = { ...request };
      this.showServiceRequestModal = true;
    },
    closeServiceRequestModal() {
      this.showServiceRequestModal = false;
      this.serviceRequestForm = {
        id: null,
        name: "",
        description: "",
        base_price: 0,
        time_required: 0
      };
    },
    searchServices() {
      this.services = this.services.filter(service =>
        service.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        service.description.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
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

.table-responsive {
  margin-bottom: 1rem;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.table {
  margin-bottom: 0;
}

.card {
  transition: transform 0.2s;
  height: 100%;
}

.card:hover {
  transform: translateY(-5px);
}

.search-box {
  max-width: 300px;
}

@media (prefers-color-scheme: light) {
  .modal-content {
    background: white;
    color: #213547;
  }
}

@media (prefers-color-scheme: dark) {
  .modal-content {
    background: #1a1a1a;
    color: rgba(255, 255, 255, 0.87);
  }
}
</style>
