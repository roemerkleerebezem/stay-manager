<template>
  <section class="app-section">
    <template>
      <!-- NAVBAR -->
      <b-navbar fixed-top class="is-dark">
        <template slot="brand">
          <b-navbar-item href="/">
            <img src="@/assets/merle-round-logo.png" />
            <span class="navbar-item has-text-light"
              >Moulin du Merle stay-manager</span
            >
          </b-navbar-item>
        </template>
        <template slot="start"></template>

        <template slot="end">
          <b-navbar-item tag="div">
            <div class="buttons">
              <b-tooltip
                :type="dataReady ? 'is-success' : 'is-warning'"
                :label="
                  dataReady
                    ? 'Save the booking'
                    : 'Missing information, either booking status or dates'
                "
                position="is-left"
                size="is-large"
                multilined
              >
                <b-button
                  @click="getApi(state, 'save')"
                  :disabled="synced || !dataReady"
                  :class="synced ? 'is-success' : 'is-warning'"
                  >{{ synced ? "Saved" : "Save" }}</b-button
                >
              </b-tooltip>
            </div>
          </b-navbar-item>
        </template>
      </b-navbar>
    </template>

    <!-- TABS -->
    <b-tabs
      :key="updateTab"
      style="margin-top:55.972px;"
      id="sheetTabs"
      size="is-medium is-boxed"
      v-model="activeTab"
      expanded
      class="has-text-weight-medium"
    >
      <b-tab-item label="Reservation">
        <reservation-tab></reservation-tab>
      </b-tab-item>

      <b-tab-item label="Restauration">
        <catering-tab></catering-tab>
      </b-tab-item>

      <b-tab-item label="Facture">
        <invoice-tab></invoice-tab>
      </b-tab-item>

      <b-tab-item label="Settings">
        <settings-tab></settings-tab>
      </b-tab-item>
    </b-tabs>

    <!-- BOOKING INFORMATION MODAL -->
    <b-modal
      :active.sync="isStoreModalActive"
      has-modal-card
      :destroy-on-hide="false"
      trap-focus
      scroll="keep"
    >
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Booking data</p>
          <button
            type="button"
            class="delete"
            @click="isDepositModalActive = false"
          />
        </header>
        <section class="modal-card-body">
          <div v-for="(value, propertyName) in state" v-bind:key="propertyName">
            <span class="tag is-dark is-small">{{ propertyName }}</span>
            <pre>{{ value }}</pre>
          </div>
        </section>
      </div>
    </b-modal>

    <!-- FOOTER -->
    <footer class="footer has-background-dark level">
      <div class="level-left">
        <div class="level-item">
          <b-checkbox
            type="is-danger"
            size="is-medium"
            class="has-text-light is-pulled-left is-family-code"
            v-model="devIsTrue"
            >DO NOT UPDATE CALENDAR</b-checkbox
          >
        </div>
      </div>
      <div class="level-right">
        <div class="level-item">
          <b-button @click="isStoreModalActive = true" class="is-family-code"
            >Show booking details</b-button
          >
        </div>
      </div>
    </footer>
  </section>
</template>

<script>
import reservationTab from "@/tabs/reservation-tab.vue";
import cateringTab from "@/tabs/catering-tab.vue";
import invoiceTab from "@/tabs/invoice-tab.vue";
import settingsTab from "@/tabs/settings-tab.vue";

const CONFIG = require("@/scripts/settings");
const CalendarAPI = require("node-google-calendar");
let cal = new CalendarAPI(CONFIG);

import axios from "axios";

import moment from "moment";

