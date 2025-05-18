<template>
  <q-page class="q-pa-md bg-dark">
    <div class="row q-col-gutter-md">
      <!-- Statistiche Generali -->
      <div class="col-12 col-md-3">
        <q-card class="bg-dark-card text-white">
          <q-card-section>
            <div class="text-h6">Dispositivi Attivi</div>
            <div class="text-h4 text-primary">{{ activeDevices }}</div>
            <div class="text-caption text-grey-7">Su {{ totalDevices }} totali</div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-md-3">
        <q-card class="bg-dark-card text-white">
          <q-card-section>
            <div class="text-h6">Flussi Attivi</div>
            <div class="text-h4 text-secondary">{{ activeFlows }}</div>
            <div class="text-caption text-grey-7">Su {{ totalFlows }} totali</div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-md-3">
        <q-card class="bg-dark-card text-white">
          <q-card-section>
            <div class="text-h6">Automazioni</div>
            <div class="text-h4 text-accent">{{ activeAutomations }}</div>
            <div class="text-caption text-grey-7">Attive</div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-md-3">
        <q-card class="bg-dark-card text-white">
          <q-card-section>
            <div class="text-h6">Uptime Sistema</div>
            <div class="text-h4 text-primary">{{ systemUptime }}</div>
            <div class="text-caption text-grey-7">Ultimo riavvio: {{ lastRestart }}</div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Grafico Consumi -->
      <div class="col-12 col-md-8">
        <q-card class="bg-dark-card text-white">
          <q-card-section>
            <div class="text-h6">Consumi Energetici</div>
            <div class="chart-container">
              <!-- Qui andrà il grafico dei consumi -->
              <div class="text-center q-pa-lg text-grey-7">
                Grafico dei consumi energetici
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Dispositivi Recenti -->
      <div class="col-12 col-md-4">
        <q-card class="bg-dark-card text-white">
          <q-card-section>
            <div class="text-h6">Dispositivi Recenti</div>
            <q-list separator>
              <q-item v-for="device in recentDevices" :key="device.id" class="text-white">
                <q-item-section avatar>
                  <q-icon :name="device.icon" :color="device.status === 'online' ? 'positive' : 'negative'" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>{{ device.name }}</q-item-label>
                  <q-item-label caption class="text-grey-7">{{ device.lastSeen }}</q-item-label>
                </q-item-section>
                <q-item-section side>
                  <q-badge :color="device.status === 'online' ? 'positive' : 'negative'">
                    {{ device.status }}
                  </q-badge>
                </q-item-section>
              </q-item>
            </q-list>
          </q-card-section>
        </q-card>
      </div>

      <!-- Log Attività -->
      <div class="col-12">
        <q-card class="bg-dark-card text-white">
          <q-card-section>
            <div class="text-h6">Log Attività</div>
            <q-list separator>
              <q-item v-for="log in activityLogs" :key="log.id" class="text-white">
                <q-item-section avatar>
                  <q-icon :name="log.icon" :color="log.type" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>{{ log.message }}</q-item-label>
                  <q-item-label caption class="text-grey-7">{{ log.timestamp }}</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'DashboardPage',
  setup() {
    // Dati di esempio
    const activeDevices = ref(12)
    const totalDevices = ref(15)
    const activeFlows = ref(8)
    const totalFlows = ref(10)
    const activeAutomations = ref(5)
    const systemUptime = ref('15 giorni')
    const lastRestart = ref('01/03/2024')

    const recentDevices = ref([
      { id: 1, name: 'Termostato', status: 'online', icon: 'thermostat', lastSeen: '2 min fa' },
      { id: 2, name: 'Luci Soggiorno', status: 'offline', icon: 'lightbulb', lastSeen: '5 min fa' },
      { id: 3, name: 'Sensore Porta', status: 'online', icon: 'door_front', lastSeen: '1 min fa' }
    ])

    const activityLogs = ref([
      { id: 1, message: 'Nuovo dispositivo rilevato: Termostato', type: 'primary', icon: 'add_circle', timestamp: '10:30' },
      { id: 2, message: 'Flusso "Temperatura -> Luci" attivato', type: 'secondary', icon: 'hub', timestamp: '10:28' },
      { id: 3, message: 'Automazione "Luci Serali" completata', type: 'accent', icon: 'auto_awesome', timestamp: '10:25' },
      { id: 4, message: 'Disconnessione rilevata: Luci Soggiorno', type: 'negative', icon: 'warning', timestamp: '10:20' }
    ])

    return {
      activeDevices,
      totalDevices,
      activeFlows,
      totalFlows,
      activeAutomations,
      systemUptime,
      lastRestart,
      recentDevices,
      activityLogs
    }
  }
}
</script>

<style lang="scss" scoped>
.bg-dark {
  background: #1E1E2E !important;
}

.bg-dark-card {
  background: #2D2D44 !important;
  border: 1px solid #3D3D54;
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

.chart-container {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}

.q-item {
  &:hover {
    background: rgba(33, 150, 243, 0.05);
  }
}
</style> 