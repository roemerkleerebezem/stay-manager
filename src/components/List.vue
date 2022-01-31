<template>
  <div>
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
            <b-button
              tag="router-link"
              class="is-light"
              to="./booking"
              type="is-link"
              >New Booking</b-button
            >
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
              <b-button
                type="is-dark"
                outlined
                rounded
                @click="setDateFilter('year')"
                >{{ thisYear }}</b-button
              >
            </p>
            <p class="control">
              <b-button
                type="is-dark"
                outlined
                rounded
                @click="setDateFilter('previous-year')"
                >{{ thisYear - 1 }}</b-button
              >
            </p>
            <p class="control">
              <b-button
                type="is-dark"
                outlined
                rounded
                @click="setDateFilter('month')"
                >{{ thisMonth }}</b-button
              >
            </p>
            <p class="control">
              <b-button
                type="is-dark"
                outlined
                rounded
                @click="setDateFilter('previous-month')"
                >{{ thisMonth }} {{ thisYear - 1 }}</b-button
              >
            </p>
            <p class="control">
              <b-button
                type="is-dark"
                outlined
                rounded
                @click="setDateFilter('all')"
                >All</b-button
              >
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
              >Cancelled</b-checkbox-button
            >

            <b-checkbox-button
              v-model="selectedTypes"
              native-value="inquiry"
              type="is-warning"
              >Inquiry</b-checkbox-button
            >

            <b-checkbox-button
              v-model="selectedTypes"
              native-value="contract"
              type="is-success"
              >Contract</b-checkbox-button
            >

            <b-checkbox-button
              v-model="selectedTypes"
              native-value="completed"
              type="is-success"
              >Completed</b-checkbox-button
            >
          </b-field>

          <!-- STATS -->
          <div class="columns">
            <!-- Results -->
            <div class="column">
              <article class="message is-dark">
                <div class="message-body is-size-6">
                  <p class="is-size-5">
                    Filter
                    <span class="has-text-weight-semibold"
                      >({{ filterStats.total.number }})</span
                    >
                  </p>
                  <p>
                    Weeks :
                    <span class="has-text-weight-bold">{{
                      filterDateSpan
                    }}</span>
                  </p>
                  <p>
                    Total :
                    <span class="has-text-weight-bold"
                      >{{ filterStats.total.totalPaid }} €</span
                    >
                  </p>
                  <p>
                    Total Value :
                    <span class="has-text-weight-bold"
                      >{{ filterStats.total.totalValue }} €</span
                    >
                  </p>
                  <p>
                    Total Tax :
                    <span class="has-text-weight-bold"
                      >{{ filterStats.total.tax }} € ({{
                        filterStats.total.taxNights
                      }}
                      nights)</span
                    >
                  </p>
                </div>
              </article>
            </div>
            <div class="column">
              <article class="message is-success">
                <div class="message-body is-size-6">
                  <p class="is-size-5">
                    Completed
                    <span class="has-text-weight-semibold"
                      >({{ filterStats.completed.number }})</span
                    >
                  </p>
                  <p>
                    Total :
                    <span class="has-text-weight-bold"
                      >{{ filterStats.completed.totalPaid }} €</span
                    >
                  </p>
                  <p>
                    Value :
                    <span class="has-text-weight-bold"
                      >{{ filterStats.completed.totalValue }} €</span
                    >
                  </p>
                  <p>
                    Average :
                    <span class="has-text-weight-bold"
                      >{{ filterStats.completed.averageValue }} €</span
                    >
                  </p>
                </div>
              </article>
            </div>
            <div class="column">
              <article class="message is-success">
                <div class="message-body is-size-6">
                  <p class="is-size-5">
                    Contract
                    <span class="has-text-weight-semibold"
                      >({{ filterStats.contract.number }})</span
                    >
                  </p>
                  <p>
                    Total :
                    <span class="has-text-weight-bold"
                      >{{ filterStats.contract.totalPaid }} €</span
                    >
                  </p>
                  <p>
                    Value :
                    <span class="has-text-weight-bold"
                      >{{ filterStats.contract.totalValue }} €</span
                    >
                  </p>
                  <p>
                    Average :
                    <span class="has-text-weight-bold"
                      >{{ filterStats.contract.averageValue }} €</span
                    >
                  </p>
                </div>
              </article>
            </div>
            <div class="column">
              <article class="message is-warning">
                <div class="message-body is-size-6">
                  <p class="is-size-5">
                    Inquiry
                    <span class="has-text-weight-semibold"
                      >({{ filterStats.inquiry.number }})</span
                    >
                  </p>
                  <p>
                    Total :
                    <span class="has-text-weight-bold"
                      >{{ filterStats.inquiry.totalPaid }} €</span
                    >
                  </p>
                  <p>
                    Value :
                    <span class="has-text-weight-bold"
                      >{{ filterStats.inquiry.totalValue }} €</span
                    >
                  </p>
                  <p>
                    Average :
                    <span class="has-text-weight-bold"
                      >{{ filterStats.inquiry.averageValue }} €</span
                    >
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
              <tr v-if="selectedTypes.indexOf(booking.status) != -1">
                <td>{{ booking.invoiceNumber }}</td>
                <td>
                  <b-button
                    :class="getStatusColor(booking.status)"
                    tag="router-link"
                    :to="'/booking/' + booking.uuid"
                    type="is-link"
                    >{{ booking.status }}</b-button
                  >
                </td>
                <td>
                  <a
                    class="has-text-link has-text-weight-bold"
                    :href="'/booking/' + booking.uuid"
                    >{{ booking.name }}</a
                  >
                </td>
                <td>
                  <p>
                    {{ humanFormatDate(booking.arrivalDate) }}
                  </p>
                  <p>
                    {{ humanFormatTime(booking.arrivalTime) }}
                  </p>
                </td>
                <td>{{ booking.nights }}</td>
                <td v-if="booking.minGuests == booking.maxGuests">
                  {{ booking.minGuests }}
                </td>
                <td v-if="booking.minGuests != booking.maxGuests">
                  {{ booking.minGuests }}-{{ booking.maxGuests }}
                </td>
                <td>{{ booking.source }}</td>
                <td>{{ booking.meals }}</td>
                <td>
                  <p>
                    {{ booking.paid }} / {{ booking.total }} ({{
                      booking.value
                    }}) €
                  </p>
                  <p>{{ booking.tax }} € tax</p>
                </td>
                <td>
                  <b-field>
                    <b-rate
                      icon-pack="fas"
                      v-model="booking.rating"
                      disabled
                    ></b-rate>
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
        moment()
          .startOf("year")
          .toDate(),
        moment()
          .endOf("year")
          .toDate(),
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
    filterDateSpan: function() {
      return moment(this.filterDates[1]).diff(
        moment(this.filterDates[0]),
        "weeks"
      );
    },
    state: function() {},
    filteredBookingList: function() {
      var filteredBookingList = [];
      var filterDates = this.filterDates;
      var selectedTypes = this.selectedTypes;
      this.bookingList.forEach(function(booking, index) {
        if (
          selectedTypes.indexOf(booking.status) != -1 &&
          moment(filterDates[1]).isSameOrAfter(
            moment.unix(booking.departureDate)
          ) &&
          moment(filterDates[0]).isSameOrBefore(
            moment.unix(booking.departureDate)
          )
        ) {
          filteredBookingList.push(booking);
        }
      });
      return filteredBookingList;
    },
    filterStats: function() {
      var filteredBookingList = this.filteredBookingList;

      var completedList = filteredBookingList.filter(function(booking) {
        return booking.status == "completed";
      });
      var inquiryList = filteredBookingList.filter(function(booking) {
        return booking.status == "inquiry";
      });
      var contractList = filteredBookingList.filter(function(booking) {
        return booking.status == "contract";
      });

      var filterStats = {
        completed: {
          number: completedList.length,
          totalValue: completedList
            .map((a) => moment(a.value))
            .reduce((a, b) => a + b, 0),
          totalPaid: completedList
            .map((a) => moment(a.total))
            .reduce((a, b) => a + b, 0),
          averageValue:
            completedList.length > 0
              ? Math.round(
                  completedList
                    .map((a) => moment(a.value))
                    .reduce((a, b) => a + b, 0) / completedList.length
                )
              : 0,
        },
        inquiry: {
          number: inquiryList.length,
          totalPaid: inquiryList
            .map((a) => moment(a.total))
            .reduce((a, b) => a + b, 0),
          totalValue: inquiryList
            .map((a) => moment(a.value))
            .reduce((a, b) => a + b, 0),
          averageValue:
            inquiryList.length > 0
              ? Math.round(
                  inquiryList
                    .map((a) => moment(a.value))
                    .reduce((a, b) => a + b, 0) / inquiryList.length
                )
              : 0,
        },
        contract: {
          number: contractList.length,
          totalPaid: contractList
            .map((a) => moment(a.paid))
            .reduce((a, b) => a + b, 0),
          totalValue: contractList
            .map((a) => moment(a.value))
            .reduce((a, b) => a + b, 0),
          averageValue:
            contractList.length > 0
              ? Math.round(
                  contractList
                    .map((a) => moment(a.value))
                    .reduce((a, b) => a + b, 0) / contractList.length
                )
              : 0,
        },
        total: {
          number: filteredBookingList.length,
          totalPaid: filteredBookingList
            .map((a) => moment(a.total))
            .reduce((a, b) => a + b, 0),
          totalValue: filteredBookingList
            .map((a) => moment(a.value))
            .reduce((a, b) => a + b, 0),
          averageValue:
            filteredBookingList.length > 0
              ? Math.round(
                  filteredBookingList
                    .map((a) => moment(a.value))
                    .reduce((a, b) => a + b, 0) / filteredBookingList.length
                )
              : 0,
          tax: filteredBookingList
            .map((a) => moment(a.tax))
            .reduce((a, b) => a + b, 0),
          taxNights: filteredBookingList
            .map((a) => moment(a.taxNights))
            .reduce((a, b) => a + b, 0),
        },
      };
      return filterStats;
    },
  },

  async mounted() {
    await this.getApiBookings("list");
    this.setDateFilter("all");
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
    setDateFilter: function(period) {
      if (period == "year") {
        this.filterDates = [
          moment()
            .startOf("year")
            .toDate(),
          moment()
            .endOf("year")
            .toDate(),
        ];
      } else if (period == "previous-year") {
        this.filterDates = [
          moment()
            .subtract(1, "year")
            .startOf("year")
            .toDate(),
          moment()
            .subtract(1, "year")
            .endOf("year")
            .toDate(),
        ];
      } else if (period == "month") {
        this.filterDates = [
          moment()
            .startOf("month")
            .toDate(),
          moment()
            .endOf("month")
            .toDate(),
        ];
      } else if (period == "previous-month") {
        this.filterDates = [
          moment()
            .subtract(1, "year")
            .startOf("month")
            .toDate(),
          moment()
            .subtract(1, "year")
            .endOf("month")
            .toDate(),
        ];
      } else if (period == "all") {
        var bookingList = this.bookingList;
        let result = bookingList.map((a) => moment.unix(a.departureDate));
        this.filterDates = [
          moment.min(result).toDate(),
          moment.max(result).toDate(),
        ];
      }
      return null;
    },
    getYearCompleted: function(bookingList) {
      var total = 0;
      var now = moment();
      bookingList.forEach(function(booking, index) {
        var departureDate = moment.unix(departureDate);
        if (
          departureDate.year() == now.year() &&
          booking.status == "completed"
        ) {
          total += booking.value;
        }
      });
      return total;
    },
    getYearContracts: function(bookingList) {
      var total = 0;
      var now = moment();
      bookingList.forEach(function(booking, index) {
        var departureDate = moment.unix(departureDate);
        if (
          departureDate.year() == now.year() &&
          booking.status == "contract"
        ) {
          total += booking.value;
        }
      });

      return total;
    },
    getStatusColor: function(bookingStatus) {
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

    humanFormatDateTime: function(date, time) {
      return moment
        .unix(date)
        .hour(moment.unix(time).hour())
        .minute(moment.unix(time).minute())
        .format("ddd D MMM YYYY HH:mm");
    },
    humanFormatDate: function(date) {
      return moment.unix(date).format("ddd D MMM YYYY");
    },
    humanFormatTime: function(time) {
      return moment.unix(time).format("HH:mm");
    },
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
      console.log(queryResults);
      return queryResults;
    },

    getApiBookings: async function(action) {
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
        .then(function(response) {
          return response.data;
        })
        .catch(function(error) {
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
