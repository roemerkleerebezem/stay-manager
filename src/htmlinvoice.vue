<template>
  <div id="app">
    <link
      rel="stylesheet"
      href="https://use.fontawesome.com/releases/v5.2.0/css/all.css"
    />

    <!-- TOTAL INVOICE FLEX-->
    <div v-if="tempInvoice != null">
      <div class="A4 sheet stretchy-wrapper flex-container">
        <!-- HEADER -->
        <div class="header">
          <!-- INVOICE HEADER -->
          <div class="level">
            <div class="level-left">
              <div class="level-item">
                <div class="container">
                  <h4 class="title is-size-4 is-uppercase">
                    {{
                      tempInvoice.main.status === "completed"
                        ? "Facture " + tempInvoice.meta.invoiceIndex
                        : "Réservation"
                    }}
                  </h4>
                  <span
                    :class="
                      getStatusColor(tempInvoice.main.status) +
                        ' is-uppercase tag'
                    "
                    >{{ tempInvoice.main.status }}</span
                  >
                </div>
              </div>
            </div>
            <div class="level-right">
              <div class="level-item">
                <div class="container is-size-7 has-text-right">
                  <p>
                    {{ formatDate(tempInvoice.meta.creationDate, "ddmmyyyy") }}
                  </p>
                  <p>{{ tempInvoice.meta.creationCity }}</p>
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
                      <p>{{ tempInvoice.meta.host.name }}</p>
                      <p>{{ tempInvoice.meta.host.address1 }}</p>
                      <p>{{ tempInvoice.meta.host.address2 }}</p>
                      <p>{{ tempInvoice.meta.host.phone }}</p>
                      <p>{{ tempInvoice.meta.host.email }}</p>
                    </div>
                  </div>
                  <!-- CLIENT -->
                  <div class="column">
                    <div class="has-text-centered">
                      <h6 class="title is-6">CLIENT</h6>
                      <p>{{ tempInvoice.main.contact.name }}</p>
                      <br />
                      <br />
                      <p>{{ tempInvoice.main.contact.phone }}</p>
                      <p>{{ tempInvoice.main.contact.email }}</p>
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
              <tr v-if="tempInvoice.stay.total !== 0">
                <td>Total sejour</td>
                <td>
                  {{ tempInvoice.stay.total }}
                  €
                </td>
              </tr>

              <!-- MEALS -->
              <tr v-if="tempInvoice.meals.total !== 0">
                <td>Total restauration</td>
                <td>{{ tempInvoice.meals.total }} €</td>
              </tr>
            </tbody>

            <!-- COSTS -->
            <tbody v-for="cost in tempInvoice.main.costs" :key="cost.id">
              <tr>
                <td class="is-capitalized	">
                  {{ cost.label }}
                  <span
                    v-if="(cost.units !== null) & (cost.unitPrice !== null)"
                    class="has-text-grey "
                    style="margin-left:1rem;"
                    >{{ cost.units }} x {{ cost.unitPrice }} €</span
                  >
                </td>
                <td>{{ cost.totalPrice }} €</td>
              </tr>
            </tbody>

            <!-- DISCOUNTS -->
            <tbody
              v-for="discount in tempInvoice.main.discounts"
              :key="discount.id"
            >
              <tr class="has-text-success has-text-weight-semibold">
                <td class="is-capitalized	">
                  {{ discount.label }}
                  <span
                    v-if="
                      (discount.units !== null) & (discount.unitPrice !== null)
                    "
                    class="has-text-grey"
                    style="margin-left:1rem;"
                    >{{ discount.units }} x {{ discount.unitPrice }} €</span
                  >
                </td>
                <td>-{{ discount.totalPrice }} €</td>
              </tr>
            </tbody>

            <!-- SUBTOTAL -->
            <tbody>
              <tr class="has-background-light">
                <td
                  class="has-text-darkgrey is-uppercase has-text-weight-semibold"
                >
                  Sous-total
                </td>

                <td class="has-text-darkgrey is-uppercase has-text-weight-bold">
                  {{ tempInvoice.main.total }}
                  €
                </td>
              </tr>
            </tbody>

            <!-- PAYMENTS -->
            <tbody
              v-for="transaction in tempInvoice.main.transactions"
              :key="transaction.id"
            >
              <tr>
                <td
                  class="has-text-success has-text-weight-semibold 
                  "
                >
                  {{ transaction.label }}
                  <span
                    v-if="
                      (transaction.units !== null) &
                        (transaction.unitPrice !== null)
                    "
                    class="has-text-grey"
                    style="margin-left:1rem;"
                    >{{ transaction.units }} x
                    {{ transaction.unitPrice }} €</span
                  >
                </td>
                <td class="has-text-success has-text-weight-semibold ">
                  -{{ transaction.totalPrice }} €
                </td>
              </tr>
            </tbody>

            <tbody>
              <tr class="has-background-light">
                <td
                  class="has-text-darkgrey is-uppercase has-text-weight-semibold"
                >
                  Reste à payer
                </td>
                <td
                  class="has-text-darkgrey is-uppercase has-text-weight-semibold"
                >
                  {{ tempInvoice.main.toPay }} €
                </td>
              </tr>
            </tbody>
          </table>
          <p class="has-text-grey has-text-right pre-line">
            {{ tempInvoice.meta.mainTableFooter }}
          </p>
        </div>

        <!-- DEPOSIT -->
        <div v-if="tempInvoice.main.deposits.length > 0">
          <span class="is-size-5 title">Caution</span>

          <div
            class="container"
            style="margin-bottom:1rem;"
            v-for="deposit in tempInvoice.main.deposits"
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
                  <span class="has-text-grey is-uppercase"
                    >{{ deposit.type }} -</span
                  >
                  {{ deposit.amount }} €
                </p>

                <span
                  :class="
                    'tag is-medium ' +
                      (deposit.status === 'pending'
                        ? 'is-warning'
                        : 'is-success')
                  "
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

        <!-- IBAN -->
        <div class="has-text-grey has-text-right pre-line">
          {{ tempInvoice.meta.mainPageFooter }}
        </div>
      </div>

      <!-- STAY INVOICE FLEX-->
      <div
        v-if="
          (tempInvoice.stay.total > 0) |
            (tempInvoice.meta.stayNoPrint === false)
        "
        class="A4 sheet stretchy-wrapper flex-container"
      >
        <!-- HEADER -->
        <div class="header">
          <!-- INVOICE HEADER -->
          <div class="level">
            <div class="level-left">
              <div class="level-item">
                <div class="container">
                  <h4 class="title is-size-4 is-uppercase">
                    {{
                      tempInvoice.main.status === "completed"
                        ? "Facture " + tempInvoice.meta.invoiceIndex
                        : "Réservation"
                    }}
                    - DETAILS SEJOUR
                  </h4>
                </div>
              </div>
            </div>
            <div class="level-right">
              <div class="level-item">
                <div class="container is-size-7 has-text-right">
                  <p>
                    {{ formatDate(tempInvoice.meta.creationDate, "ddmmyyyy") }}
                  </p>
                  <p>{{ tempInvoice.meta.creationCity }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- DATES -->
          <div class="container">
            <div class="field is-grouped is-grouped-multiline">
              <div class="control">
                <div class="tags has-addons">
                  <span class="tag is-dark is-small">Check-in</span>
                  <span class="tag is-light is-small">
                    {{ formatDate(tempInvoice.stay.arrivalDate, "human") }}
                    <b-icon
                      style="margin-left:0.5ch;margin-right:0.5ch;"
                      pack="fas"
                      icon="clock"
                      size="is-small"
                    ></b-icon>
                    {{ humanFormatTime(tempInvoice.stay.arrivalTime) }}
                  </span>
                </div>
              </div>
              <div class="control">
                <div class="tags has-addons">
                  <span class="tag is-dark is-small">Check-out</span>
                  <span class="tag is-light is-small">
                    {{ formatDate(tempInvoice.stay.departureDate, "human") }}
                    <b-icon
                      style="margin-left:0.5ch;margin-right:0.5ch;"
                      pack="fas"
                      icon="clock"
                      size="is-small"
                    ></b-icon>
                    {{ humanFormatTime(tempInvoice.stay.departureTime) }}
                  </span>
                </div>
              </div>

              <!-- GUEST RANGE -->
              <div class="control">
                <span
                  v-if="
                    tempInvoice.stay.guestAmount.min !=
                      tempInvoice.stay.guestAmount.max
                  "
                  class="tag is-dark is-small"
                >
                  {{ tempInvoice.stay.guestAmount.min }}-{{
                    tempInvoice.stay.guestAmount.max
                  }}
                  personnes</span
                >
                <span
                  v-if="
                    tempInvoice.stay.guestAmount.min ==
                      tempInvoice.stay.guestAmount.max
                  "
                  class="tag is-dark is-small"
                >
                  {{ tempInvoice.stay.guestAmount.max }}
                  personnes</span
                >
              </div>
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
                    <p class="pre-line">
                      {{ tempInvoice.meta.property.description }}
                    </p>
                  </div>
                  <div class="column">
                    <img src="./assets/mill_sketch.jpg" />
                  </div>

                  <!-- HOST -->
                  <div class="column">
                    <div class="is-pulled-right">
                      <h6 class="title is-6">Adresse</h6>
                      <p class="pre-line">
                        {{ tempInvoice.meta.property.address }}
                      </p>
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
            <!-- VILLA -->
            <tr
              v-if="tempInvoice.stay.villa.external.units > 0"
              class="has-text-weight-light"
            >
              <td>Villa (payé)</td>
              <td>{{ tempInvoice.stay.villa.external.units }} nuit(s)</td>
              <td>{{ tempInvoice.stay.villa.external.price }} €</td>
              <td>{{ tempInvoice.stay.villa.external.total }} €</td>
            </tr>
            <tr v-if="tempInvoice.stay.villa.internal.units > 0">
              <td>Villa</td>
              <td>{{ tempInvoice.stay.villa.internal.units }} nuit(s)</td>
              <td>{{ tempInvoice.stay.villa.internal.price }} €</td>
              <td>{{ tempInvoice.stay.villa.internal.total }} €</td>
            </tr>
          </tbody>
          <!-- GUESTS -->
          <tbody
            v-for="night in tempInvoice.stay.guests"
            :key="night.internal.date"
          >
            <tr v-if="night.external.units > 0" class="has-text-weight-light">
              <td>
                Couchages
                {{ humanInvoiceDate(night.external.date, "unix") }} (payé)
              </td>
              <td>{{ night.external.units }}</td>
              <td>{{ night.external.price }} €</td>
              <td>{{ night.external.total }} €</td>
            </tr>
            <tr v-if="night.internal.units > 0">
              <td>
                Couchages
                {{
                  night.external.units > 0
                    ? "supplémentaires " +
                      humanInvoiceDate(night.internal.date, "unix")
                    : humanInvoiceDate(night.internal.date, "unix")
                }}
              </td>
              <td>{{ night.internal.units }}</td>
              <td>{{ night.internal.price }} €</td>
              <td>{{ night.internal.total }} €</td>
            </tr>
          </tbody>
          <tbody>
            <tr v-if="tempInvoice.stay.pets.units > 0">
              <td>Animaux de compagnie</td>
              <td>{{ tempInvoice.stay.pets.units }} nuit(s)</td>
              <td>{{ tempInvoice.stay.pets.price }} €</td>
              <td>
                {{ tempInvoice.stay.pets.total }}
                €
              </td>
            </tr>
            <tr class="has-background-light">
              <td
                class="has-text-darkgrey is-uppercase has-text-weight-semibold"
              >
                Sous-total
              </td>
              <td></td>
              <td></td>
              <td
                class="has-text-darkgrey is-uppercase has-text-weight-semibold"
              >
                {{ tempInvoice.stay.totalBeforeDiscount }} €
              </td>
            </tr>
            <tr v-if="tempInvoice.stay.discount.total > 0">
              <td>
                Réduction {{ tempInvoice.stay.discount.nights }} nuits ({{
                  Math.round(100 * tempInvoice.stay.discount.percentage)
                }}%)
              </td>
              <td></td>
              <td></td>
              <td class="has-text-success has-text-weight-semibold">
                -{{ tempInvoice.stay.discount.total }} €
              </td>
            </tr>
            <tr v-if="tempInvoice.stay.extraHours.units > 0">
              <td>Heures supplémentaires</td>
              <td>{{ tempInvoice.stay.extraHours.units }}</td>
              <td>{{ tempInvoice.stay.extraHours.price }} €</td>
              <td>{{ tempInvoice.stay.extraHours.total }} €</td>
            </tr>
            <tr v-if="tempInvoice.stay.tax.total > 0">
              <td>
                Taxe de séjour
                <span class="has-text-grey has-text-weight-light"
                  >({{
                    (Math.round(tempInvoice.stay.tax.percentage * 1000) * 100) /
                      1000
                  }}
                  %)</span
                >
              </td>
              <td>{{ tempInvoice.stay.tax.units }}</td>
              <td>
                {{
                  Math.round(
                    (tempInvoice.stay.tax.total / tempInvoice.stay.tax.units) *
                      100
                  ) / 100
                }}
                €
              </td>
              <td>
                {{ tempInvoice.stay.tax.total }}
                €
              </td>
            </tr>
            <tr class="has-background-light">
              <td
                class="has-text-darkgrey is-uppercase has-text-weight-semibold"
              >
                Total séjour
              </td>
              <td></td>
              <td></td>
              <td class="has-text-darkgrey is-uppercase has-text-weight-bold">
                {{ tempInvoice.stay.total }}
                €
              </td>
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
        v-if="
          (tempInvoice.meals.total > 0) &
            (tempInvoice.meta.cateringNoPrint === false)
        "
        class="A4 sheet stretchy-wrapper flex-container"
      >
        <!-- HEADER -->
        <div class="header">
          <!-- INVOICE HEADER -->
          <div class="level">
            <div class="level-left">
              <div class="level-item">
                <div class="container">
                  <h4 class="title is-size-4 is-uppercase">
                    {{
                      tempInvoice.main.status === "completed"
                        ? "Facture " + tempInvoice.meta.invoiceIndex
                        : "Réservation"
                    }}
                    - DETAILS RESTAURATION
                  </h4>
                </div>
              </div>
            </div>
            <div class="level-right">
              <div class="level-item">
                <div class="container is-size-7 has-text-right">
                  <p>
                    {{ formatDate(tempInvoice.meta.creationDate, "ddmmyyyy") }}
                  </p>
                  <p>{{ tempInvoice.meta.creationCity }}</p>
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
            <tbody v-for="meal in tempInvoice.meals.meals" :key="meal.date">
              <tr v-if="meal.adults.units != 0">
                <td>
                  {{ cateringString[meal.type] }}
                  {{ humanInvoiceDate(meal.date) }}
                </td>
                <td>{{ meal.adults.units }} adultes</td>
                <td>{{ meal.adults.price }} €</td>
                <td>{{ meal.adults.total }} €</td>
              </tr>
              <tr v-if="meal.children.units != 0">
                <td>
                  {{ cateringString[meal.type] }}
                  {{ humanInvoiceDate(meal.date) }}
                </td>
                <td>{{ meal.children.units }} enfants</td>
                <td>{{ meal.children.price }} €</td>
                <td>{{ meal.children.total }} €</td>
              </tr>
            </tbody>
            <tbody>
              <tr>
                <td
                  class="has-text-darkgrey is-uppercase has-text-weight-semibold"
                >
                  Total restauration
                </td>
                <td></td>
                <td></td>
                <td class="has-text-darkgrey is-uppercase has-text-weight-bold">
                  {{ tempInvoice.meals.total }} €
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- FOOTER -->
        <div>
          <!-- <p class="is-pulled-right">Page 2/3</p> -->
        </div>
      </div>

      <!-- CONTRACT FLEX-->
      <div
        v-if="tempInvoice.meta.contractNoPrint === false"
        class="A4 sheet stretchy-wrapper flex-container"
      >
        <div>
          <!-- ADD CONTRACT -->
          <div class="contract-span" v-html="htmlContract"></div>
        </div>

        <!-- FOOTER -->
        <div>
          <!-- <p class="is-pulled-right">Page 2/3</p> -->
        </div>
      </div>

      <!-- V-IF tempInvoice exists -->
    </div>

    <!-- END -->
  </div>
</template>

<script>
import Vue from "vue";
import Buefy from "buefy";
import "buefy/dist/buefy.css";

import marked from "marked";

import moment from "moment";

import contract from "!raw-loader!@/assets/contract.md";

Vue.use(Buefy);

export default {
  data: function() {
    return {
      state: this.$store.state,
      htmlContract: marked(contract),

      tempInvoice: null,

      cateringString: {
        breakfast: "Petit-déjeuner",
        lunch: "Déjeuner",
        dinner: "Dîner",
      },
    };
  },
  computed: {},
  methods: {
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
    formatDate: function(date, format) {
      if (format == "human") {
        return moment(date)
          .locale("fr")
          .format("ddd D MMM YYYY");
      } else if (format == "ddmmyyyy") {
        return moment.unix(date).format("DD/MM/YYYY");
      }
    },
    humanFormatTime: function(date) {
      return moment(date).format("HH:mm");
    },
    humanInvoiceDate: function(unixDate, format) {
      if (format === "unix") {
        return moment
          .unix(unixDate)
          .locale("fr")
          .format("dddd D MMM");
      } else {
        return moment(unixDate)
          .locale("fr")
          .format("dddd D MMM");
      }
    },
  },
  mounted() {
    if (localStorage.getItem("state")) {
      this.state = JSON.parse(localStorage.getItem("state"));
    } else {
      this.state = this.$store.state;
    }
    if (localStorage.getItem("tempInvoice")) {
      this.tempInvoice = JSON.parse(localStorage.getItem("tempInvoice"));
    } else {
      console.log("ERROR : no tempInvoice to load");
      this.tempInvoice = null;
    }
  },
};
</script>

<style scoped>
.pre-line {
  white-space: pre-line;
}

.contract-span {
  font-size: 0.65em;
  white-space: pre-line;
}

.contract-span >>> h1 {
  font-size: 2em;
}

.flex-container {
  display: flex;
  height: 100vh;
  flex-direction: column;
  flex-wrap: nowrap;
  justify-content: space-between;
  padding: 10mm;
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
