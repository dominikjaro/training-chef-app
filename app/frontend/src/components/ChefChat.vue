<script setup>
import { ref, onMounted } from 'vue';

const messages = ref([]);
const newMessage = ref('');
const loading = ref(true);
const profileExists = ref(false);

// 1. On load, check if user has a profile
async function checkProfile() {
  try {
    const res = await fetch('/api/profile');
    const data = await res.json();
    
    // Your backend sends { message: "No profile..." } if empty
    // OR { weight: 78, ... } if it exists.
    if (data.weight || data.currentWeight) {
        profileExists.value = true;
        // Add a welcome message
        messages.value.push({ sender: 'ai', text: 'Hello! I am your Training Chef. How can I help you today?' });
    } else {
        profileExists.value = false;
    }
  } catch (e) {
    console.error("Connection error:", e);
  } finally {
    loading.value = false;
  }
}

// 2. Function to send message to AI
async function sendMessage() {
  if (!newMessage.value.trim()) return;

  // Add user message to UI immediately
  messages.value.push({ sender: 'user', text: newMessage.value });
  const textToSend = newMessage.value;
  newMessage.value = '';

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      // Note: Backend expects query param ?message=... in your current code
      // simpler to change fetch url:
      // BUT simpler is to change backend to accept body. 
      // Let's use the Query param method for now as per your backend code:
    });
    
    // WAIT! Your current backend uses: @app.post("/api/chat") def chat_with_ai(message: str)
    // In FastAPI, if you don't define a Pydantic model, it expects a Query Parameter.
    // Let's call it correctly:
    const response = await fetch(`/api/chat?message=${encodeURIComponent(textToSend)}`, {
        method: 'POST'
    });
    
    const data = await response.json();
    messages.value.push({ sender: 'ai', text: data.response });

  } catch (e) {
    messages.value.push({ sender: 'ai', text: "Sorry, I'm having trouble connecting to the kitchen." });
  }
}

// Check profile when component mounts
onMounted(() => {
    checkProfile();
});

// Allow parent to trigger a re-check (when profile is saved)
defineExpose({ checkProfile });
</script>

<template>
  <div class="flex flex-col h-full bg-white rounded-lg shadow-md p-4">
    <h2 class="text-2xl font-bold mb-4 text-gray-800">Talk to your Training Chef</h2>

    <div v-if="loading" class="flex-grow flex items-center justify-center bg-gray-100 rounded">
      <p class="text-gray-500">Checking profile...</p>
    </div>

    <div v-else-if="!profileExists" class="flex-grow flex items-center justify-center bg-gray-100 rounded">
      <p class="text-gray-600">Please save your profile on the left to start chatting.</p>
    </div>

    <div v-else class="flex flex-col flex-grow h-0">
      <div class="flex-grow overflow-y-auto mb-4 space-y-2 p-2 bg-gray-50 rounded border">
        <div 
            v-for="(msg, index) in messages" 
            :key="index"
            :class="['p-2 rounded max-w-[80%]', msg.sender === 'user' ? 'bg-blue-100 self-end ml-auto' : 'bg-gray-200 self-start']"
        >
            <strong>{{ msg.sender === 'user' ? 'You' : 'Chef' }}:</strong> {{ msg.text }}
        </div>
      </div>

      <form @submit.prevent="sendMessage" class="flex gap-2">
        <input 
            v-model="newMessage"
            type="text" 
            placeholder="Ask about your diet..." 
            class="flex-grow shadow appearance-none border rounded py-2 px-3 text-gray-700 focus:outline-none"
        />
        <button type="submit" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Send
        </button>
      </form>
    </div>
  </div>
</template>