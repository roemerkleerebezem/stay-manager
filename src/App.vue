<template>
  <div id="app">
    <!-- NAVBAR -->
    <template>
      <b-navbar fixed-top class="is-dark">
        <template slot="brand">
          <b-navbar-item>
            <img src="./assets/merle-round-logo.png" />
            <span class="navbar-item has-text-light"
              >Moulin du Merle stay-manager</span
            >
          </b-navbar-item>
        </template>
        <template slot="start"> </template>

        <template slot="end">
          <b-navbar-item tag="div">
            <div class="buttons">
              <b-button
                @click="getApi(state, 'save')"
                :disabled="synced"
                :class="synced ? 'is-success' : 'is-warning'"
                >{{ synced ? "Saved" : "Save" }}</b-button
              >
            </div>
          </b-navbar-item>
        </template>
      </b-navbar>
    </template>

    <!-- TABS -->
    <b-tabs
      id="sheetTabs"
      size="is-medium is-boxed"
      v-model="activeTab"
      expanded
    >
      <b-tab-item class="has-text-grey" label="Reservation">
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

    <!-- DEBUGGING -->
    <!-- <div>
      <b-collapse :open="false" aria-id="payloadCollapse">
        <button
          class="button is-primary"
          slot="trigger"
          aria-controls="payloadCollapse"
        >
          Toggle Payload
        </button>
        <pre></pre>
      </b-collapse>
    </div> -->
  </div>
</template>

<script>
import reservationTab from "./tabs/reservation-tab.vue";
import cateringTab from "./tabs/catering-tab.vue";
import invoiceTab from "./tabs/invoice-tab.vue";

import AsyncComputed from "vue-async-computed";

import Vue from "vue";
Vue.use(AsyncComputed);

import axios from "axios";

export default {
  components: {
    reservationTab,
    cateringTab,
    invoiceTab
  },
  data() {
    return {
      activeTab: 0,
      apiStateNeedsUpdate: true,
      synced: false
    };
  },
  computed: {
    state: function() {
      return this.$store.state;
    }
  },
  asyncComputed: {
    apiState: {
      get() {
        var apiState = this.getApi(this.state, "retreive");
        this.apiStateNeedsUpdate = false;
        return apiState;
      },
      default() {
        return this.state;
      },
      shouldUpdate() {
        return this.apiStateNeedsUpdate;
      }
    }
  },

  watch: {
    state: {
      handler() {
        if (this.state != this.apiState) {
          this.apiStateNeedsUpdate = true;
        }
        localStorage.setItem("state", JSON.stringify(this.state));
      },
      deep: true
    }
  },

  methods: {
    getApi: async function(state, action) {
      const headers = {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json"
      };

      var localState = state;
      var request = {};
      request["action"] = action;
      request["data"] = localState;

      var synced = this.synced;

      var apiState = await axios({
        method: "post",
        url: "/api",
        headers: headers,
        data: request
      })
        .then(function(response) {
          synced = response.data.synced;
          return response.data.data;
        })
        .catch(function(error) {
          console.log(error);
        });

      if (state.booking.uuid === null) {
        this.$store.commit("addUUID", apiState.booking.uuid);
      }

      this.synced = synced;

      return apiState;
    }
  }
};
</script>

<style lang="scss">
@import "@/scss/_mystyles.scss";

section {
  background-color: $background;
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
