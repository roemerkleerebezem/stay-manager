import VueRouter from "vue-router";

import Vue from "vue";
import App from "./App.vue";

import Form from "./components/Form.vue";

import store from "./store";

import Buefy from "buefy";

import "@fortawesome/fontawesome-free/css/all.css";
import "@fortawesome/fontawesome-free/js/all.js";

import AsyncComputed from "vue-async-computed";

Vue.use(AsyncComputed);
Vue.use(Buefy, { defaultIconPack: "fas" });

Vue.use(VueRouter);

Vue.config.productionTip = false;

const routes = [
  { path: "/booking", component: Form },
  { path: "/booking/:uuid", props: true, component: Form }
];

const router = new VueRouter({
  routes,
  mode: "history"
});

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
