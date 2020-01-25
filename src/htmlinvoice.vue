<template>
  <div id="app">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.2.0/css/all.css" />

    <!-- TOTAL INVOICE FLEX-->
    <div class="A4 sheet stretchy-wrapper flex-container">
      <!-- HEADER -->
      <div class="header">
        <!-- INVOICE HEADER -->
        <div class="level">
          <div class="level-left">
            <div class="level-item">
              <div class="container">
                <h4
                  class="title is-size-4 is-uppercase"
                >{{ state.booking.status === 'completed'?'Facture #'+state.booking.invoiceNumber:"Réservation"}}</h4>
                <span
                  :class="
                    getStatusColor(state.booking.status) + ' is-uppercase tag'
                  "
                >{{ state.booking.status }}</span>
              </div>
            </div>
          </div>
          <div class="level-right">
            <div class="level-item">
              <div class="container is-size-7 has-text-right">
                <p>{{ todayDate }}</p>
                <p>St. Germain des Bois</p>
              </div>
            </div>
          </div>
        </div>
        <!-- HOST AND CLIENT -->
        <div class="container padding-10mm">
          <div class="card">
            <div class="card-content">
              <div class="columns is-mobile">
                <!-- HOST -->
                <div class="column">
                  <div class="has-text-centered">
                    <h6 class="title is-6">HÔTE</h6>
                    <p>Gilberthe AKKERMANS</p>
                    <p>Moulin du Merle</p>
                    <p>58210 Saint-Germain-des-Bois</p>
                    <p>06 77 29 83 45</p>
                    <p>moulindumerle@gmail.com</p>
                  </div>
                </div>
                <!-- HOST -->
                <div class="column">
                  <div class="has-text-centered">
                    <h6 class="title is-6">CLIENT</h6>
                    <p>{{ state.contact.name }}</p>
                    <br />
                    <br />
                    <p>{{ state.contact.phone }}</p>
                    <p>{{ state.contact.email }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- TOTAL INVOICE TABLE -->
      <div>
        <table class="table is-fullwidth is-bordered">
          <thead>
            <tr class="has-background-light">
              <th>Produit</th>
              <th>Total</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="staySubtotal*(1-invoiceData.discount) !== 0">
              <td>Total sejour</td>
              <td>{{staySubtotal*(1-invoiceData.discount) + invoiceData.taxedNights*state.prices.taxeSejourNight}} €</td>
            </tr>
            <tr v-if="cateringSubtotal !== 0">
              <td>Total restauration</td>
              <td>{{cateringSubtotal}} €</td>
            </tr>
            <tr class="has-background-light">
              <td class="has-text-darkgrey is-uppercase has-text-weight-semibold">Sous-total</td>
              <td
                class="has-text-darkgrey is-uppercase has-text-weight-bold"
              >{{staySubtotal*(1-invoiceData.discount) + invoiceData.taxedNights*state.prices.taxeSejourNight + cateringSubtotal}} €</td>
            </tr>
          </tbody>
          <tbody v-for="cost in state.booking.costs" :key="cost.id">
            <tr>
              <td :class="cost.type==='payment'?'has-text-success has-text-weight-semibold':''">
                {{cost.label}}
                <span
                  v-if="(cost.units!== null) & (cost.unitPrice!== null)"
                  class="has-text-grey"
                  style="margin-left:1rem;"
                >{{cost.units}} x {{cost.unitPrice}} €</span>
              </td>
              <td
                :class="cost.type==='payment'?'has-text-success has-text-weight-semibold':''"
              >{{cost.type==="payment"?"-":"+"}}{{cost.totalPrice}} €</td>
            </tr>
          </tbody>
          <tbody>
            <tr class="has-background-light">
              <td class="has-text-darkgrey is-uppercase has-text-weight-semibold">Reste à payer</td>
              <td
                class="has-text-darkgrey is-uppercase has-text-weight-semibold"
              >{{Math.round(100*invoiceTotal)/100}} €</td>
            </tr>
          </tbody>
        </table>
        <p class="has-text-grey has-text-right">TVA non-applicable</p>
      </div>

      <!-- DEPOSIT -->
      <div v-if="state.booking.deposits.length > 0">
        <span class="is-size-5 title">Caution</span>

        <div
          class="container"
          style="margin-bottom:1rem;"
          v-for="deposit in state.booking.deposits"
          :key="deposit.id"
        >
          <article class="message is-light">
            <div class="message-header">
              <p>
                <b-icon
                  style="margin-right:0.5ch;display: inline-table;"
                  pack="fas"
                  :icon="getDepositIcon(deposit.type)"
                  size="is-medium"
                  type="is-grey"
                ></b-icon>
                <span class="has-text-grey is-uppercase">{{ deposit.type }} -</span>
                {{ deposit.amount }} €
              </p>

              <span
                :class="'tag is-medium ' + (deposit.status==='pending'?'is-warning':'is-success') "
              >
                {{
                deposit.dateReceived === null
                ? ""
                : deposit.dateReceived.substring(0, 10) + ", "
                }}
                {{ deposit.status }}
              </span>
            </div>
          </article>
        </div>
      </div>

      <!-- FOOTER -->
      <div>
        <!-- <p class="is-pulled-right">Page 1/3</p> -->
      </div>
    </div>

    <!-- STAY INVOICE FLEX-->
    <div
      v-if="(state.stay.stayNightArray > 0) | (stayNoPrint === false)"
      class="A4 sheet stretchy-wrapper flex-container"
    >
      <!-- HEADER -->
      <div class="header">
        <!-- INVOICE HEADER -->
        <div class="level">
          <div class="level-left">
            <div class="level-item">
              <div class="container">
                <h4
                  class="title is-size-4 is-uppercase"
                >{{ state.booking.status === 'completed'?'Facture #'+state.booking.invoiceNumber:"Réservation"}} - DETAILS SEJOUR</h4>
              </div>
            </div>
          </div>
          <div class="level-right">
            <div class="level-item">
              <div class="container is-size-7 has-text-right">
                <p>{{ todayDate }}</p>
                <p>St. Germain des Bois</p>
              </div>
            </div>
          </div>
        </div>

        <!-- DATES -->
        <div class="container">
          <div class="field is-grouped is-grouped-multiline">
            <div class="control">
              <div class="tags has-addons">
                <span class="tag is-dark">Check-in</span>
                <span class="tag is-light">
                  {{ humanFormatDate(state.stay.arrivalDatetime) }}
                  <b-icon
                    style="margin-left:0.5ch;margin-right:0.5ch;"
                    pack="fas"
                    icon="clock"
                    size="is-small"
                  ></b-icon>
                  {{ humanFormatTime(state.stay.arrivalDatetime) }}
                </span>
              </div>
            </div>
            <div class="control">
              <div class="tags has-addons">
                <span class="tag is-dark">Check-out</span>
                <span class="tag is-light">
                  {{ humanFormatDate(state.stay.departureDatetime) }}
                  <b-icon
                    style="margin-left:0.5ch;margin-right:0.5ch;"
                    pack="fas"
                    icon="clock"
                    size="is-small"
                  ></b-icon>
                  {{ humanFormatTime(state.stay.departureDatetime) }}
                </span>
              </div>
            </div>
            <span class="tag is-dark">{{ state.stay.baseGuests }} personnes</span>
          </div>
        </div>

        <!-- PROPERTY -->
        <div class="container padding-10mm">
          <div class="card">
            <div class="card-content">
              <div class="columns is-mobile">
                <!-- HOST -->
                <div class="column">
                  <h6 class="title is-6">Propriete</h6>
                  <p>Villa de tourisme</p>
                  <p>9 chambres</p>
                  <p>3.5 salles de bains</p>
                  <p>1 cuisine</p>
                </div>
                <div class="column">
                  <img src="./assets/mill_sketch.jpg" />
                </div>

                <!-- HOST -->
                <div class="column">
                  <div class="is-pulled-right">
                    <h6 class="title is-6">Adresse</h6>
                    <p>Moulin du Merle</p>
                    <p>58210</p>
                    <p>St-Germain-des-Bois</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- TOTAL INVOICE TABLE -->
      <table class="table is-fullwidth is-bordered">
        <thead>
          <tr class="has-background-light">
            <th>Produit</th>
            <th>Unités</th>
            <th>Prix unitaire</th>
            <th>Total</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="invoiceData.externalVillaNights>0" class="has-text-weight-light">
            <td>Villa (payé)</td>
            <td>{{invoiceData.externalVillaNights}} nuit(s)</td>
            <td>0 €</td>
            <td>0 €</td>
          </tr>
          <tr v-if="invoiceData.villaNights>0">
            <td>Villa</td>
            <td>{{invoiceData.villaNights}} nuit(s)</td>
            <td>{{state.prices.villaNight}} €</td>
            <td>{{invoiceData.villaNights*state.prices.villaNight}} €</td>
          </tr>
        </tbody>
        <tbody v-for="night in state.stay.stayNightArray" :key="night.id">
          <tr v-if="night.externalGuests > 0" class="has-text-weight-light">
            <td>Couchages {{humanInvoiceDate(night.date, "unix")}} (payé)</td>
            <td>{{night.externalGuests}}</td>
            <td>0 €</td>
            <td>0 €</td>
          </tr>
          <tr v-if="night.guests>0">
            <td>Couchages {{night.externalGuests>0?'supplémentaires':humanInvoiceDate(night.date, "unix")}}</td>
            <td>{{night.guests}}</td>
            <td>{{state.prices.stayNight}} €</td>
            <td>{{night.guests*state.prices.stayNight}} €</td>
          </tr>
        </tbody>
        <tbody>
          <!-- <tr>
            <td>Taxe de séjour</td>
            <td>40</td>
            <td>1 €</td>
            <td>40 €</td>
          </tr>-->
          <tr v-if="state.stay.pets>0">
            <td>Animaux de compagnie</td>
            <td>{{state.stay.pets*invoiceData.villaNights}} nuit(s)</td>
            <td>{{state.prices.petNight}} €</td>
            <td>{{state.stay.pets*invoiceData.villaNights*state.prices.petNight}} €</td>
          </tr>
          <tr v-if="invoiceData.extraHours>0">
            <td>Heures supplémentaires</td>
            <td>{{invoiceData.extraHours}}</td>
            <td>{{state.prices.extraHour}} €</td>
            <td>{{invoiceData.extraHours*state.prices.extraHour}} €</td>
          </tr>
          <tr class="has-background-light">
            <td class="has-text-darkgrey is-uppercase has-text-weight-semibold">Sous-total</td>
            <td></td>
            <td></td>
            <td class="has-text-darkgrey is-uppercase has-text-weight-semibold">{{staySubtotal}} €</td>
          </tr>
          <tr v-if="invoiceData.discount > 0">
            <td>Réduction {{state.stay.stayNightArray.length}} nuits ({{Math.round(100*invoiceData.discount)}}%)</td>
            <td></td>
            <td></td>
            <td
              class="has-text-success has-text-weight-semibold"
            >-{{invoiceData.discount*staySubtotal}} €</td>
          </tr>
          <tr v-if="invoiceData.taxedNights > 0">
            <td>Taxe de séjour</td>
            <td>{{invoiceData.taxedNights}}</td>
            <td>{{state.prices.taxeSejourNight}} €</td>
            <td>{{Math.round( invoiceData.taxedNights*state.prices.taxeSejourNight * 100) / 100 }} €</td>
          </tr>
          <tr class="has-background-light">
            <td class="has-text-darkgrey is-uppercase has-text-weight-semibold">Total séjour</td>
            <td></td>
            <td></td>
            <td
              class="has-text-darkgrey is-uppercase has-text-weight-bold"
            >{{staySubtotal*(1-invoiceData.discount) + invoiceData.taxedNights*state.prices.taxeSejourNight}} €</td>
          </tr>
        </tbody>
      </table>

      <!-- FOOTER -->
      <div>
        <!-- <p class="is-pulled-right">Page 2/3</p> -->
      </div>
    </div>

    <!-- CATERING INVOICE FLEX-->
    <div
      v-if="(state.meals.length > 0) & (cateringNoPrint===false)"
      class="A4 sheet stretchy-wrapper flex-container"
    >
      <!-- HEADER -->
      <div class="header">
        <!-- INVOICE HEADER -->
        <div class="level">
          <div class="level-left">
            <div class="level-item">
              <div class="container">
                <h4
                  class="title is-size-4 is-uppercase"
                >{{ state.booking.status === 'completed'?'Facture #'+state.booking.invoiceNumber:"Réservation"}} - DETAILS RESTAURATION</h4>
              </div>
            </div>
          </div>
          <div class="level-right">
            <div class="level-item">
              <div class="container is-size-7 has-text-right">
                <p>{{ todayDate }}</p>
                <p>St. Germain des Bois</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- TOTAL INVOICE TABLE -->
      <div>
        <table class="table is-fullwidth is-bordered">
          <thead>
            <tr>
              <th>Produit</th>
              <th>Unités</th>
              <th>Prix unitaire</th>
              <th>Total</th>
            </tr>
          </thead>
          <tbody v-for="meal in state.meals" :key="meal.id">
            <tr v-if="meal.adults !=0">
              <td>{{meal.type}} {{humanInvoiceDate(meal.date)}}</td>
              <td>{{meal.adults}} adultes</td>
              <td>{{meal.adultPrice}} €</td>
              <td>{{meal.adults*meal.adultPrice}} €</td>
            </tr>
            <tr v-if="meal.children !=0">
              <td>{{meal.type}} {{(humanInvoiceDate(meal.date))}}</td>
              <td>{{meal.children}} enfants</td>
              <td>{{meal.childPrice}} €</td>
              <td>{{meal.children*meal.childPrice}} €</td>
            </tr>
          </tbody>
          <tbody>
            <tr>
              <td class="has-text-darkgrey is-uppercase has-text-weight-semibold">Total restauration</td>
              <td></td>
              <td></td>
              <td class="has-text-darkgrey is-uppercase has-text-weight-bold">{{cateringSubtotal}} €</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- FOOTER -->
      <div>
        <!-- <p class="is-pulled-right">Page 2/3</p> -->
      </div>
    </div>

    <!-- END -->
  </div>
</template>

<script>
import Vue from "vue";
import Buefy from "buefy";
import "buefy/dist/buefy.css";

import moment from "moment";
import { mintcream } from "color-name";

Vue.use(Buefy);

export default {
  data: function() {
    return {
      todayDate: new Date().toISOString().substring(0, 10),

      state: this.$store.state,
      stayNoPrint: false,
      cateringNoPrint: false
    };
  },
  computed: {
    extraHours: function() {
      var arrivalDatetime = moment(this.state.stay.arrivalDatetime);
      var departureDatetime = moment(this.state.stay.departureDatetime);
      var minArrivalDatetime = arrivalDatetime.clone().set({
        hour: 17,
        minute: 0,
        second: 0,
        millisecond: 0
      });
      var maxDepartureDatetime = departureDatetime.clone().set({
        hour: 14,
        minute: 0,
        second: 0,
        millisecond: 0
      });
      var extraHours = 0;
      var arrivalExtraHours = minArrivalDatetime.diff(arrivalDatetime, "hours");
      var departureExtraHours = departureDatetime.diff(
        maxDepartureDatetime,
        "hours"
      );
      if (arrivalExtraHours > 0) {
        extraHours += arrivalExtraHours;
      }

      if (departureExtraHours > 0) {
        extraHours += departureExtraHours;
      }
      return extraHours;
    },
    staySubtotal: function() {
      if (this.stayNoPrint === true) {
        return 0;
      }

      var state = this.state;
      var invoiceData = this.invoiceData;

      var villaTotal = invoiceData.villaNights * state.prices.villaNight;
      var stayNightsTotal = 0;
      state.stay.stayNightArray.forEach(function(night, index) {
        stayNightsTotal += night.guests * state.prices.stayNight;
      });

      var petsTotal =
        state.stay.pets * invoiceData.villaNights * state.prices.petNight;
      var extraHoursTotal = invoiceData.extraHours * state.prices.extraHour;

      return villaTotal + stayNightsTotal + petsTotal + extraHoursTotal;
    },
    cateringSubtotal: function() {
      if (this.cateringNoPrint === true) {
        return 0;
      }
      var state = this.state;
      var cateringSubtotal = 0;
      state.meals.forEach(function(meal, index) {
        cateringSubtotal += meal.adults * meal.adultPrice;
        cateringSubtotal += meal.children * meal.childPrice;
      });

      return cateringSubtotal;
    },
    invoiceTotal: function() {
      var state = this.state;
      var invoiceData = this.invoiceData;

      var invoiceTotal =
        this.staySubtotal * (1 - invoiceData.discount) +
        invoiceData.taxedNights * state.prices.taxeSejourNight +
        this.cateringSubtotal;

      state.booking.costs.forEach(function(cost, index) {
        cost.type === "payment"
          ? (invoiceTotal -= cost.totalPrice)
          : (invoiceTotal += cost.totalPrice);
      });
      return invoiceTotal;
    },

    invoiceData: function() {
      var state = this.state;
      var stayNightArray = state.stay.stayNightArray;
      var externalVillaNights = 0;
      var villaNights = 0;
      var taxedNights = 0;
      stayNightArray.forEach(function(night) {
        if (!night.external) {
          villaNights += 1;
        } else {
          externalVillaNights += 1;
        }
        taxedNights += night.guests;
      });
      return {
        villaNights: villaNights,
        externalVillaNights: externalVillaNights,
        stayNightArray: state.stay.stayNightArray,
        taxedNights: taxedNights,
        extraHours: this.extraHours,
        discount: state.discountPerNight.hasOwnProperty(
          state.stay.stayNightArray.length
        )
          ? state.discountPerNight[state.stay.stayNightArray.length]
          : 0.15
      };
    }
  },
  methods: {
    hoursDifference: function(startDatetime, endDatetime) {
      var duration = moment.duration(endDatetime.diff(startDatetime));
      var hours = duration.asHours();
      return hours;
    },

    getDepositIcon: function(depositType) {
      if (depositType === "cheque") {
        return "money-check-alt";
      } else if (depositType === "cash") {
        return "money-bill-wave";
      } else if (depositType === "transfer") {
        return "exchange-alt";
      } else {
        return "money-check-alt";
      }
    },
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
    },
    humanFormatDate: function(date) {
      return moment(date).format("ddd D MMM YYYY");
    },
    humanFormatTime: function(date) {
      return moment(date).format("HH:mm");
    },
    humanInvoiceDate: function(unixDate, format) {
      if (format === "unix") {
        return moment.unix(unixDate).format("ddd. D MMM.");
      } else {
        return moment(unixDate).format("ddd. D MMM.");
      }
    }
  },
  mounted() {
    if (localStorage.getItem("state")) {
      this.state = JSON.parse(localStorage.getItem("state"));
    } else {
      this.state = this.$store.state;
    }
    if (localStorage.getItem("stayNoPrint")) {
      this.stayNoPrint = JSON.parse(localStorage.getItem("stayNoPrint"));
    } else {
      this.stayNoPrint = false;
    }
    if (localStorage.getItem("cateringNoPrint")) {
      this.cateringNoPrint = JSON.parse(
        localStorage.getItem("cateringNoPrint")
      );
    } else {
      this.cateringNoPrint = false;
    }
  }
};
</script>

