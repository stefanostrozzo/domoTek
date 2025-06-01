<template>
  <q-page class="q-pa-md bg-dark">
    <div class="row q-col-gutter-md">
      <!-- Sezione Dispositivi -->
      <div class="col-12 col-md-6">
        <q-card class="device-card bg-dark-card">
          <q-card-section class="bg-primary text-white">
            <div class="text-h6">Dispositivi</div>
          </q-card-section>

          <q-card-section>
            <div class="row q-col-gutter-md">
              <div class="col-12">
                <q-btn
                  color="primary"
                  icon="search"
                  label="Scansiona Rete"
                  class="full-width q-mb-md"
                  @click="scanNetwork"
                  :loading="scanning"
                />
              </div>
              <div class="col-12">
                <q-btn
                  color="primary"
                  icon="add"
                  label="Aggiungi Dispositivo"
                  class="full-width"
                  @click="showAddDeviceDialog = true"
                />
              </div>
            </div>

            <!-- Lista Dispositivi -->
            <div class="q-mt-md">
              <div v-if="devices.length === 0" class="text-center q-pa-md text-grey-7">
                Nessun dispositivo trovato
              </div>
              <q-list v-else bordered separator class="bg-dark-card">
                <q-item v-for="device in devices" :key="device.id" clickable v-ripple class="text-white">
                  <q-item-section avatar>
                    <q-icon :name="device.icon" color="primary" />
                  </q-item-section>
                  <q-item-section>
                    <q-item-label>{{ device.name }}</q-item-label>
                    <q-item-label caption class="text-grey-7">{{ device.type }}</q-item-label>
                  </q-item-section>
                  <q-item-section side>
                    <q-badge :color="device.status === 'online' ? 'positive' : 'negative'">
                      {{ device.status }}
                    </q-badge>
                  </q-item-section>
                </q-item>
              </q-list>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Sezione Flussi -->
      <div class="col-12 col-md-6">
        <q-card class="flow-card bg-dark-card">
          <q-card-section class="bg-secondary text-white">
            <div class="text-h6">Flussi di Dati</div>
          </q-card-section>

          <q-card-section>
            <q-btn
              color="secondary"
              icon="add"
              label="Nuovo Flusso"
              class="full-width q-mb-md"
              @click="showAddFlowDialog = true"
            />

            <!-- Lista Flussi -->
            <div class="q-mt-md">
              <div v-if="flows.length === 0" class="text-center q-pa-md text-grey-7">
                Nessun flusso configurato
              </div>
              <q-list v-else bordered separator class="bg-dark-card">
                <q-item v-for="flow in flows" :key="flow.id" clickable v-ripple class="text-white">
                  <q-item-section avatar>
                    <q-icon name="hub" color="secondary" />
                  </q-item-section>
                  <q-item-section>
                    <q-item-label>{{ flow.name }}</q-item-label>
                    <q-item-label caption class="text-grey-7">{{ flow.description }}</q-item-label>
                  </q-item-section>
                  <q-item-section side>
                    <q-btn flat round dense icon="more_vert" color="secondary">
                      <q-menu class="bg-dark-card text-white">
                        <q-list style="min-width: 150px">
                          <q-item clickable v-close-popup @click="editFlow(flow)">
                            <q-item-section avatar>
                              <q-icon name="edit" color="secondary" />
                            </q-item-section>
                            <q-item-section>Modifica</q-item-section>
                          </q-item>
                          <q-item clickable v-close-popup @click="deleteFlow(flow)">
                            <q-item-section avatar>
                              <q-icon name="delete" color="secondary" />
                            </q-item-section>
                            <q-item-section>Elimina</q-item-section>
                          </q-item>
                        </q-list>
                      </q-menu>
                    </q-btn>
                  </q-item-section>
                </q-item>
              </q-list>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Dialog Aggiungi Dispositivo -->
    <q-dialog v-model="showAddDeviceDialog">
      <q-card class="bg-dark-card text-white" style="min-width: 350px">
        <q-card-section class="bg-primary text-white">
          <div class="text-h6">Aggiungi Dispositivo</div>
        </q-card-section>

        <q-card-section class="q-pt-md">
          <q-input v-model="newDevice.name" label="Nome" dark />
          <q-input v-model="newDevice.type" label="Tipo" class="q-mt-md" dark />
          <q-input v-model="newDevice.ip" label="Indirizzo IP" class="q-mt-md" dark />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Annulla" color="primary" v-close-popup />
          <q-btn flat label="Aggiungi" color="primary" @click="addDevice" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Dialog Aggiungi Flusso -->
    <q-dialog v-model="showAddFlowDialog">
      <q-card class="bg-dark-card text-white" style="min-width: 350px">
        <q-card-section class="bg-secondary text-white">
          <div class="text-h6">Nuovo Flusso</div>
        </q-card-section>

        <q-card-section class="q-pt-md">
          <q-input v-model="newFlow.name" label="Nome" dark />
          <q-input v-model="newFlow.description" label="Descrizione" class="q-mt-md" type="textarea" dark />
          <q-select
            v-model="newFlow.sourceDevice"
            :options="devices"
            label="Dispositivo Sorgente"
            class="q-mt-md"
            option-label="name"
            dark
          />
          <q-select
            v-model="newFlow.targetDevice"
            :options="devices"
            label="Dispositivo Destinazione"
            class="q-mt-md"
            option-label="name"
            dark
          />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Annulla" color="secondary" v-close-popup />
          <q-btn flat label="Aggiungi" color="secondary" @click="addFlow" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import { ref } from 'vue'
