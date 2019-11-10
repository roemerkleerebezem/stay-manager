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
  </div>
</template>

<script>
import reservationTab from "./tabs/reservation-tab.vue";
import cateringTab from "./tabs/catering-tab.vue";
import invoiceTab from "./tabs/invoice-tab.vue";

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

  methods: {}
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
