<template>
  <q-page class="flex flex-center">
    <q-card class="login-card">
      <q-card-section>
        <div class="text-h6 text-center">Login</div>
      </q-card-section>

      <q-card-section>
        <q-form @submit="onSubmit" class="q-gutter-md">
          <q-input
            v-model="email"
            label="Email"
            type="email"
            :rules="[val => !!val || 'Email is required',
                    val => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val) || 'Invalid email format']"
          >
            <template v-slot:prepend>
              <q-icon name="mail" />
            </template>
          </q-input>

          <q-input
            v-model="password"
            label="Password"
            :type="isPwd ? 'password' : 'text'"
            :rules="[val => !!val || 'Password is required']"
          >
            <template v-slot:prepend>
              <q-icon name="lock" />
            </template>
            <template v-slot:append>
              <q-icon
                :name="isPwd ? 'visibility_off' : 'visibility'"
                class="cursor-pointer"
                @click="isPwd = !isPwd"
              />
            </template>
          </q-input>

          <div class="row justify-between items-center">
            <q-checkbox v-model="rememberMe" label="Remember me" />
            <q-btn flat color="primary" label="Forgot password?" />
          </div>

          <div>
            <q-btn
              label="Login"
              type="submit"
              color="primary"
              class="full-width"
            />
          </div>

          <div class="text-center q-mt-sm">
            Don't have an account?
            <router-link to="/register" class="text-primary">Register</router-link>
          </div>
        </q-form>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'LoginPage',
  setup () {
    const router = useRouter()
    const email = ref('')
    const password = ref('')
    const isPwd = ref(true)
    const rememberMe = ref(false)

    const onSubmit = async () => {
      try {
        // TODO: Implement login logic here
        console.log('Login attempt with:', {
          email: email.value,
          password: password.value,
          rememberMe: rememberMe.value
        })
        
        // After successful login, redirect to home page
        router.push('/')
      } catch (error) {
        console.error('Login failed:', error)
      }
    }

    return {
      email,
      password,
      isPwd,
      rememberMe,
      onSubmit
    }
  }
}
</script>

<style lang="scss" scoped>
.login-card {
  width: 100%;
  max-width: 400px;
  padding: 1rem;
}
</style> 