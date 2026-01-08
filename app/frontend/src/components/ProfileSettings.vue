<script setup>
import { ref, reactive, onMounted } from 'vue';
// Import the shared store to get the token
import { userState } from '../store.js';

const emit = defineEmits(['profileSaved']);

const loading = ref(true);
const saving = ref(false);
const message = ref({ text: '', type: '' });

const profile = reactive({
  currentWeight: null,
  height: null,
  ftp: null,
  bodyType: 'ectomorph'
});

// --- FETCH DATA ON LOAD ---
onMounted(async () => {
  const token = userState.token;

  if (!token) {
      // Should not happen if App.vue logic is correct
      loading.value = false;
      return;
  }

  try {
    // ATTACH TOKEN TO HEADERS
    const response = await fetch('/api/profile', {
        headers: {
             'Authorization': `Bearer ${token}`,
             'Content-Type': 'application/json'
        }
    });

    if (response.ok) {
      const data = await response.json();
      if (Object.keys(data).length > 0) {
          profile.currentWeight = data.currentWeight;
          profile.height = data.height;
          profile.ftp = data.ftp;
          profile.bodyType = data.bodyType;
      }
    } else if (response.status === 401 || response.status === 403) {
         console.error("Unauthorized access to profile.");
    }
  } catch (error) {
    console.error('Error fetching profile:', error);
  } finally {
    loading.value = false;
  }
});

// --- SAVE DATA ---
const saveProfile = async () => {
  saving.value = true;
  message.value = { text: '', type: '' };

  const token = userState.token;
   if (!token) {
      message.value = { text: 'Authentication error. Please log in again.', type: 'error' };
      saving.value = false;
      return;
  }

  try {
    // ATTACH TOKEN TO HEADERS
    const response = await fetch('/api/profile', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(profile),
    });

    if (response.ok) {
      message.value = { text: 'Profile saved successfully!', type: 'success' };
      emit('profileSaved');
    } else {
       if (response.status === 401) {
           message.value = { text: 'Unauthorized. Your session may have expired.', type: 'error' };
       } else {
           message.value = { text: 'Failed to save profile.', type: 'error' };
       }
    }
  } catch (error) {
    console.error('Error saving profile:', error);
    message.value = { text: 'An error occurred.', type: 'error' };
  } finally {
    saving.value = false;
    if (message.value.type === 'success') {
        setTimeout(() => { message.value.text = ''; }, 3000);
    }
  }
};
</script>

<template>
  <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200 h-full">
    <h2 class="text-xl font-bold text-gray-800 mb-6">My Rider Profile</h2>

    <div v-if="loading" class="text-gray-500">Loading profile...</div>

    <form v-else @submit.prevent="saveProfile">
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="weight">
          Current Weight (kg)
        </label>
        <input
          v-model.number="profile.currentWeight"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          id="weight"
          type="number"
          step="0.1"
          required
        >
      </div>

      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="height">
          Height (cm)
        </label>
        <input
          v-model.number="profile.height"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          id="height"
          type="number"
          required
        >
      </div>

      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="ftp">
          Functional Threshold Power (FTP)
        </label>
        <input
          v-model.number="profile.ftp"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          id="ftp"
          type="number"
          required
        >
      </div>

       <div class="mb-6">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="bodyType">
          Body Type
        </label>
        <select
          v-model="profile.bodyType"
          class="block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline"
          id="bodyType"
        >
          <option value="ectomorph">Hard Gainer (Ectomorph)</option>
          <option value="mesomorph">Athletic (Mesomorph)</option>
          <option value="endomorph">Soft Gainer (Endomorph)</option>
        </select>
      </div>

      <div class="flex items-center justify-between">
        <button
          class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline disabled:opacity-50 transition ease-in-out duration-150"
          type="submit"
          :disabled="saving"
        >
          <span v-if="saving">Saving...</span>
          <span v-else>Save Profile</span>
        </button>
      </div>

      <p v-if="message.text" :class="{'text-green-600': message.type === 'success', 'text-red-600': message.type === 'error'}" class="mt-4 text-sm font-bold">
          {{ message.text }}
      </p>

    </form>
  </div>
</template>