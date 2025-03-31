<template>
  <router-view />
</template>

<script>
export default {
  name: "App"
};
</script>

<style>
/* Global styles */
body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
  color: #333;
}

/* Add smooth scrolling */
html {
  scroll-behavior: smooth;
}

/* Add some global utility classes */
.text-primary {
  color: #007bff !important;
}

.bg-primary {
  background-color: #007bff !important;
}

/* Add some spacing utilities */
.mt-6 {
  margin-top: 4rem;
}

.mb-6 {
  margin-bottom: 4rem;
}

/* Add some animation utilities */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
  