<style scoped>
.flex-container {
  display: flex;
  height: 100vh;
  flex-direction: column;
  flex-wrap: nowrap;
  justify-content: space-between;
  padding: 10mm;
}
.flex-container > div {
  /* border: dashed grey; */
}

.sheet {
  size: A4;
  margin: 0;
  overflow: hidden;
  position: relative;
  box-sizing: border-box;
  page-break-after: always;
}

/** Paper sizes **/
.A4 .sheet {
  width: 210mm;
  height: 296mm;
}
.A4.landscape .sheet {
  width: 297mm;
  height: 209mm;
}

/** Padding area **/
.padding-10mm {
  padding: 10mm;
}
.padding-15mm {
  padding: 15mm;
}
.padding-20mm {
  padding: 20mm;
}
.padding-25mm {
  padding: 25mm;
}

/** For screen preview **/
@media screen {
  .sheet {
    background: white;
    box-shadow: 0 0.5mm 2mm rgba(0, 0, 0, 0.3);
    margin: 5mm auto;
    transform: scale(1);
  }
  .stretchy-wrapper {
    width: 100%;
    padding-bottom: 141.4%; /* A4 */
    position: relative;
    background: white;
  }
  .stretchy-wrapper > div {
    position: relative;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
  }
}

* {
  -webkit-print-color-adjust: exact;
}

@media print {
  .A4.landscape {
    width: 297mm;
  }
  .A4 {
    width: 210mm;
  }
}

@page {
  margin: 0;
  size: A4;
}
</style>