<script setup>
import ProfileSettings from './components/ProfileSettings.vue';
import ChefChat from './components/ChefChat.vue';
</script>

<template>
  <div class="flex h-screen bg-gray-100 font-sans">
    <div class="w-1/3 p-6 border-r border-gray-200">
      <ProfileSettings />
    </div>
    <div class="w-2/3 p-6">
      <ChefChat />
    </div>
  </div>
</template>