export default {
  components: {
    reservationTab,
    cateringTab,
    invoiceTab,
    settingsTab,
  },
  beforeMount() {
    window.addEventListener("beforeunload", (event) => {
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
      updateTab: false,
      devIsTrue: false,
      isStoreModalActive: false,
    };
  },
  computed: {
    state: function() {
      return this.$store.state;
    },
    dataReady: function() {
      var state = this.state;
      if (
        (state.booking.status !== null) &
        (state.stay.arrivalDate != state.stay.departureDate)
      ) {
        return true;
      } else {
        return false;
      }
    },
  },

  mounted: async function() {
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
      },
    },
  },

  watch: {
    state: {
      handler() {
        if (this.state != this.apiState) {
          this.apiStateNeedsUpdate = true;
        }
        localStorage.setItem("state", JSON.stringify(this.state));
      },
      deep: true,
    },
  },

  methods: {
    listEvents: async function(calendarId, query) {
      let params = {
        q: query,
        singleEvents: true,
        orderBy: "startTime",
      };

      let response = await cal.Events.list(calendarId, params);
      var responseArray = [];
      response.forEach(function(event) {
        event.calendarId = calendarId;
        if (event.description.includes(query)) {
          responseArray.push(event);
        }
      });
      return responseArray;
    },
    concatEvents: function(events) {
      var queryResults = [];
      events.forEach((event) => (queryResults = queryResults.concat(event)));
      return queryResults;
    },
    getEvent: async function(query) {
      var promises = [];

      for (const [label, calendarId] of Object.entries(CONFIG.calendarIdList)) {
        promises.push(await this.listEvents(calendarId, query));
      }
      var queryResults = Promise.all(promises).then((result) => {
        return this.concatEvents(promises);
      });
      return queryResults;
    },

    upsertEvent: async function(state) {
      if (this.devIsTrue) {
        this.$buefy.toast.open({
          message: "Booking not changed in calendar",
          type: "is-danger",
          duration: 5000,
        });
        return null;
      }
      var startTime = moment.unix(state.stay.arrivalTime);
      var endTime = moment.unix(state.stay.departureTime);
      var startDateTime = moment
        .unix(state.stay.arrivalDate)
        .hour(startTime.hour())
        .minute(startTime.minute());
      var endDateTime = moment
        .unix(state.stay.departureDate)
        .hour(endTime.hour())
        .minute(endTime.minute());
      endDateTime = endDateTime.subtract(1, "days");
      if (
        startDateTime.clone().format("DD-MM-YYYY") ==
        endDateTime.clone().format("DD-MM-YYYY")
      ) {
        endDateTime = startDateTime.clone();
        endDateTime = endDateTime.add(1, "hours");
      }

      var maxChildren = Math.max.apply(
        Math,
        state.stay.stayNightArray.map(function(o) {
          return o.internal.kids + o.external.kids;
        })
      );

      var maxAdults = Math.max.apply(
        Math,
        state.stay.stayNightArray.map(function(o) {
          return o.internal.adults + o.external.adults;
        })
      );

      var maxPets = Math.max.apply(
        Math,
        state.stay.stayNightArray.map(function(o) {
          return o.internal.pets + o.external.pets;
        })
      );

      var maxPersons = Math.max.apply(
        Math,
        state.stay.stayNightArray.map(function(o) {
          return (
            o.internal.adults +
            o.external.adults +
            o.internal.kids +
            o.external.kids
          );
        })
      );

      let event = {
        start: { dateTime: startDateTime.toDate() },
        end: { dateTime: endDateTime.toDate() },
        summary:
          state.contact.name +
          ", " +
          maxPersons +
          "p. " +
          state.stay.stayNightArray.length +
          "n. via " +
          state.booking.source,
        description:
          "http://localhost:8080/booking/" +
          state.booking.uuid +
          "\n\n" +
          maxAdults +
          " adults, " +
          maxChildren +
          " children, " +
          maxPets +
          " pets" +
          "\n" +
          "Check-out : " +
          endDateTime.format("HH:mm") +
          "\n\n" +
          state.stay.guestInfo +
          "\n\n" +
          state.meals.length +
          " meals" +
          "\n\n" +
          state.contact.name +
          "\n" +
          state.contact.phone +
          "\n" +
          state.contact.email,
      };

      var status = state.booking.status;
      if (status === null) {
        console.log("No status given, can't update calendar");
        return 1;
      }
      var calendarId =
        status === "cancelled"
          ? CONFIG.calendarIdList.cancelled
          : status === "inquiry"
          ? CONFIG.calendarIdList.inquiry
          : CONFIG.calendarIdList.definitive;

      var uuid = state.booking.uuid;
      if (uuid === null) {
        console.log("uuid is null");
      } else {
        var events = await this.getEvent(uuid);
        if (events.length === 1) {
          var apiEvent = events[0];
          cal.Events.update(apiEvent.calendarId, apiEvent.id, event)
            .then((resp) => {
              if (apiEvent.calendarId !== calendarId) {
                cal.Events.delete(apiEvent.calendarId, apiEvent.id)
                  .then((results) => {
                    cal.Events.insert(calendarId, event)
                      .then((resp) => {
                        this.$buefy.toast.open({
                          message: "Booking updated and moved",
                          type: "is-light",
                          duration: 5000,
                        });
                      })
                      .catch((err) => {
                        console.log("Error: insertEvent " + err.message);
                      });
                  })
                  .catch((err) => {
                    console.log(
                      "Error deleteEvent:" + JSON.stringify(err.message)
                    );
                  });
              } else {
                this.$buefy.toast.open({
                  message: "Booking updated",
                  type: "is-light",
                  duration: 5000,
                });
              }
              return resp;
            })
            .catch((err) => {
              console.log("Error: updatedEvent", err.message);
            });
        } else if (events.length === 0) {
          cal.Events.insert(calendarId, event)
            .then((resp) => {
              this.$buefy.toast.open({
                message: "Added new booking in calendar",
                type: "is-success",
                duration: 5000,
              });
            })
            .catch((err) => {
              console.log("Error: insertEvent " + err.message);
            });
        }
      }
    },
    getApi: async function(state, action) {
      const headers = {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json",
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
        data: request,
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
        this.upsertEvent(apiState);
        this.$router
          .push(`/booking/${apiState.booking.uuid}`)
          .catch((err) => {});
      }

      if (action === "retrieve") {
        this.$store.commit("replaceState", apiState);
        this.updateTab = true;
      }

      return apiState;
    },
  },
};
</script>

<style lang="scss">
@import "@/scss/_mystyles.scss";

nav.tabs > ul > li {
  background-color: white;
}

section.app-section {
  background-color: "transparent";
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

.tab-content {
  min-height: 90vh;
}
</style>
