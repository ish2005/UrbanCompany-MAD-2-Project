<template>
  <div class="home-page">
    <!-- Navigation Bar -->
    <nav class="navbar navbar-expand-lg navbar-light bg-white fixed-top shadow-sm">
      <div class="container">
        <router-link class="navbar-brand" to="/">
          <img src="https://cdn-icons-png.flaticon.com/512/1041/1041916.png" alt="UrbanClap" height="40">
        </router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/login">Login</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link btn btn-primary text-white px-3" to="/signup">Sign Up</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <div class="hero-section">
      <div class="hero-content">
        <h1>Welcome to UrbanClap</h1>
        <p>Your one-stop solution for all home services</p>
        <div class="auth-buttons">
          <router-link to="/login" class="btn btn-primary btn-lg me-3">Login</router-link>
          <router-link to="/signup" class="btn btn-outline-light btn-lg">Sign Up</router-link>
        </div>
      </div>
    </div>

    <!-- Services Section -->
    <div class="services-section py-5">
      <div class="container">
        <h2 class="text-center mb-5">Our Services</h2>
        <div class="row g-4">
          <div v-for="service in services" :key="service.id" class="col-md-4">
            <div class="service-card">
              <div class="service-icon">
                <i :class="getServiceIcon(service.name)"></i>
              </div>
              <h3>{{ service.name }}</h3>
              <p>{{ service.description }}</p>
              <div class="service-details">
                <span class="price">₹{{ service.base_price }}</span>
                <span class="time">{{ service.time_required }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Cities Section -->
    <div class="cities-section py-5 bg-light">
      <div class="container">
        <h2 class="text-center mb-5">Available Cities</h2>
        <div class="row g-4">
          <div v-for="city in cities" :key="city.id" class="col-md-3">
            <div class="city-card">
              <i class="fas fa-city mb-3"></i>
              <h3>{{ city.name }}</h3>
              <p>Pincode: {{ city.pincode }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div class="features-section py-5">
      <div class="container">
        <h2 class="text-center mb-5">Why Choose Us?</h2>
        <div class="row g-4">
          <div class="col-md-4">
            <div class="feature-card">
              <div class="feature-icon">
                <i class="fas fa-check-circle"></i>
              </div>
              <h3>Verified Professionals</h3>
              <p>All our service providers are thoroughly verified and background checked</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="feature-card">
              <div class="feature-icon">
                <i class="fas fa-clock"></i>
              </div>
              <h3>On-Time Service</h3>
              <p>We value your time and ensure punctual service delivery</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="feature-card">
              <div class="feature-icon">
                <i class="fas fa-shield-alt"></i>
              </div>
              <h3>Secure Payments</h3>
              <p>Multiple payment options with secure transaction processing</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="footer py-4 bg-dark text-white">
      <div class="container">
        <div class="row">
          <div class="col-md-4">
            <h5>About Us</h5>
            <p>UrbanClap is your trusted partner for all home services. We connect you with verified professionals.</p>
          </div>
          <div class="col-md-4">
            <h5>Quick Links</h5>
            <ul class="list-unstyled">
              <li><router-link to="/" class="text-white">Home</router-link></li>
              <li><router-link to="/services" class="text-white">Services</router-link></li>
              <li><router-link to="/cities" class="text-white">Cities</router-link></li>
            </ul>
          </div>
          <div class="col-md-4">
            <h5>Contact Us</h5>
            <ul class="list-unstyled">
              <li><i class="fas fa-phone"></i> +91 1234567890</li>
              <li><i class="fas fa-envelope"></i> support@urbanclap.com</li>
              <li><i class="fas fa-map-marker-alt"></i> 123, Service Street, City</li>
            </ul>
          </div>
        </div>
        <hr class="my-4">
        <div class="text-center">
          <p class="mb-0">&copy; 2024 UrbanClap. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import api from '@/services/api';

export default {
  name: "HomePage",
  data() {
    return {
      services: [],
      cities: [],
      loading: true,
      error: null
    };
  },
  methods: {
    getServiceIcon(serviceName) {
      const icons = {
        'Plumbing': 'fas fa-wrench',
        'Electrical': 'fas fa-bolt',
        'Cleaning': 'fas fa-broom',
        'Carpenter': 'fas fa-hammer',
        'Painter': 'fas fa-paint-roller',
        'Appliance Repair': 'fas fa-tools',
        'Pest Control': 'fas fa-bug-slash',
        'Car Wash': 'fas fa-car',
        'Moving': 'fas fa-truck',
        'Default': 'fas fa-tools'
      };
      return icons[serviceName] || icons.Default;
    }
  },
  async created() {
    try {
      const servicesResponse = await api.get('/services');
      this.services = servicesResponse.data.services;

      const citiesResponse = await api.get('/cities');
      this.cities = citiesResponse.data.cities;
    } catch (error) {
      console.error('Error fetching data:', error);
      this.error = 'Failed to load data';
    } finally {
      this.loading = false;
    }
  }
};
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  padding-top: 76px; /* Account for fixed navbar */
}

.navbar {
  z-index: 1000;
}

.navbar-brand img {
  transition: transform 0.3s ease;
}

.navbar-brand img:hover {
  transform: scale(1.1);
}

.hero-section {
  background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)),
              url('https://images.unsplash.com/photo-1556911220-bff31c812dba?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  height: 90vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: white;
  margin-top: -76px;
}

.hero-content {
  max-width: 800px;
  padding: 0 20px;
}

.hero-content h1 {
  font-size: 4rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.hero-content p {
  font-size: 1.8rem;
  margin-bottom: 2.5rem;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.auth-buttons .btn {
  padding: 1rem 2.5rem;
  font-size: 1.2rem;
  border-radius: 50px;
  transition: all 0.3s ease;
}

.auth-buttons .btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.service-card {
  background: white;
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  height: 100%;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.service-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
}

.service-icon {
  font-size: 3rem;
  color: #007bff;
  margin-bottom: 1.5rem;
  transition: transform 0.3s ease;
}

.service-card:hover .service-icon {
  transform: scale(1.1);
}

.service-details {
  display: flex;
  justify-content: space-between;
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
  color: #666;
  font-weight: 500;
}

.city-card {
  background: white;
  border-radius: 15px;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.city-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
}

.city-card i {
  font-size: 2.5rem;
  color: #007bff;
  margin-bottom: 1rem;
}

.feature-card {
  text-align: center;
  padding: 2.5rem;
  background: white;
  border-radius: 15px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  height: 100%;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
}

.feature-icon {
  width: 80px;
  height: 80px;
  background: #f8f9fa;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
}

.feature-icon i {
  font-size: 2rem;
  color: #007bff;
}

.footer {
  background: #1a1a1a;
}

.footer h5 {
  color: #fff;
  margin-bottom: 1.5rem;
  font-weight: 600;
}

.footer ul li {
  margin-bottom: 0.8rem;
}

.footer ul li i {
  margin-right: 10px;
  color: #007bff;
}

@media (max-width: 768px) {
  .hero-content h1 {
    font-size: 2.5rem;
  }
  
  .hero-content p {
    font-size: 1.2rem;
  }
  
  .service-card, .city-card, .feature-card {
    margin-bottom: 1.5rem;
  }
}
</style> 