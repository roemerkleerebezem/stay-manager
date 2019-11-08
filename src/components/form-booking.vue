<template>
  <div class="container">
    <!-- FORM SECTION TITLE -->
    <h6 class="title is-6">Réservation</h6>
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
        v-model="booking.date"
        placeholder="Date de réservation"
        ref="bookingDatePicker"
      >
        <button class="button is-success" @click="$refs.bookingDatePicker.toggle()">
          <b-icon icon="check"></b-icon>
          <span>Valider</span>
        </button>
      </b-datepicker>
    </b-field>
  </div>
</template>

<script>
export default {
  props: {
    booking: {
      type: Object
    }
  },
  data() {
    return {};
  },
  computed: {},
  methods: {}
};
</script>

<style scoped>
</style>