import { useQuasar } from 'quasar'
import { api } from '../boot/axios'

export default {
  name: 'IndexPage',
  setup() {
    const $q = useQuasar()
    const scanning = ref(false)
    const showAddDeviceDialog = ref(false)
    const showAddFlowDialog = ref(false)

    // Dati di esempio
    const devices = ref([
      { id: 1, name: 'Termostato', type: 'Sensore Temperatura', status: 'online', icon: 'thermostat' },
      { id: 2, name: 'Luci Soggiorno', type: 'Luci Smart', status: 'offline', icon: 'lightbulb' }
    ])

    const flows = ref([
      { id: 1, name: 'Temperatura -> Luci', description: 'Accendi le luci quando la temperatura scende sotto i 20°C' }
    ])

    const newDevice = ref({
      name: '',
      type: '',
      ip: ''
    })

    const newFlow = ref({
      name: '',
      description: '',
      sourceDevice: null,
      targetDevice: null
    })

    const scanNetwork = async () => {
      scanning.value = true
      try {
        // Chiamata API al backend per avviare la scansione
        const response = await api.post('/scan-network', {
          protocol: 'upnp' // Specifica il protocollo da scansionare
        });

        if (response.data.status === 'success') {
          console.log(`Scansione ${response.data.protocol} completata:`, response.data.output);
          $q.notify({
            color: 'positive',
            message: `Scansione ${response.data.protocol} completata`, // Messaggio di successo con il protocollo
            caption: `Output: ${response.data.output.substring(0, 100)}...`, // Mostra parte dell'output (opzionale)
            position: 'top',
            timeout: 5000 // Mantieni il messaggio visibile più a lungo per leggere l'output
          });
          // Qui puoi elaborare ulteriormente response.data.output e mostrarlo nell'interfaccia utente
        } else {
          console.error(`Errore durante la scansione ${response.data.protocol}:`, response.data.message);
          console.error("Dettagli errore:", response.data.details);
          console.error("Output di errore Python:", response.data.errorOutput);
          $q.notify({
            color: 'negative',
            message: `Errore durante la scansione ${response.data.protocol}`,
            caption: `Dettagli: ${response.data.details || response.data.errorOutput || 'Nessun dettaglio'}`,
            position: 'top',
            timeout: 8000 // Mantieni il messaggio visibile più a lungo per gli errori
          });
        }
      } catch (error) {
        console.error("Errore nella chiamata API di scansione:", error);
        $q.notify({
          color: 'negative',
          message: 'Errore nella comunicazione con il backend',
          caption: error.message || 'Verifica la console per i dettagli.',
          position: 'top',
          timeout: 8000
        });
      } finally {
        scanning.value = false
      }
    }

    const addDevice = () => {
      devices.value.push({
        id: devices.value.length + 1,
        name: newDevice.value.name,
        type: newDevice.value.type,
        status: 'offline',
        icon: 'devices'
      })
      newDevice.value = { name: '', type: '', ip: '' }
      $q.notify({
        color: 'positive',
        message: 'Dispositivo aggiunto con successo',
        position: 'top'
      })
    }

    const addFlow = () => {
      flows.value.push({
        id: flows.value.length + 1,
        name: newFlow.value.name,
        description: newFlow.value.description
      })
      newFlow.value = { name: '', description: '', sourceDevice: null, targetDevice: null }
      $q.notify({
        color: 'positive',
        message: 'Flusso aggiunto con successo',
        position: 'top'
      })
    }

    const editFlow = (flow) => {
      // Implementare la logica di modifica
      console.log('Modifica flusso:', flow)
    }

    const deleteFlow = (flow) => {
      const index = flows.value.findIndex(f => f.id === flow.id)
      if (index !== -1) {
        flows.value.splice(index, 1)
        $q.notify({
          color: 'positive',
          message: 'Flusso eliminato con successo',
          position: 'top'
        })
      }
    }

    return {
      scanning,
      devices,
      flows,
      showAddDeviceDialog,
      showAddFlowDialog,
      newDevice,
      newFlow,
      scanNetwork,
      addDevice,
      addFlow,
      editFlow,
      deleteFlow
    }
  }
}
</script>

<style lang="scss" scoped>
.device-card, .flow-card {
  height: 100%;
}

.bg-dark {
  background: #1E1E2E !important;
}

.bg-dark-card {
  background: #2D2D44 !important;
  border: 1px solid #3D3D54;
}

.bg-primary {
  background: #2196F3 !important;
}

.bg-secondary {
  background: #00BCD4 !important;
}

.text-primary {
  color: #2196F3 !important;
}

.text-secondary {
  color: #00BCD4 !important;
}

:deep(.q-field--dark) {
  .q-field__control {
    background: #333;
  }
}

:deep(.q-menu) {
  background: #2D2D44 !important;
  border: 1px solid #3D3D54;
}

:deep(.q-item) {
  &.q-router-link-active {
    color: #2196F3;
    background: rgba(33, 150, 243, 0.1);
  }
  
  &:hover {
    background: rgba(33, 150, 243, 0.05);
  }
}
</style>
