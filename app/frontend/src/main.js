import { createApp } from 'vue'
import './assets/style.css'
import App from './App.vue'
// --- CHANGE 1: Import the new plugin ---
import vue3GoogleLogin from 'vue3-google-login'

const app = createApp(App)

// --- CHANGE 2: Use the new plugin ---
app.use(vue3GoogleLogin, {
  clientId: '777681998732-e6kccs0paubeq69fp3b82fighdbvtuo6.apps.googleusercontent.com'
})

app.mount('#app')