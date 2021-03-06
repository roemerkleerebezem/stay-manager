import Vue from 'vue'
import htmlinvoice from './htmlinvoice.vue'

import store from './store'

import Buefy from 'buefy'

import '@fortawesome/fontawesome-free/css/all.css'
import '@fortawesome/fontawesome-free/js/all.js'

Vue.use(Buefy,
  { defaultIconPack: 'fas' })

Vue.config.productionTip = false

new Vue({
  store,
  render: h => h(htmlinvoice),
}).$mount('#app')
