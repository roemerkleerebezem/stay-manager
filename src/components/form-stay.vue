<template>
  <div class="container">
    <!-- FORM SECTION TITLE -->
    <h6 class="title is-6">Nuitées</h6>
    <!-- ARRIVAL -->
    <b-field label="Check-in" label-position="on-border">
      <b-datetimepicker
        v-model="stay.arrivalDatetime"
        ref="arrivalDatetimePicker"
        placeholder="Check-in"
        :timepicker="{incrementMinutes:15}"
        :datetime-formatter="humanFormatDatetime"
        :mobile-native="false"
      >
        <template slot="right">
          <button class="button is-success" @click="$refs.arrivalDatetimePicker.toggle()">
            <b-icon icon="check"></b-icon>
            <span>Valider</span>
          </button>
        </template>
      </b-datetimepicker>
    </b-field>
    <!-- DEPARTURE -->
    <b-field label="Check-out" label-position="on-border">
      <b-datetimepicker
        v-model="stay.departureDatetime"
        ref="departureDatetimePicker"
        placeholder="Check-out"
        :timepicker="{incrementMinutes:15}"
        :datetime-formatter="humanFormatDatetime"
        :mobile-native="false"
      >
        <template slot="right">
          <button class="button is-success" @click="$refs.departureDatetimePicker.toggle()">
            <b-icon icon="check"></b-icon>
            <span>Valider</span>
          </button>
        </template>
      </b-datetimepicker>
    </b-field>

    <!-- GUESTS -->
    <b-field label="Invités payants" label-position="on-border" message="2 ans et plus">
      <b-numberinput v-model="stay.baseGuests" min="10" controlsPosition="compact"></b-numberinput>
    </b-field>

    <!-- CHILDREN -->
    <b-field label="Enfants" label-position="on-border">
      <b-numberinput v-model="stay.children" min="0" controlsPosition="compact"></b-numberinput>
    </b-field>

    <!-- PETS -->
    <b-field label="Animaux de compagnie" label-position="on-border">
      <b-numberinput v-model="stay.pets" min="0" controlsPosition="compact"></b-numberinput>
    </b-field>

    <!-- GUEST INFO -->
    <b-field label="Informations supplémentaires">
      <b-input v-model="stay.guestInfo" type="textarea"></b-input>
    </b-field>

    <!-- GUEST DETAILED CONTROLS -->
    <b-collapse :open="false" class="card" aria-id="editNightContent">
      <div slot="trigger" class="card-header" role="button" aria-controls="editNightContent">
        <p class="card-header-title">{{ this.stay.stayNightArray.length }} nights</p>
        <a class="card-header-icon">
          <b-icon type="is-dark" icon="caret-down"></b-icon>
        </a>
      </div>
      <div class="card-content">
        <div class="content">
          <ul>
            <li v-for="night in stay.stayNightArray" :key="night.id">
              <b-field grouped>
                <b-field
                  style="width:100%;"
                  :label="editNightContentTextFormat(night.date)"
                  type="has-text-grey"
                >
                  <b-numberinput v-model="night.guests" min="10" controlsPosition="compact"></b-numberinput>
                </b-field>
              </b-field>
            </li>
          </ul>
        </div>
      </div>
    </b-collapse>
  </div>
</template>

<script>
import moment from "moment";

export default {
  props: ["stay"],
  data() {
    return {};
  },
  computed: {
    computedStay: function() {
      return Object.assign({}, this.stay);
    },
    stayNightArray: function() {
      var tempStayNightArray = [];
      var tempArrivalDate = moment(this.stay.arrivalDatetime);
      var tempDepartureDate = moment(this.stay.departureDatetime);

      var i = 0;
      while (tempArrivalDate < tempDepartureDate) {
        var tempStayNightObject = {
          id: i,
          date: tempArrivalDate.unix(),
          guests: this.stay.baseGuests
        };
        tempStayNightArray.push(tempStayNightObject);
        tempArrivalDate = tempArrivalDate.add(1, "days");
        i++;
      }
      return tempStayNightArray;
    }
  },
  methods: {
    humanFormatDatetime: function(date) {
      return moment(date).format("ddd D MMM YYYY - HH:mm");
    },
    editNightContentTextFormat: function(date) {
      return moment.unix(date).format("dddd D");
    },
    datetimepickerValidate: function() {
      console.log(this.$refs.dropdown);
    }
  },
  watch: {
    computedStay: {
      // Update departure date (not time) if the arrival date changes
      deep: true,
      handler: function(newStay, oldStay) {
        var oldStayArrivalDatetime = moment(oldStay.arrivalDatetime);
        var oldStayDepartureDatetime = moment(oldStay.departureDatetime);
        var newStayArrivalDatetime = moment(newStay.arrivalDatetime);
        var newStayDepartureDatetime = moment(newStay.departureDatetime);
        if (
          (oldStayArrivalDatetime.format("LL") !==
            newStayArrivalDatetime.format("LL")) &
          (oldStayDepartureDatetime.format("LL") ==
            newStayDepartureDatetime.format("LL"))
        ) {
          this.stay.departureDatetime = newStayArrivalDatetime
            .hour(oldStayDepartureDatetime.hour())
            .minute(oldStayDepartureDatetime.minute())
            .toDate();
        }
        this.stay.stayNightArray = this.stayNightArray;
      }
    }
  }
};
</script>

<style lang=scss>
@import "@/scss/_mystyles.scss";
</style>
