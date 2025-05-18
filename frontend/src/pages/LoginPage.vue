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
              :loading="loading"
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
import { useQuasar } from 'quasar'
import { useAuthStore } from 'src/stores/auth'

export default {
  name: 'LoginPage',
  setup () {
    const router = useRouter()
    const $q = useQuasar()
    const authStore = useAuthStore()
    const email = ref('')
    const password = ref('')
    const isPwd = ref(true)
    const rememberMe = ref(false)
    const loading = ref(false)

    const onSubmit = async () => {
      try {
        loading.value = true
        await authStore.login({
          email: email.value,
          password: password.value
        })

        $q.notify({
          color: 'positive',
          message: 'Login effettuato con successo',
          position: 'top',
          timeout: 3000
        })

        router.push('/')
      } catch (error) {
        console.error('Login failed:', error)
        if (error.response?.data?.errors) {
          const errors = error.response.data.errors;
          Object.keys(errors).forEach(field => {
            $q.notify({
              color: 'negative',
              message: errors[field][0],
              position: 'top',
              timeout: 5000
            });
          });
        } else {
          $q.notify({
            color: 'negative',
            message: error.response?.data?.message || 'Errore durante il login',
            position: 'top',
            timeout: 5000
          });
        }
      } finally {
        loading.value = false
      }
    }

    return {
      email,
      password,
      isPwd,
      rememberMe,
      loading,
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