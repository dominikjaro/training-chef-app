<script setup>
import { ref } from 'vue';
// --- CHANGE: Update import to the new library ---
import { decodeCredential } from 'vue3-google-login'

// Imports for your existing components
import ProfileSettings from './components/ProfileSettings.vue';
import ChefChat from './components/ChefChat.vue';

// --- STATE ---
const isLoggedIn = ref(false);
const userEmail = ref('');
const chatRef = ref(null);

// --- LOGIN HANDLERS ---
const handleLoginSuccess = (response) => {
  // The new library sends the token in a property called 'credential'
  const { credential } = response;
  console.log("Google Login Success! Encoded Token:", credential);

  try {
    const userData = decodeCredential(credential);
    userEmail.value = userData.email;
    isLoggedIn.value = true;
  } catch (error) {
    console.error("Failed to decode Google token", error);
  }
};

const handleLoginError = () => {
    console.error("Google Login Failed");
    alert("Login failed. Please try again.");
};

const handleProfileSaved = () => {
  if (chatRef.value) {
    chatRef.value.checkProfile();
  }
};
</script>

<template>
  <div class="h-screen bg-gray-100 font-sans">

    <header v-if="isLoggedIn" class="bg-white border-b border-gray-200 px-6 py-3 flex justify-between items-center">
       <h1 class="text-xl font-bold text-gray-800">Training Chef</h1>
       <span class="text-sm text-gray-600">Logged in as: {{ userEmail }}</span>
    </header>

    <div v-if="!isLoggedIn" class="flex h-full items-center justify-center">
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
        <ChefChat ref="chatRef" />
      </div>
    </div>

  </div>
</template>