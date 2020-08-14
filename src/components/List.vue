<template>
  <div>
    <!-- NAVBAR -->
    <b-navbar fixed-top class="is-dark">
      <template slot="brand">
        <b-navbar-item href="/">
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

    <section class="app-section">
      <!-- LIST -->
      <div class="container reservation-list">
        <div class="box">
          <!-- FORM TITLE -->
          <h3 class="title is-3">Reservation list</h3>

          <!-- TABLE -->
          <!-- LIST SETTINGS -->

          <!-- DATERANGE FILTER -->
          <b-field grouped>
            <p class="control">
              <b-button type="is-dark" outlined rounded @click="setDateFilter('year')">{{thisYear}}</b-button>
            </p>
            <p class="control">
              <b-button
                type="is-dark"
                outlined
                rounded
                @click="setDateFilter('month')"
              >{{thisMonth}}</b-button>
            </p>
            <p class="control">
              <b-button type="is-dark" outlined rounded @click="setDateFilter('all')">All</b-button>
            </p>
            <b-datepicker
              icon-pack="fas"
              placeholder="Click to select..."
              v-model="filterDates"
              :first-day-of-week="1"
              range
            ></b-datepicker>
          </b-field>

          <!-- TYPE FILTER -->
          <b-field>
            <b-checkbox-button
              v-model="selectedTypes"
              native-value="cancelled"
              type="is-dark"
              outlined
            >Cancelled</b-checkbox-button>

            <b-checkbox-button
              v-model="selectedTypes"
              native-value="inquiry"
              type="is-warning"
            >Inquiry</b-checkbox-button>

            <b-checkbox-button
              v-model="selectedTypes"
              native-value="contract"
              type="is-success"
            >Contract</b-checkbox-button>

            <b-checkbox-button
              v-model="selectedTypes"
              native-value="completed"
              type="is-success"
            >Completed</b-checkbox-button>
          </b-field>

          <!-- STATS -->
          <div class="columns">
            <!-- Results -->
            <div class="column">
              <article class="message is-dark">
                <div class="message-body is-size-6">
                  <p class="is-size-5">
                    Filter
                    <span class="has-text-weight-semibold">({{filterStats.total.number}})</span>
                  </p>
                  <p>
                    Weeks :
                    <span class="has-text-weight-bold">{{filterDateSpan}}</span>
                  </p>
                  <p>
                    Total Value :
                    <span
                      class="has-text-weight-bold"
                    >{{ filterStats.total.totalValue }} €</span>
                  </p>
                </div>
              </article>
            </div>
            <div class="column">
              <article class="message is-success">
                <div class="message-body is-size-6">
                  <p class="is-size-5">
                    Completed
                    <span class="has-text-weight-semibold">({{filterStats.completed.number}})</span>
                  </p>
                  <p>
                    Value :
                    <span class="has-text-weight-bold">{{filterStats.completed.totalValue}} €</span>
                  </p>
                  <p>
                    Average :
                    <span
                      class="has-text-weight-bold"
                    >{{filterStats.completed.averageValue }} €</span>
                  </p>
                </div>
              </article>
            </div>
            <div class="column">
              <article class="message is-success">
                <div class="message-body is-size-6">
                  <p class="is-size-5">
                    Contract
                    <span class="has-text-weight-semibold">({{filterStats.contract.number}})</span>
                  </p>
                  <p>
                    Value :
                    <span class="has-text-weight-bold">{{filterStats.contract.totalValue}} €</span>
                  </p>
                  <p>
                    Average :
                    <span
                      class="has-text-weight-bold"
                    >{{filterStats.contract.averageValue }} €</span>
                  </p>
                </div>
              </article>
            </div>
            <div class="column">
              <article class="message is-warning">
                <div class="message-body is-size-6">
                  <p class="is-size-5">
                    Inquiry
                    <span class="has-text-weight-semibold">({{filterStats.inquiry.number}})</span>
                  </p>
                  <p>
                    Value :
                    <span class="has-text-weight-bold">{{filterStats.inquiry.totalValue}} €</span>
                  </p>
                  <p>
                    Average :
                    <span
                      class="has-text-weight-bold"
                    >{{filterStats.inquiry.averageValue }} €</span>
                  </p>
                </div>
              </article>
            </div>
          </div>

          <!-- TABLE -->
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
            <tbody v-for="booking in filteredBookingList" :key="booking.uuid">
              <tr v-if="(selectedTypes.indexOf(booking.status) != -1) ">
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
                <td>{{booking.paid}} / {{booking.bookingValue}} €</td>
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
      filterDates: [
        moment().startOf("year").toDate(),
        moment().endOf("year").toDate(),
      ],
      selectedTypes: ["inquiry", "contract"],
      apiStateNeedsUpdate: true,
      synced: false,
      justLoaded: true,
      updateTab: false,
      bookingList: [],
      thisYear: moment().year(),
      thisMonth: moment().format("MMMM"),
      yearCompleted: 0,
      yearContracts: 0,
    };
  },
  computed: {
    filterDateSpan: function () {
      return moment(this.filterDates[1]).diff(
        moment(this.filterDates[0]),
        "weeks"
      );
    },
    state: function () {},
    filteredBookingList: function () {
      var filteredBookingList = [];
      var filterDates = this.filterDates;
      var selectedTypes = this.selectedTypes;
      this.bookingList.forEach(function (booking, index) {
        if (
          selectedTypes.indexOf(booking.status) != -1 &&
          moment(filterDates[1]).isSameOrAfter(
            moment(booking.departureDatetime)
          ) &&
          moment(filterDates[0]).isSameOrBefore(
            moment(booking.departureDatetime)
          )
        ) {
          filteredBookingList.push(booking);
        }
      });
      return filteredBookingList;
    },
    filterStats: function () {
      var filteredBookingList = this.filteredBookingList;

      var completedList = filteredBookingList.filter(function (booking) {
        return booking.status == "completed";
      });
      var inquiryList = filteredBookingList.filter(function (booking) {
        return booking.status == "inquiry";
      });
      var contractList = filteredBookingList.filter(function (booking) {
        return booking.status == "contract";
      });

      var filterStats = {
        completed: {
          number: completedList.length,
          totalValue: completedList
            .map((a) => moment(a.bookingValue))
            .reduce((a, b) => a + b, 0),
          averageValue:
            completedList.length > 0
              ? Math.round(
                  completedList
                    .map((a) => moment(a.bookingValue))
                    .reduce((a, b) => a + b, 0) / completedList.length
                )
              : 0,
        },
        inquiry: {
          number: inquiryList.length,
          totalValue: inquiryList
            .map((a) => moment(a.bookingValue))
            .reduce((a, b) => a + b, 0),
          averageValue:
            inquiryList.length > 0
              ? Math.round(
                  inquiryList
                    .map((a) => moment(a.bookingValue))
                    .reduce((a, b) => a + b, 0) / inquiryList.length
                )
              : 0,
        },
        contract: {
          number: contractList.length,
          totalValue: contractList
            .map((a) => moment(a.bookingValue))
            .reduce((a, b) => a + b, 0),
          averageValue:
            contractList.length > 0
              ? Math.round(
                  contractList
                    .map((a) => moment(a.bookingValue))
                    .reduce((a, b) => a + b, 0) / contractList.length
                )
              : 0,
        },
        total: {
          number: filteredBookingList.length,
          totalValue: filteredBookingList
            .map((a) => moment(a.bookingValue))
            .reduce((a, b) => a + b, 0),
          averageValue:
            filteredBookingList.length > 0
              ? Math.round(
                  filteredBookingList
                    .map((a) => moment(a.bookingValue))
                    .reduce((a, b) => a + b, 0) / filteredBookingList.length
                )
              : 0,
        },
      };
      return filterStats;
    },
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
      deep: true,
    },
  },

  methods: {
    setDateFilter: function (period) {
      if (period == "year") {
        this.filterDates = [
          moment().startOf("year").toDate(),
          moment().endOf("year").toDate(),
        ];
      } else if (period == "month") {
        this.filterDates = [
          moment().startOf("month").toDate(),
          moment().endOf("month").toDate(),
        ];
      } else if (period == "all") {
        var bookingList = this.bookingList;
        let result = bookingList.map((a) => moment(a.departureDatetime));
        this.filterDates = [
          moment.min(result).toDate(),
          moment.max(result).toDate(),
        ];
      }
      return null;
    },
    getYearCompleted: function (bookingList) {
      var total = 0;
      var now = moment();
      bookingList.forEach(function (booking, index) {
        var departureDatetime = moment(departureDatetime);
        if (
          departureDatetime.year() == now.year() &&
          booking.status == "completed"
        ) {
          total += booking.bookingValue;
        }
      });
      return total;
    },
    getYearContracts: function (bookingList) {
      var total = 0;
      var now = moment();
      bookingList.forEach(function (booking, index) {
        var departureDatetime = moment(departureDatetime);
        if (
          departureDatetime.year() == now.year() &&
          booking.status == "contract"
        ) {
          total += booking.bookingValue;
        }
      });

      return total;
    },
    getStatusColor: function (bookingStatus) {
      if (bookingStatus === "inquiry") {
        return "is-warning";
      } else if (bookingStatus === "contract") {
        return "is-success";
      } else if (bookingStatus === "completed") {
        return "is-success";
      } else if (bookingStatus === "cancelled") {
        return "is-dark";
      } else {
        return "is-light";
      }
    },

    humanFormatDatetime: function (date) {
      return moment(date).format("ddd D MMM YYYY - HH:mm");
    },
    listEvents: async function (calendarId, query) {
      let params = {
        q: query,
        singleEvents: true,
        orderBy: "startTime",
      };

      let response = await cal.Events.list(calendarId, params);
      var responseArray = [];
      response.forEach(function (event) {
        event.calendarId = calendarId;
        if (event.description.includes(query)) {
          responseArray.push(event);
        }
      });
      return responseArray;
    },
    concatEvents: function (events) {
      var queryResults = [];
      events.forEach((event) => (queryResults = queryResults.concat(event)));
      return queryResults;
    },
    getEvent: async function (query) {
      var promises = [];

      for (const [label, calendarId] of Object.entries(CONFIG.calendarIdList)) {
        promises.push(await this.listEvents(calendarId, query));
      }
      var queryResults = Promise.all(promises).then((result) => {
        return this.concatEvents(promises);
      });
      console.log(queryResults);
      return queryResults;
    },

    getApiBookings: async function (action) {
      const headers = {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json",
      };

      var request = {};

      var bookingList = await axios({
        method: "get",
        url: "http://localhost:5000/api",
        headers: headers,
      })
        .then(function (response) {
          return response.data;
        })
        .catch(function (error) {
          console.log(error);
        });

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
      this.bookingList = bookingList;
      this.yearCompleted = this.getYearCompleted(bookingList);
      this.yearContracts = this.getYearContracts(bookingList);

      return bookingList;
    },
  },
};
</script>

<style lang="scss">
@import "@/scss/_mystyles.scss";

section.app-section {
  background-color: $background;
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
