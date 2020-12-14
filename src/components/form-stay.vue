<template>
  <div class="container">
    <!-- FORM SECTION TITLE -->
    <div class="subsection-header has-background-light">
      <h5 class="is-size-5 subtitle has-text-dark has-text-weight-medium">
        Nuitées
      </h5>
    </div>
    <div class="columns subsection">
      <div class="column is-9">
        <!-- GUEST DETAILED CONTROLS -->
        <!-- ADD DAY AT START -->
        <div class="buttons">
          <b-button
            icon-pack="fas"
            icon-left="plus-circle"
            type="is-light"
            expanded
            @click="addDays(true)"
            class="is-size-5 has-text-dark has-text-weight-bold"
            >{{ dayBefore }}</b-button
          >
        </div>
        <!-- STAYTNIGHT ARRAY EDITABLE -->
        <article
          class="message is-dark"
          v-for="night in stay.stayNightArray"
          :key="night.id"
        >
          <b-collapse
            animation="slide"
            :aria-id="'nightAria' + night.id"
            :open="false"
          >
            <div
              slot="trigger"
              role="button"
              :aria-controls="'nightAria' + night.id"
              class="message-header"
              aria-close-label="Close message"
            >
              <p class="is-size-5 has-text-light has-text-weight-bold">
                {{ editNightContentTextFormat(night.date) }} -

                <span v-if="night.internal.adults + night.external.adults > 0"
                  ><div class="tag has-text-weight-normal">ADULTS</div>
                  {{ night.internal.adults + night.external.adults }}
                  <span class="has-text-weight-normal"
                    >({{ night.external.adults }} +
                    {{ night.internal.adults }})</span
                  ></span
                >
                &nbsp;
                <span v-if="night.internal.kids + night.external.kids > 0"
                  ><div class="tag has-text-weight-normal">KIDS</div>
                  {{ night.external.kids + night.internal.kids }}
                  <span class="has-text-weight-normal"
                    >({{ night.external.kids }} +
                    {{ night.internal.kids }})</span
                  ></span
                >
                &nbsp;

                <span v-if="night.internal.infants + night.external.infants > 0"
                  ><div class="tag has-text-weight-normal">INFANTS</div>
                  &nbsp;
                  {{ night.external.infants + night.internal.infants }}
                </span>

                <span v-if="night.internal.pets + night.external.pets > 0"
                  ><div class="tag has-text-weight-normal">PETS</div>
                  {{ night.internal.pets + night.external.pets }}</span
                >
              </p>
              <button
                v-if="
                  night == stay.stayNightArray[0] &&
                    night != stay.stayNightArray[stay.stayNightArray.length - 1]
                "
                class="delete is-medium"
                type="is-danger"
                @click="deleteDay(true)"
              ></button>
              <button
                v-if="
                  night ==
                    stay.stayNightArray[stay.stayNightArray.length - 1] &&
                    night != stay.stayNightArray[0]
                "
                class="delete is-medium"
                type="is-danger"
                @click="deleteDay(false)"
              ></button>
            </div>
            <div class="message-body">
              <!-- TABLE START -->
              <table class="table">
                <thead>
                  <tr>
                    <th></th>
                    <th>Platform</th>
                    <th>Direct</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>
                      <p>VILLA</p>
                    </td>
                    <td>
                      <b-numberinput
                        icon-pack="fas"
                        v-model="night.external.villa"
                        min="0"
                        controls-rounded
                        type="is-light"
                      ></b-numberinput>
                    </td>
                    <td>
                      <b-numberinput
                        icon-pack="fas"
                        v-model="night.internal.villa"
                        min="0"
                        controls-rounded
                        type="is-light"
                      ></b-numberinput>
                    </td>
                    <td v-if="night.external.villa + night.internal.villa != 1">
                      <span class="has-text-weight-bold has-text-danger">
                        WARNING: set villa to either internal or external
                      </span>
                    </td>
                  </tr>

                  <tr>
                    <td>ADULTS</td>
                    <td>
                      <b-numberinput
                        icon-pack="fas"
                        v-model="night.external.adults"
                        min="0"
                        controls-rounded
                        type="is-light"
                      ></b-numberinput>
                    </td>
                    <td>
                      <b-numberinput
                        icon-pack="fas"
                        v-model="night.internal.adults"
                        min="0"
                        controls-rounded
                        type="is-light"
                      ></b-numberinput>
                    </td>
                    <td
                      v-if="
                        (night.external.villa > 0) &
                          (night.external.adults == 0)
                      "
                    >
                      <span class="has-text-weight-bold has-text-danger">
                        WARNING: there is external villa but no external guests
                      </span>
                    </td>
                  </tr>

                  <tr>
                    <td>KIDS</td>
                    <td>
                      <b-numberinput
                        icon-pack="fas"
                        v-model="night.external.kids"
                        min="0"
                        controls-rounded
                        type="is-light"
                      ></b-numberinput>
                    </td>
                    <td>
                      <b-numberinput
                        icon-pack="fas"
                        v-model="night.internal.kids"
                        min="0"
                        controls-rounded
                        type="is-light"
                      ></b-numberinput>
                    </td>
                  </tr>

                  <tr>
                    <td>INFANTS</td>
                    <td>
                      <b-numberinput
                        icon-pack="fas"
                        v-model="night.external.infants"
                        min="0"
                        controls-rounded
                        type="is-light"
                      ></b-numberinput>
                    </td>
                    <td>
                      <b-numberinput
                        icon-pack="fas"
                        v-model="night.internal.infants"
                        min="0"
                        controls-rounded
                        type="is-light"
                      ></b-numberinput>
                    </td>
                  </tr>

                  <tr>
                    <td>PETS</td>
                    <td>
                      <b-numberinput
                        icon-pack="fas"
                        v-model="night.external.pets"
                        min="0"
                        controls-rounded
                        type="is-light"
                      ></b-numberinput>
                    </td>
                    <td>
                      <b-numberinput
                        icon-pack="fas"
                        v-model="night.internal.pets"
                        min="0"
                        controls-rounded
                        type="is-light"
                      ></b-numberinput>
                    </td>
                  </tr>
                </tbody>
              </table>
              <!-- TABLE END -->
              <!-- BUTTONS -->
              <b-button
                icon-pack="fas"
                icon-left="arrow-down"
                class="button is-dark"
                outlined
                @click="cloneNightToNext(night.id)"
              >
                <span class="has-text-weight-bold"
                  >Apply to all following nights</span
                >
              </b-button>
            </div>
          </b-collapse>
        </article>
        <!-- ADD DAY AT END -->
        <div class="buttons">
          <b-button
            icon-pack="fas"
            icon-left="plus-circle"
            type="is-light"
            expanded
            @click="addDays(false)"
            class="is-size-5 has-text-dark has-text-weight-bold"
            >{{ dayAfter }}</b-button
          >
        </div>
      </div>
      <div class="column is-3">
        <!-- ARRIVAL -->
        <b-field label="Check-in" label-position="on-border">
          <b-datepicker
            icon-pack="fas"
            :datepicker="{ 'first-day-of-week': 1 }"
            v-model="tempArrivalDate"
            @input="changeArrivalDate()"
            ref="arrivalDatePicker"
            placeholder="Check-in"
            :date-formatter="humanFormatDate"
            :mobile-native="false"
          >
            <button
              class="button is-success"
              @click="$refs.arrivalDatePicker.toggle()"
            >
              <b-icon pack="fas" icon="check"></b-icon>
              <span>Valider</span>
            </button>
          </b-datepicker>
        </b-field>
        <b-field
          ><b-timepicker
            v-model="tempArrivalTime"
            @input="changeTime('arrival')"
            :incrementMinutes="15"
            inline
          ></b-timepicker>
          <b-tag
            v-if="extraHours.arrival != 0"
            :type="
              extraHours.arrival > 0
                ? 'is-danger is-light'
                : 'is-success is-light'
            "
          >
            {{
              extraHours.arrival > 0
                ? "+" + extraHours.arrival
                : extraHours.arrival
            }}
          </b-tag>
        </b-field>
        <!-- DEPARTURE -->
        <b-field label="Check-out" label-position="on-border">
          <b-datepicker
            icon-pack="fas"
            v-model="tempDepartureDate"
            @input="changeDepartureDate()"
            :datepicker="{ 'first-day-of-week': 1 }"
            ref="departureDatePicker"
            placeholder="Check-out"
            :date-formatter="humanFormatDate"
            :mobile-native="false"
          >
            <button
              class="button is-success"
              @click="$refs.departureDatePicker.toggle()"
            >
              <b-icon pack="fas" icon="check"></b-icon>
              <span>Valider</span>
            </button>
          </b-datepicker>
        </b-field>
        <b-field
          ><b-timepicker
            v-model="tempDepartureTime"
            @input="changeTime('departure')"
            :incrementMinutes="15"
            inline
          ></b-timepicker>
          <b-tag
            v-if="extraHours.departure != 0"
            :type="
              extraHours.departure > 0
                ? 'is-danger is-light'
                : 'is-success is-light'
            "
          >
            {{
              extraHours.departure > 0
                ? "+" + extraHours.departure
                : extraHours.departure
            }}
          </b-tag>
        </b-field>

        <!-- GUEST INFO -->
        <b-field label="Informations supplémentaires">
          <b-input v-model="stay.guestInfo" type="textarea"></b-input>
        </b-field>
      </div>
    </div>
  </div>
