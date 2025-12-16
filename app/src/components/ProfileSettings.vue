<script setup>
import { ref } from 'vue';

const currentWeight = ref(null);
const ftp = ref(null);
const height = ref(null);
const bodyType = ref('Hard Gainer (Ectomorph)');

const bodyTypes = [
  'Hard Gainer (Ectomorph)',
  'Endomorph',
  'Mesomorph',
];

function saveProfile() {
  console.log('Saving profile:', {
    currentWeight: currentWeight.value,
    ftp: ftp.value,
    height: height.value,
    bodyType: bodyType.value,
  });
  // Here you would typically send the data to a server
}
</script>

<template>
  <div class="p-4 bg-white rounded-lg shadow-md">
    <h2 class="text-2xl font-bold mb-6 text-gray-800">Profile Settings</h2>
    <form @submit.prevent="saveProfile">
      <div class="mb-4">
        <label for="currentWeight" class="block text-gray-700 text-sm font-bold mb-2">Current Weight (kg)</label>
        <input
          id="currentWeight"
          v-model.number="currentWeight"
          type="number"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        />
      </div>
      <div class="mb-4">
        <label for="ftp" class="block text-gray-700 text-sm font-bold mb-2">Functional Threshold Power (FTP)</label>
        <input
          id="ftp"
          v-model.number="ftp"
          type="number"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        />
      </div>
      <div class="mb-4">
        <label for="height" class="block text-gray-700 text-sm font-bold mb-2">Height (cm)</label>
        <input
          id="height"
          v-model.number="height"
          type="number"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        />
      </div>
      <div class="mb-6">
        <label for="bodyType" class="block text-gray-700 text-sm font-bold mb-2">Body Type</label>
        <div class="relative">
          <select
            id="bodyType"
            v-model="bodyType"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          >
            <option v-for="option in bodyTypes" :key="option" :value="option">
              {{ option }}
            </option>
          </select>
          <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
            <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
          </div>
        </div>
      </div>
      <button
        type="submit"
        class="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
      >
        Save Profile
      </button>
    </form>
  </div>
</template>
