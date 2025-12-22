<script setup>
import { ref } from 'vue';
import ProfileSettings from './components/ProfileSettings.vue';
import ChefChat from './components/ChefChat.vue';

const chatRef = ref(null);

const handleProfileSaved = () => {
  // When profile is saved, tell the chat component to check again
  if (chatRef.value) {
    chatRef.value.checkProfile();
  }
};
</script>

<template>
  <div class="flex h-screen bg-gray-100 font-sans">
    <div class="w-1/3 p-6 border-r border-gray-200">
      <ProfileSettings @profileSaved="handleProfileSaved" />
    </div>
    <div class="w-2/3 p-6">
      <ChefChat ref="chatRef" />
    </div>
  </div>
</template>