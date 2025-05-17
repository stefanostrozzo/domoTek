<template>
  <q-page class="flex flex-center">
    <q-card class="register-card">
      <q-card-section>
        <div class="text-h6">Register</div>
      </q-card-section>

      <q-card-section>
        <q-form @submit="onSubmit" class="q-gutter-md">
          <q-input
            v-model="name"
            label="Name"
            :rules="[val => !!val || 'Name is required']"
          />

          <q-input
            v-model="email"
            label="Email"
            type="email"
            :rules="[
              val => !!val || 'Email is required',
              val => /.+@.+\..+/.test(val) || 'Invalid email format'
            ]"
          />

          <q-input
            v-model="password"
            label="Password"
            type="password"
            :rules="[
              val => !!val || 'Password is required',
              val => val.length >= 8 || 'Password must be at least 8 characters'
            ]"
          />

          <q-input
            v-model="password_confirmation"
            label="Confirm Password"
            type="password"
            :rules="[
              val => !!val || 'Please confirm your password',
              val => val === password || 'Passwords do not match'
            ]"
          />

          <div>
            <q-btn label="Register" type="submit" color="primary" class="full-width" />
          </div>

          <div class="text-center q-mt-sm">
            <router-link to="/login" class="text-primary">Already have an account? Login</router-link>
          </div>
        </q-form>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useQuasar } from 'quasar';
import { useAuthStore } from '../stores/auth';

export default {
  name: 'RegisterPage',
  setup() {
    const $q = useQuasar();
    const router = useRouter();
    const authStore = useAuthStore();

    const name = ref('');
    const email = ref('');
    const password = ref('');
    const password_confirmation = ref('');

    const onSubmit = async () => {
      try {
        await authStore.register(
          name.value,
          email.value,
          password.value,
          password_confirmation.value
        );
        $q.notify({
          color: 'positive',
          message: 'Registration successful',
        });
        router.push('/');
      } catch (error) {
        $q.notify({
          color: 'negative',
          message: error.response?.data?.message || 'Registration failed',
        });
      }
    };

    return {
      name,
      email,
      password,
      password_confirmation,
      onSubmit,
    };
  },
};
</script>

<style scoped>
.register-card {
  width: 100%;
  max-width: 400px;
}
</style> 