<template>
  <!-- FORM -->
  <section class="section">
    <div class="container">
      <!-- FORM TITLE -->
      <div class="box">
        <h3 class="title is-3">Reservation</h3>
      </div>

      <!-- CONTACT -->
      <div class="box">
        <form-contact class="form-section"></form-contact>
      </div>
      <div class="box">
        <!-- BOOKING -->
        <form-booking class="form-section"></form-booking>
      </div>
      <!-- STAY -->
      <div class="box">
        <form-stay class="form-section"></form-stay>
      </div>
    </div>
  </section>
</template>

<script>
import formContact from "../components/form-contact.vue";
import formBooking from "../components/form-booking.vue";
import formStay from "../components/form-stay.vue";

export default {
  components: {
    formContact,
    formBooking,
    formStay
  },
  data() {
    return {};
  },
  computed: {
    stay: function() {
      return this.$store.state.stay;
    },
    booking: function() {
      return this.$store.state.booking;
    },
    contact: function() {
      return this.$store.state.contact;
    }
  },
  watch: {},

  methods: {}
};
</script>