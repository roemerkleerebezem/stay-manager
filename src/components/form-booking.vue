<template>
  <div class="container">
    <!-- FORM SECTION TITLE -->
    <div class="subsection-header has-background-light">
      <h5 class="is-size-5 subtitle has-text-dark has-text-weight-medium">
        Information
      </h5>
    </div>
    <div class="subsection">
      <!-- BOOKING STATUS -->
      <b-field
        :type="getStatusColor(booking.status)"
        custom-class="is-medium"
        label="Statut"
        label-position="on-border"
      >
        <b-select
          v-model="booking.status"
          size="is-medium"
          placeholder="Select a type"
        >
          <option value="inquiry">Inquiry</option>
          <option value="contract">Definitive</option>
          <option value="completed">Completed</option>
          <option value="cancelled">Cancelled</option>
        </b-select>
      </b-field>

      <!-- BOOKING SOURCE -->
      <b-field label="Source" label-position="on-border">
        <b-select v-model="booking.source" placeholder="Source">
          <option value="airbnb">AirBnb</option>
          <option value="homeaway">HomeAway</option>
          <option value="direct">Direct</option>
          <option value="other">Autre</option>
        </b-select>
      </b-field>
      <!-- BOOKING DATE -->
      <b-field label="Date de réservation">
        <b-datepicker
          icon-pack="fas"
          v-model="booking.date"
          :first-day-of-week="1"
          placeholder="Date de réservation"
          ref="bookingDatePicker"
        >
          <button
            class="button is-success"
            @click="$refs.bookingDatePicker.toggle()"
          >
            <b-icon pack="fas" icon="check"></b-icon>
            <span>Valider</span>
          </button>
        </b-datepicker>
      </b-field>
    </div>
  </div>
</template>

<script>
import moment from "moment";

export default {
  props: {},
  data() {
    return {
      booking: this.$store.state.booking,
    };
  },
  computed: {
    bookingDate: function() {
      var returnDate =
        this.booking.date == null ? null : moment(this.booking.date).toDate();
      console.log(this.booking.date);
      return returnDate;
    },
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
        return "is-grey";
      } else {
        return "is-grey";
      }
    },
  },
};
</script>

<style scoped></style>
