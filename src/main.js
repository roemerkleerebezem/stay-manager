import Vue from 'vue'
import App from './App.vue'

import Buefy from 'buefy'
import 'buefy/dist/buefy.css'

import '@fortawesome/fontawesome-free/css/all.css'
import '@fortawesome/fontawesome-free/js/all.js'

Vue.use(Buefy,
  { defaultIconPack: 'fas' })

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
