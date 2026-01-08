<script setup>
import { ref, reactive, nextTick, onMounted } from 'vue';
// Import store for token
import { userState } from '../store.js';

const userInput = ref('');
const isLoading = ref(false);
const chatContainer = ref(null);
const hasProfile = ref(false);

const chatHistory = reactive([
  { role: 'chef', content: "Bonjour! I am your Cycling Chef. Let's plan your nutrition. What are your goals?" }
]);

const checkProfile = async () => {
    const token = userState.token;
    if (!token) return;

    try {
      // ATTACH TOKEN
      const response = await fetch('/api/profile', {
          headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        hasProfile.value = Object.keys(data).length > 0;
      }
    } catch (error) {
      console.error("Failed to check profile status", error);
    }
};

defineExpose({ checkProfile });

onMounted(() => {
    checkProfile();
});

const scrollToBottom = () => {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
    }
  });
};

const sendMessage = async () => {
  if (userInput.value.trim() === '') return;

  const userMessage = userInput.value;
  chatHistory.push({ role: 'user', content: userMessage });
  userInput.value = '';
  scrollToBottom();
  isLoading.value = true;

  const token = userState.token;
  if (!token) {
       chatHistory.push({ role: 'chef', content: "Pardon, I cannot verify your identity. Please log in again." });
       isLoading.value = false;
       scrollToBottom();
       return;
  }

  try {
    // ATTACH TOKEN
    const response = await fetch('/api/chat?message=' + encodeURIComponent(userMessage), {
        method: 'POST',
        headers: {
             'Authorization': `Bearer ${token}`
        }
    });
    
    if (!response.ok) {
         if (response.status === 401 || response.status === 403) {
             throw new Error("Unauthorized: Please check your login or whitelist status.");
         }
         throw new Error(`HTTP error! status: ${response.status}`);
    }
      
    const data = await response.json();
    chatHistory.push({ role: 'chef', content: data.response });
  } catch (error) {
    console.error('Chat Error:', error);
    chatHistory.push({ role: 'chef', content: "Zut alors! My brain is tired. Let's try again later. (" + error.message + ")" });
  } finally {
    isLoading.value = false;
    scrollToBottom();
  }
};
</script>

<template>
  <div class="flex flex-col h-full bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
    <div class="bg-gray-50 p-4 border-b border-gray-200 flex justify-between items-center">
      <h2 class="text-lg font-bold text-gray-800">Chef's Table</h2>
      <span v-if="hasProfile" class="text-xs text-green-600 font-medium px-2 py-1 bg-green-100 rounded-full">Profile Active</span>
      <span v-else class="text-xs text-orange-600 font-medium px-2 py-1 bg-orange-100 rounded-full">No Profile Found</span>
    </div>

    <div ref="chatContainer" class="flex-1 p-4 overflow-y-auto space-y-4 bg-gray-50">
      <div
        v-for="(message, index) in chatHistory"
        :key="index"
        :class="['flex', message.role === 'user' ? 'justify-end' : 'justify-start']"
      >
        <div
          :class="[
            'max-w-[70%] rounded-lg p-3 shadow-sm',
            message.role === 'user'
              ? 'bg-blue-600 text-white rounded-br-none'
              : 'bg-white border border-gray-200 text-gray-800 rounded-bl-none'
          ]"
        >
          <p class="text-sm">{{ message.content }}</p>
        </div>
      </div>
      
      <div v-if="isLoading" class="flex justify-start">
         <div class="bg-white border border-gray-200 text-gray-500 p-3 rounded-lg rounded-bl-none shadow-sm">
            <div class="flex space-x-2">
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
            </div>
         </div>
      </div>

    </div>

    <div class="p-4 border-t border-gray-200 bg-white">
      <form @submit.prevent="sendMessage" class="flex space-x-2">
        <input
          v-model="userInput"
          type="text"
          placeholder="Ask about nutrition for your next ride..."
          class="flex-1 appearance-none border rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:border-blue-500 focus:shadow-outline transition ease-in-out duration-150"
          :disabled="isLoading"
        >
        <button
          type="submit"
          class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded focus:outline-none focus:shadow-outline disabled:opacity-50 transition ease-in-out duration-150"
          :disabled="isLoading || userInput.trim() === ''"
        >
          Send
        </button>
      </form>
    </div>
  </div>
</template>