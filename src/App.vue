<template>
  <div id="app">
    <!-- TITLE -->
    <section class="hero">
      <div class="hero-body">
        <div class="container">
          <h1 class="title has-text-white is-3">stay-manager</h1>
          <h2 class="subtitle has-text-light is-4">Gérez vos réservations via cette page</h2>
        </div>
      </div>
    </section>
    <!-- TABS -->
    <b-tabs id="sheetTabs" size="is-medium is-boxed" v-model="activeTab" expanded>
      <b-tab-item label="Reservation">
        <reservation-tab></reservation-tab>
      </b-tab-item>

      <b-tab-item label="Restauration">
        <catering-tab></catering-tab>
      </b-tab-item>

      <b-tab-item label="Frais" disabled></b-tab-item>

      <b-tab-item label="Facture">
        <invoice-tab></invoice-tab>
      </b-tab-item>
    </b-tabs>

    <div>
      <b-button @click="tempFunction">Click</b-button>
      <p>Payload</p>
      <pre>stay : {{ this.$store.state.stay }}</pre>
      <pre>booking : {{ this.$store.state.booking }}</pre>
      <pre>contact : {{ this.$store.state.contact }}</pre>
      <pre>meals : {{ this.$store.state.meals }}</pre>
    </div>
  </div>
</template>

<script>
import reservationTab from "./tabs/reservation-tab.vue";
import cateringTab from "./tabs/catering-tab.vue";
import invoiceTab from "./tabs/invoice-tab.vue";

import axios from "axios"

console.log(axios)

export default {
  components: {
    reservationTab,
    cateringTab,
    invoiceTab
  },
  data() {
    return {
      activeTab: 0
    };
  },
  computed: {},
  watch: {},

  methods: {
    tempFunction: function() {
      this.$store.state.tempBool = "OK";
      console.log(this.$store.state.booking);
    }
  }
};
</script>

<style lang=scss>
@import "@/scss/_mystyles.scss";

section {
  background-color: $light;
}
.hero {
  background-color: $dark;
}
.control {
  max-width: 15rem;
}

.debug {
  border: solid;
}
</style>
