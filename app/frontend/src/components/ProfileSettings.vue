<script setup>
import { ref } from 'vue';

const currentWeight = ref(null);
const ftp = ref(null);
const height = ref(null);
const bodyType = ref('Hard Gainer (Ectomorph)');
const statusMessage = ref(''); // To show success/error to user

const bodyTypes = [
  'Hard Gainer (Ectomorph)',
  'Soft Gainer (Endomorph)',
  'Natural Athlete (Mesomorph)',
];

// Define emits so we can tell the parent (App.vue) when we are done
const emit = defineEmits(['profileSaved']);

async function saveProfile() {
  statusMessage.value = 'Saving...';
  
  try {
    // 1. Send data to Backend
    // We use /api/... relative path so it works on your domain automatically
    const response = await fetch('/api/profile', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        // These keys match the "alias" we set in your Python Backend
        currentWeight: currentWeight.value,
        ftp: ftp.value,
        height: height.value,
        bodyType: bodyType.value,
      }),
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const data = await response.json();
    console.log('Success:', data);
    
    statusMessage.value = 'Profile saved successfully!';
    
    // 2. Tell the App to unlock the chat
    emit('profileSaved');

  } catch (error) {
    console.error('Error saving profile:', error);
    statusMessage.value = 'Error saving profile. Check console.';
  }
}
</script>

<template>
  <div class="p-4 bg-white rounded-lg shadow-md">
    <h2 class="text-2xl font-bold mb-6 text-gray-800">Profile Settings</h2>
    <form @submit.prevent="saveProfile">
      <div class="mb-4">
        <label for="currentWeight" class="block text-gray-700 text-sm font-bold mb-2">Current Weight (kg)</label>
        <input id="currentWeight" v-model.number="currentWeight" type="number" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" />
      </div>
      <div class="mb-4">
        <label for="ftp" class="block text-gray-700 text-sm font-bold mb-2">Functional Threshold Power (FTP)</label>
        <input id="ftp" v-model.number="ftp" type="number" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" />
      </div>
      <div class="mb-4">
        <label for="height" class="block text-gray-700 text-sm font-bold mb-2">Height (cm)</label>
        <input id="height" v-model.number="height" type="number" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" />
      </div>
      <div class="mb-6">
        <label for="bodyType" class="block text-gray-700 text-sm font-bold mb-2">Body Type</label>
        <div class="relative">
          <select id="bodyType" v-model="bodyType" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
            <option v-for="option in bodyTypes" :key="option" :value="option">{{ option }}</option>
          </select>
        </div>
      </div>

      <div class="flex items-center justify-between">
        <button type="submit" class="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
          Save Profile
        </button>
      </div>
      <p v-if="statusMessage" class="mt-4 text-center text-sm font-bold" :class="statusMessage.includes('Error') ? 'text-red-500' : 'text-green-600'">
        {{ statusMessage }}
      </p>
    </form>
  </div>
</template>