import { boot } from 'quasar/wrappers'
import { createApp } from 'vue'
import AppBanner from 'components/AppBanner.vue'

export default boot(({ app }) => {
  // Crea un div per il banner
  const bannerDiv = document.createElement('div')
  bannerDiv.id = 'app-banner'
  document.body.appendChild(bannerDiv)

  // Crea un'istanza del componente banner
  const bannerApp = createApp(AppBanner)
  const bannerInstance = bannerApp.mount('#app-banner')

  // Aggiungi il metodo showBanner all'app
  app.config.globalProperties.$banner = {
    success: (message) => bannerInstance.addMessage(message, 'success'),
    error: (message) => bannerInstance.addMessage(message, 'error'),
    warning: (message) => bannerInstance.addMessage(message, 'warning'),
    info: (message) => bannerInstance.addMessage(message, 'info')
  }
}) 