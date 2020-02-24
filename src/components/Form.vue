<template>
  <div>
    <template>
      <!-- NAVBAR -->
      <b-navbar fixed-top class="is-dark">
        <template slot="brand">
          <b-navbar-item>
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
                type="is-warning"
                :label="
                  dataReady
                    ? ''
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
        <pre>state : {{ state }}</pre>
      </b-collapse>
    </div> -->
  </div>
</template>

<script>
import reservationTab from "@/tabs/reservation-tab.vue";
import cateringTab from "@/tabs/catering-tab.vue";
import invoiceTab from "@/tabs/invoice-tab.vue";

const CONFIG = require("@/scripts/settings");
const CalendarAPI = require("node-google-calendar");
let cal = new CalendarAPI(CONFIG);

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
    },
    dataReady: function() {
      var state = this.state;
      if (
        (state.booking.status !== null) &
        (state.stay.arrivalDatetime.getDate() !=
          state.stay.departureDatetime.getDate())
      ) {
        return true;
      } else {
        return false;
      }
    }
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
    listEvents: async function(calendarId, query) {
      let params = {
        q: query,
        singleEvents: true,
        orderBy: "startTime"
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
      events.forEach(event => (queryResults = queryResults.concat(event)));
      return queryResults;
    },
    getEvent: async function(query) {
      var promises = [];

      for (const [label, calendarId] of Object.entries(CONFIG.calendarIdList)) {
        promises.push(await this.listEvents(calendarId, query));
      }
      var queryResults = Promise.all(promises).then(result => {
        return this.concatEvents(promises);
      });
      console.log(queryResults);
      return queryResults;
    },

    moveEvent: function(calendarId, eventId, destination) {
      return cal.Events.move(calendarId, eventId, destination)
        .then(resp => {
          return resp;
        })
        .catch(err => {
          console.log("Error: moveEvent", err.message);
        });
    },

    upsertEvent: async function(state) {
      var startDateTime = moment(state.stay.arrivalDatetime);
      var endDateTime = moment(state.stay.departureDatetime);
      endDateTime = endDateTime.subtract(1, "days");
      if (
        startDateTime.clone().format("DD-MM-YYYY") ==
        endDateTime.clone().format("DD-MM-YYYY")
      ) {
        endDateTime = startDateTime.clone();
        endDateTime = endDateTime.add(1, "hours");
      }

      let event = {
        start: { dateTime: startDateTime.toDate() },
        end: { dateTime: endDateTime.toDate() },
        summary:
          state.contact.name +
          ", " +
          state.stay.baseGuests +
          "p. " +
          state.stay.stayNightArray.length +
          "n. via " +
          state.booking.source,
        description:
          "http://localhost:8080/booking/" +
          state.booking.uuid +
          "\n\n" +
          state.stay.baseGuests +
          " adults, " +
          state.stay.children +
          " children, " +
          state.stay.pets +
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
          state.contact.email
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
            .then(resp => {
              if (apiEvent.calendarId !== calendarId) {
                this.moveEvent(apiEvent.calendarId, apiEvent.id, {
                  destination: calendarId
                })
                  .then(resp => {
                    return resp;
                  })
                  .catch(err => {
                    console.log("Error: movedEvent", err.message);
                  });
              }
              return resp;
            })
            .catch(err => {
              console.log("Error: updatedEvent", err.message);
            });
        } else if (events.length === 0) {
          cal.Events.insert(calendarId, event)
            .then(resp => {
              console.log("inserted event");
            })
            .catch(err => {
              console.log("Error: insertEvent-" + err.message);
            });
        }
      }
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
        this.upsertEvent(apiState);
        this.$router.push(`/booking/${apiState.booking.uuid}`).catch(err => {});
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

.tab-content {
  min-height: 90vh;
}
</style>