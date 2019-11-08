<template>
  <!-- FORM -->
  <section class="section">
    <div class="container">
      <!-- FORM TITLE -->
      <div class="box">
        <h1 class="title">Reservation</h1>
      </div>

      <!-- CONTACT -->
      <div class="box">
        <form-contact :contact="contact" class="form-section"></form-contact>
      </div>
      <div class="box">
        <!-- BOOKING -->
        <form-booking :booking="booking" class="form-section"></form-booking>
      </div>
      <!-- STAY -->
      <div class="box">
        <form-stay :stay="stay" class="form-section"></form-stay>
      </div>
    </div>
  </section>
</template>

<script>
import formContact from "../components/form-contact.vue";
import formBooking from "../components/form-booking.vue";
import formStay from "../components/form-stay.vue";
import moment from "moment";

export default {
  components: {
    formContact,
    formBooking,
    formStay
  },
  data() {
    return {
      contact: {
        email: null,
        name: null,
        phone: null,
        nationality: null
      },
      booking: {
        source: null,
        date: null
      },
      stay: {
        arrivalDatetime: moment()
          .hour(17)
          .minute(0)
          .toDate(),
        departureDatetime: moment()
          .hour(14)
          .minute(0)
          .toDate(),
        baseGuests: 10,
        stayNightArray: [],
        children: null,
        guestInfo: null,
        pets: null
      }
    };
  },
  computed: {},
  watch: {},

  methods: {}
};
</script>