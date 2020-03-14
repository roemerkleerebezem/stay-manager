<template>
  <div>
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
            <b-button tag="router-link" class="is-light" to="/booking" type="is-link">New Booking</b-button>
          </div>
        </b-navbar-item>
      </template>
    </b-navbar>

    <section>
      <!-- LIST -->
      <div class="container reservation-list">
        <div class="box">
          <!-- FORM TITLE -->
          <h3 class="title is-3">Reservation list</h3>

          <!-- TABLE -->
          <b-field>
            <div class="control">
              <b-switch v-model="showAll">Show All</b-switch>
            </div>
          </b-field>

          <table class="table is-fullwidth is-bordered">
            <thead>
              <tr class="has-background-light">
                <th>No.</th>
                <th>Status</th>
                <th>Nom</th>
                <th>Check-in</th>
                <th>Nuits</th>
                <th>Clients</th>
                <th>Source</th>
                <th>Repas</th>
                <th>Valeur</th>
                <th>Avis</th>
              </tr>
            </thead>
            <tbody v-for="booking in bookingList" :key="booking.uuid">
              <tr v-if="(booking.status =='contract'|booking.status =='inquiry')|(showAll)">
                <td>{{booking.invoiceNumber}}</td>
                <td>
                  <b-button
                    :class="getStatusColor(booking.status)"
                    tag="router-link"
                    :to="'/booking/'+booking.uuid"
                    type="is-link"
                  >{{booking.status}}</b-button>
                </td>
                <td>
                  <a
                    class="has-text-link has-text-weight-bold"
                    :href="'/booking/'+booking.uuid"
                  >{{booking.name}}</a>
                </td>
                <td>{{humanFormatDatetime(booking.arrivalDatetime)}}</td>
                <td>{{booking.nights}}</td>
                <td>{{booking.baseGuests}}</td>
                <td>{{booking.source}}</td>
                <td>{{booking.meals}}</td>
                <td>{{booking.bookingValue}} €</td>
                <td>
                  <b-field>
                    <b-rate icon-pack="fas" v-model="booking.rating" disabled></b-rate>
                  </b-field>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- VALUE PER YEAR -->
      <div class="container reservation-list">
        <div class="box">
          <!-- FORM TITLE -->
          <h3
            class="title is-3"
          >Reservation value for {{thisYear}} : {{yearCompleted + yearContracts}} €</h3>
          <h4 class="title is-4">Completed reservations:</h4>
          <h5 class="title is-5">{{yearCompleted}} €</h5>
          <h4 class="title is-4">Upcoming contracts:</h4>
          <h5 class="title is-5">{{yearContracts}} €</h5>

          <!-- TABLE -->
        </div>
      </div>
    </section>
  </div>
</template>

<script>
const CONFIG = require("@/scripts/settings");
const CalendarAPI = require("node-google-calendar");
let cal = new CalendarAPI(CONFIG);

import axios from "axios";

import moment from "moment";

export default {
  components: {},

  data() {
    return {
      showAll: false,
      apiStateNeedsUpdate: true,
      synced: false,
      justLoaded: true,
      updateTab: false,
      bookingList: [],
      thisYear: moment().year()
    };
  },
  computed: {
    state: function() {},
    yearCompleted: function() {
      var total = 0;
      var now = moment();
      this.bookingList.forEach(function(booking, index) {
        var departureDatetime = moment(departureDatetime);
        if (
          departureDatetime.year() == now.year() &&
          departureDatetime <= now
        ) {
          total += booking.bookingValue;
        }
      });

      return total;
    },
    yearContracts: function() {
      var total = 0;
      var now = moment();
      this.bookingList.forEach(function(booking, index) {
        var departureDatetime = moment(departureDatetime);
        if (departureDatetime.year() == now.year() && departureDatetime > now) {
          total += booking.bookingValue;
        } else {
          console.log(departureDatetime);
        }
      });

      return total;
    }
  },

  async mounted() {
    await this.getApiBookings("list");
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
    getStatusColor: function(bookingStatus) {
      if (bookingStatus === "inquiry") {
        return "is-warning";
      } else if (bookingStatus === "contract") {
        return "is-success";
      } else if (bookingStatus === "completed") {
        return "is-success";
      } else if (bookingStatus === "cancelled") {
        return "is-danger";
      } else {
        return "is-grey";
      }
    },

    humanFormatDatetime: function(date) {
      return moment(date).format("ddd D MMM YYYY - HH:mm");
    },
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

    getApiBookings: async function(action) {
      const headers = {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json"
      };

      var request = {};

      var bookingList = await axios({
        method: "get",
        url: "http://localhost:5000/api",
        headers: headers
      })
        .then(function(response) {
          return response.data;
        })
        .catch(function(error) {
          console.log(error);
        });

      if (action === "save") {
        this.upsertEvent(apiState);
        this.$router.push(`/booking/${apiState.booking.uuid}`).catch(err => {});
      }

      if (action === "retrieve") {
        this.$store.commit("replaceState", apiState);
        this.updateTab = true;
      }
      this.bookingList = bookingList;

      return bookingList;
    }
  }
};
</script>

<style lang="scss">
@import "@/scss/_mystyles.scss";

section {
  background-color: $background;
  min-height: 95vh;
}

.hero {
  background-color: $dark;
}

.debug {
  border: solid;
}

.reservation-list {
  padding-top: 5vh;
}
</style>
