<script setup>
import { decodeCredential } from 'vue3-google-login'
// --- NEW: Import the shared store ---
import { userState } from './store.js';

// Imports for your existing components
import ProfileSettings from './components/ProfileSettings.vue';
import ChefChat from './components/ChefChat.vue';

// --- LOGIN HANDLERS ---
const handleLoginSuccess = (response) => {
  // The raw Google JWT token
  const { credential } = response;
  console.log("Google Login Success!");

  try {
    // 1. Decode temporarily just to get the email for display
    const userData = decodeCredential(credential);
    
    // 2. Save everything to our shared store
    userState.email = userData.email;
    // CRITICAL: Save the raw token so other components can use it for API calls
    userState.token = credential;
    userState.isLoggedIn = true;

  } catch (error) {
    console.error("Failed to decode Google token", error);
  }
};

const handleLoginError = () => {
    console.error("Google Login Failed");
    alert("Login failed. Please try again.");
};

// Your existing handler for component communication
const handleProfileSaved = () => {
  // We can add logic here later if needed
  console.log("Profile saved successfully");
};
</script>

<template>
  <div class="h-screen bg-gray-100 font-sans">

    <header v-if="userState.isLoggedIn" class="bg-white border-b border-gray-200 px-6 py-3 flex justify-between items-center">
       <h1 class="text-xl font-bold text-gray-800">Training Chef</h1>
       <span class="text-sm text-gray-600">Logged in as: {{ userState.email }}</span>
    </header>

    <div v-if="!userState.isLoggedIn" class="flex h-full items-center justify-center">
        <div class="bg-white p-10 rounded-xl shadow-md text-center">
            <h2 class="text-2xl font-bold mb-4 text-gray-800">Welcome to Training Chef</h2>
            <p class="text-gray-600 mb-8">Please sign in to access your tools.</p>
            <div class="flex justify-center">
                 <GoogleLogin :callback="handleLoginSuccess" :error="handleLoginError"/>
            </div>
        </div>
    </div>

    <div v-else class="flex h-[calc(100vh-60px)]">
      <div class="w-1/3 p-6 border-r border-gray-200 bg-white">
        <ProfileSettings @profileSaved="handleProfileSaved" />
      </div>
      <div class="w-2/3 p-6 bg-gray-50">
        <ChefChat />
      </div>
    </div>

  </div>
</template>