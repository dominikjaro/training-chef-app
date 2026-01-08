import { reactive } from 'vue';

// This is a simple global state object shared across the app
export const userState = reactive({
  isLoggedIn: false,
  email: '',
  // This is the crucial ID badge we need to send to the backend
  token: null 
});

// Helper to clear state on logout
export const clearUserState = () => {
  userState.isLoggedIn = false;
  userState.email = '';
  userState.token = null;
};