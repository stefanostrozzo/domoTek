<template>
  <q-layout view="lHh Lpr lFf" class="bg-dark">
    <q-header elevated class="bg-dark text-white">
      <q-toolbar>
        <q-toolbar-title>
          DomoTek
        </q-toolbar-title>

        <q-space />

        <q-btn flat round dense icon="notifications" class="q-mr-sm">
          <q-badge color="negative" floating>2</q-badge>
        </q-btn>

        <q-btn flat round dense>
          <q-avatar size="32px">
            <q-img :src="userAvatar" />
          </q-avatar>
          <q-menu class="bg-dark text-white">
            <q-list style="min-width: 150px">
              <q-item clickable v-close-popup @click="goToProfile">
                <q-item-section avatar>
                  <q-icon name="person" color="primary" />
                </q-item-section>
                <q-item-section>Profilo</q-item-section>
              </q-item>

              <q-item clickable v-close-popup @click="goToSettings">
                <q-item-section avatar>
                  <q-icon name="settings" color="primary" />
                </q-item-section>
                <q-item-section>Impostazioni</q-item-section>
              </q-item>

              <q-separator color="grey-8" />

              <q-item clickable v-close-popup @click="logout">
                <q-item-section avatar>
                  <q-icon name="logout" color="primary" />
                </q-item-section>
                <q-item-section>Logout</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>
      </q-toolbar>

      <!-- Navigation Tabs -->
      <q-tabs
        v-model="activeTab"
        class="bg-dark text-white"
        active-color="primary"
        indicator-color="primary"
        align="left"
      >
        <q-route-tab to="/" name="home" icon="home" label="Home" />
        <q-route-tab to="/dashboard" name="dashboard" icon="dashboard" label="Dashboard" />
        <q-route-tab to="/devices" name="devices" icon="devices" label="Dispositivi" />
        <q-route-tab to="/flows" name="flows" icon="hub" label="Flussi" />
        <q-route-tab to="/automations" name="automations" icon="auto_awesome" label="Automazioni" />
      </q-tabs>
    </q-header>

    <q-page-container class="bg-dark">
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAuthStore } from 'src/stores/auth'

export default {
  name: 'MainLayout',
  setup() {
    const router = useRouter()
    const $q = useQuasar()
    const authStore = useAuthStore()
    const userAvatar = ref('https://cdn.quasar.dev/img/avatar.png')
    const activeTab = ref('home')

    const goToProfile = () => {
      router.push('/profile')
    }

    const goToSettings = () => {
      router.push('/settings')
    }

    const logout = async () => {
      try {
        await authStore.logout()
        router.push('/login')
      } catch (error) {
        $q.notify({
          color: 'negative',
          message: 'Errore durante il logout',
          position: 'top'
        })
      }
    }

    return {
      userAvatar,
      activeTab,
      goToProfile,
      goToSettings,
      logout
    }
  }
}
</script>

<style lang="scss">
.bg-dark {
  background: #1E1E2E !important;
}

.text-primary {
  color: #2196F3 !important;
}

.text-secondary {
  color: #00BCD4 !important;
}

.text-accent {
  color: #4CAF50 !important;
}

.q-tabs {
  .q-tab {
    &--active {
      color: #2196F3;
    }
    
    &:hover {
      background: rgba(33, 150, 243, 0.1);
    }
  }
}

.q-menu {
  background: #1E1E2E !important;
  border: 1px solid #2D2D44;
}

.q-item {
  &.q-router-link-active {
    color: #2196F3;
    background: rgba(33, 150, 243, 0.1);
  }
  
  &:hover {
    background: rgba(33, 150, 243, 0.05);
  }
}
</style>
