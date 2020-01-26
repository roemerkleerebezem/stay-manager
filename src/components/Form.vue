<template>
  <div>
    <template>
      <!-- NAVBAR -->
      <b-navbar fixed-top class="is-dark">
        <template slot="brand">
          <b-navbar-item>
            <img src="@/assets/merle-round-logo.png" />
            <span class="navbar-item has-text-light">Moulin du Merle stay-manager</span>
          </b-navbar-item>
        </template>
        <template slot="start"></template>

        <template slot="end">
          <b-navbar-item tag="div">
            <div class="buttons">
              <b-button
                @click="getApi(state, 'save')"
                :disabled="synced"
                :class="synced ? 'is-success' : 'is-warning'"
              >{{ synced ? "Saved" : "Save" }}</b-button>
            </div>
          </b-navbar-item>
        </template>
      </b-navbar>
    </template>

    <!-- TABS -->
    <b-tabs :key="updateTab" id="sheetTabs" size="is-medium is-boxed" v-model="activeTab" expanded>
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
    <div>
      <b-collapse :open="false" aria-id="payloadCollapse">
        <button
          class="button is-primary"
          slot="trigger"
          aria-controls="payloadCollapse"
        >Toggle Payload</button>
        <!-- <pre>api : {{apiState}}</pre> -->
        <pre>state : {{state}}</pre>
      </b-collapse>
    </div>
  </div>
</template>

<script>
import reservationTab from "@/tabs/reservation-tab.vue";
import cateringTab from "@/tabs/catering-tab.vue";
import invoiceTab from "@/tabs/invoice-tab.vue";

const ical = require("ical-generator");

import downloadjs from "downloadjs";

import axios from "axios";

import moment from "moment";

export default {
  components: {
    reservationTab,
    cateringTab,
    invoiceTab
  },
  beforeMount() {
    window.addEventListener("beforeunload", event => {
      if (this.synced) return;
      event.preventDefault();
      event.returnValue = "";
    });
  },
  data() {
    return {
      activeTab: 0,
      apiStateNeedsUpdate: true,
      synced: false,
      justLoaded: true,
      updateTab: false
    };
  },
  computed: {
    state: function() {
      return this.$store.state;
    }
  },
  mounted: function() {
    getBookingFromUrl: {
      var uuid = this.$route.params.uuid;
      if (uuid !== undefined) {
        this.state.booking.uuid = uuid;
        this.getApi(this.state, "retrieve");
      }
      localStorage.setItem("state", this.state);
    }
  },
  asyncComputed: {
    apiState: {
      get() {
        var apiState = this.getApi(this.state, "update");
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
    createCal: function(state) {
      const cal = ical({ domain: "moulindumerle.com", name: "Moulin app" });

      cal.createEvent({
        start: state.stay.arrivalDatetime,
        end: state.stay.departureDatetime,
        summary:
          state.booking.status +
          ": " +
          state.contact.name +
          ", " +
          state.stay.baseGuests +
          "p. via " +
          state.booking.source,
        description:
          "http://localhost:8080/booking/" +
          state.booking.uuid +
          "\n\n" +
          state.contact.name +
          "\n" +
          state.contact.phone +
          "\n" +
          state.contact.email +
          "\n\n" +
          state.stay.baseGuests +
          " adults, " +
          state.stay.children +
          " children, " +
          state.stay.pets +
          " pets" +
          "\n\n" +
          state.stay.guestInfo
      });

      downloadjs(cal.toString(), "test.ics", "text/plain");

      return 1;
    },
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

      if (action === "save") {
        console.log("apiState : " + apiState);
        this.createCal(apiState);
      }

      if (action === "retrieve") {
        this.$store.commit("replaceState", apiState);
        this.updateTab = true;
      }

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
