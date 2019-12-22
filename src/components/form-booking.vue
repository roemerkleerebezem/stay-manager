<template>
  <div class="container">
    <!-- FORM SECTION TITLE -->
    <h6 class="title is-6">Réservation</h6>
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
        <option value="inquiry">Demande</option>
        <option value="contract">Contrat</option>
        <option value="completed">Achevé</option>
        <option value="cancelled">Annulé</option>
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
</template>

<script>
export default {
  props: {},
  data() {
    return {
      booking: this.$store.state.booking
    };
  },
  computed: {},
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
    }
  }
};
</script>

<style scoped></style>