</template>

<script>
import moment from "moment";

export default {
  data() {
    return {
      stay: this.$store.state.stay,
      stayNightArray: [],
      tempArrivalDate: moment.unix(this.$store.state.stay.arrivalDate).toDate(),
      tempArrivalTime: moment.unix(this.$store.state.stay.arrivalTime).toDate(),
      tempDepartureDate: moment
        .unix(this.$store.state.stay.departureDate)
        .toDate(),
      tempDepartureTime: moment
        .unix(this.$store.state.stay.departureTime)
        .toDate(),
    };
  },
  computed: {
    dayBefore: function() {
      return this.editNightContentTextFormat(
        moment
          .unix(this.stay.arrivalDate)
          .add(-1, "days")
          .unix()
      );
    },
    dayAfter: function() {
      return this.editNightContentTextFormat(
        moment.unix(this.stay.departureDate).unix()
      );
    },
    extraHours: function() {
      var arrivalTime = moment(this.tempArrivalTime);
      var departureTime = moment(this.tempDepartureTime);
      var minArrivalTime = this.$store.state.settings.minArrivalTime;
      var maxDepartureTime = this.$store.state.settings.maxDepartureTime;
      var extraHoursArrival = moment()
        .hours(minArrivalTime.hour)
        .minute(minArrivalTime.minute)
        .diff(
          moment()
            .hours(arrivalTime.hour())
            .minute(arrivalTime.minute()),
          "hours"
        );
      var extraHoursDeparture = moment()
        .hours(departureTime.hour())
        .minute(departureTime.minute())
        .diff(
          moment()
            .hours(maxDepartureTime.hour)
            .minute(maxDepartureTime.minute),
          "hours"
        );

      return { arrival: extraHoursArrival, departure: extraHoursDeparture };
    },
  },
  methods: {
    humanFormatDate: function(date) {
      return moment(date).format("ddd D MMM YYYY");
    },
    editNightContentTextFormat: function(date) {
      return moment.unix(date).format("dddd D");
    },
    cloneNightToNext: function(index) {
      var stayNightArray = this.stay.stayNightArray;
      var clonedNight = JSON.parse(
        JSON.stringify(stayNightArray.find((obj) => obj.id == index))
      );
      stayNightArray.forEach(function(night) {
        if (night.id > clonedNight.id) {
          night.internal = JSON.parse(JSON.stringify(clonedNight.internal));
          night.external = JSON.parse(JSON.stringify(clonedNight.external));
        }
      });
    },
    setStayNightArray: function() {
      var tempStayNightArray = [];
      var tempArrivalDate = moment.unix(this.stay.arrivalDate);
      var tempDepartureDate = moment.unix(this.stay.departureDate);
      var i = 100;
      while (
        tempArrivalDate.clone().startOf("day") <
        tempDepartureDate.clone().startOf("day")
      ) {
        var tempStayNightObject = {
          id: i,
          date: tempArrivalDate.unix(),
          internal: {
            villa: 1,
            adults: 10,
            kids: 0,
            infants: 0,
            pets: 0,
          },
          external: {
            villa: 0,
            adults: 0,
            kids: 0,
            infants: 0,
            pets: 0,
          },
        };
        tempStayNightArray.push(tempStayNightObject);
        tempArrivalDate = tempArrivalDate.add(1, "days");
        i++;
      }
      return tempStayNightArray;
    },
    changeArrivalDate: function() {
      var offset = moment(this.tempArrivalDate).diff(
        moment.unix(this.stay.arrivalDate),
        "days"
      );
      if (offset != 0) {
        this.offsetNightArray(offset);
      }
    },
    changeTime: function(type) {
      if (type == "arrival") {
        this.stay.arrivalTime = moment(this.tempArrivalTime).unix();
      } else {
        this.stay.departureTime = moment(this.tempDepartureTime).unix();
      }
    },
    changeDepartureDate: function() {
      var offset = moment(this.tempDepartureDate).diff(
        moment.unix(this.stay.departureDate),
        "days"
      );
      var stayLength = this.stay.stayNightArray.length;
      console.log("offset : " + offset);
      if (offset != 0) {
        if (offset > 0 && stayLength == 1) {
          this.tempDepartureDate = moment
            .unix(this.stay.departureDate)
            .toDate();
          var n = 0;
          while (n < offset) {
            console.log(n);
            this.addDays(false);
            n = n + 1;
          }
        } else {
          this.offsetNightArray(offset);
        }
      }
    },
    addDays: function(before) {
      var stayNightArray = this.stay.stayNightArray;
      if (before) {
        var extraNight = JSON.parse(JSON.stringify(stayNightArray[0]));
        extraNight.id = extraNight.id - 1;
        extraNight.date = moment
          .unix(extraNight.date)
          .add(-1, "days")
          .unix();
        stayNightArray.unshift(extraNight);
        this.stay.arrivalDate = moment(this.tempArrivalDate)
          .add(-1, "days")
          .unix();
        this.tempArrivalDate = moment.unix(this.stay.arrivalDate).toDate();
      }
      if (before == false) {
        var extraNight = JSON.parse(
          JSON.stringify(stayNightArray[stayNightArray.length - 1])
        );
        extraNight.id = extraNight.id + 1;
        extraNight.date = moment
          .unix(extraNight.date)
          .add(1, "days")
          .unix();
        stayNightArray.push(extraNight);
        this.stay.departureDate = moment(this.tempDepartureDate)
          .add(1, "days")
          .unix();
        this.tempDepartureDate = moment.unix(this.stay.departureDate).toDate();
      }
    },
    deleteDay: function(before) {
      var stayNightArray = this.stay.stayNightArray;
      if (before) {
        stayNightArray.shift();
        this.stay.arrivalDate = moment
          .unix(this.stay.arrivalDate)
          .add(1, "days")
          .unix();
        this.tempArrivalDate = moment.unix(this.stay.arrivalDate).toDate();
      }
      if (before == false) {
        stayNightArray.pop();
        this.stay.departureDate = moment
          .unix(this.stay.departureDate)
          .add(-1, "days")
          .unix();
        this.tempDepartureDate = moment.unix(this.stay.departureDate).toDate();
      }
    },
    offsetNightArray: function(offset) {
      var stay = this.stay;
      stay.arrivalDate = moment
        .unix(stay.arrivalDate)
        .add(offset, "days")
        .unix();
      stay.departureDate = moment
        .unix(stay.departureDate)
        .add(offset, "days")
        .unix();
      // ARRAY
      stay.stayNightArray.forEach(function(night) {
        night.date = moment
          .unix(night.date)
          .add(offset, "days")
          .unix();
      });
      this.tempArrivalDate = moment.unix(stay.arrivalDate).toDate();
      this.tempDepartureDate = moment.unix(stay.departureDate).toDate();
    },
  },
  watch: {},
};
</script>

<style lang="scss">
@import "@/scss/_mystyles.scss";

.b-numberinput {
  max-width: 150px;
}

.table {
  background-color: transparent;
}
</style>
