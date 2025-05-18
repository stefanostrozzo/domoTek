<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'AuthLayout'
})
</script>

<style lang="scss" scoped>
.q-layout {
  background: linear-gradient(135deg, #1976d2 0%, #64b5f6 100%);
  min-height: 100vh;
}
</style> 