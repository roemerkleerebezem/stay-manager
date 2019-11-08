<template>
  <div id="app">
    <!-- TITLE -->
    <section class="hero">
      <div class="hero-body">
        <div class="container">
          <h1 class="title has-text-white">stay-manager</h1>
          <h2 class="subtitle has-text-light">Gérez vos réservations via cette page</h2>
        </div>
      </div>
    </section>

    <!-- FORM -->
    <section class="section">
      <div class="container">
        <!-- FORM TITLE -->
        <div class="box">
          <h1 class="title">Formulaire</h1>
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
        <b-button @click="tempClickMe">clickMe</b-button>
      </div>
    </section>
  </div>
</template>

<script>
import formContact from "./components/form-contact.vue";
import formBooking from "./components/form-booking.vue";
import formStay from "./components/form-stay.vue";
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

  methods: {
    tempClickMe: function() {
      console.log(this.stay.stayNightArray);
    }
  }
};
</script>

<style>
section {
  background-color: #e8e8e8;
}
.hero {
  background-color: #292929;
}
.control {
  max-width: 15em;
}
</style>

