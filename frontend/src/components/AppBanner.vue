<template>
  <div class="banner-container">
    <transition-group name="banner">
      <div
        v-for="message in messages"
        :key="message.id"
        :class="['banner', message.type]"
      >
        <q-icon :name="getIcon(message.type)" size="24px" />
        <span class="message">{{ message.text }}</span>
        <q-btn
          flat
          round
          dense
          icon="close"
          @click="removeMessage(message.id)"
          class="close-btn"
        />
      </div>
    </transition-group>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'AppBanner',
  setup() {
    const messages = ref([])
    let messageId = 0

    const addMessage = (text, type = 'info') => {
      const id = messageId++
      messages.value.push({ id, text, type })
      // Rimuovi automaticamente il messaggio dopo 5 secondi
      setTimeout(() => {
        removeMessage(id)
      }, 5000)
    }

    const removeMessage = (id) => {
      const index = messages.value.findIndex(m => m.id === id)
      if (index !== -1) {
        messages.value.splice(index, 1)
      }
    }

    const getIcon = (type) => {
      switch (type) {
        case 'success':
          return 'check_circle'
        case 'error':
          return 'error'
        case 'warning':
          return 'warning'
        default:
          return 'info'
      }
    }

    return {
      messages,
      addMessage,
      removeMessage,
      getIcon
    }
  }
}
</script>

<style lang="scss" scoped>
.banner-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-width: 400px;
}

.banner {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  background: white;
  min-width: 300px;

  &.success {
    border-left: 4px solid #4caf50;
    .message { color: #2e7d32; }
  }

  &.error {
    border-left: 4px solid #f44336;
    .message { color: #c62828; }
  }

  &.warning {
    border-left: 4px solid #ff9800;
    .message { color: #ef6c00; }
  }

  &.info {
    border-left: 4px solid #2196f3;
    .message { color: #1565c0; }
  }

  .message {
    flex: 1;
    margin: 0 12px;
    font-size: 14px;
  }

  .close-btn {
    color: #757575;
    &:hover {
      color: #424242;
    }
  }
}

// Animazioni
.banner-enter-active,
.banner-leave-active {
  transition: all 0.3s ease;
}

.banner-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.banner-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style> 