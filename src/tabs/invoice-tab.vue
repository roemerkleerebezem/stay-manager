<template>
  <!-- FORM -->
  <section class="section" style="height:100%">
    <div class="container">
      <!-- FORM TITLE -->
      <div class="box">
        <b-field grouped>
          <h3 class="title is-3 control">Facture n°</h3>

          <!-- INVOICE NUMBER -->
          <b-numberinput
            icon-pack="fas"
            v-model="booking.invoiceNumber"
            min="0"
            :controls="false"
            style="width:3rem;"
          ></b-numberinput>
        </b-field>
      </div>

      <div class="box">
        <!-- INVOICE -->

        <!-- DEPOSITS, TRANSACTIONS, COSTS -->
        <div class="subsection-header has-background-light">
          <h5 class="is-size-5 subtitle has-text-dark has-text-weight-medium">
            Cautions & transactions
          </h5>
        </div>
        <div class="subsection">
          <label class="label">Caution</label>

          <!-- DEPOSIT LIST -->
          <div
            class="container"
            style="margin-bottom:1rem;"
            v-for="deposit in booking.deposits"
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
                  <span class="has-text-grey">{{ deposit.type }} -</span>
                  {{ deposit.amount }} euros
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
                      : deposit.dateReceived.toString().substring(0, 10) + ", "
                  }}
                  {{ deposit.status }}
                </span>
                <div class="buttons">
                  <b-button
                    icon-pack="fas"
                    icon-left="pencil-alt"
                    type="is-dark"
                    @click="editDeposit(deposit)"
                  >
                  </b-button>
                  <b-button
                    icon-pack="fas"
                    type=" is-danger"
                    icon-left="trash"
                    @click="
                      $delete(
                        booking.deposits,
                        booking.deposits.indexOf(deposit)
                      )
                    "
                  >
                  </b-button>
                </div>
              </div>
            </article>
          </div>

          <!-- ADD DEPOSIT -->
          <div class="container">
            <b-button @click="isDepositModalActive = true"
              >Ajouter caution</b-button
            >

            <b-modal
              :active.sync="isDepositModalActive"
              has-modal-card
              :destroy-on-hide="false"
              width="50%"
              trap-focus
              scroll="keep"
            >
              <div class="modal-card">
                <header class="modal-card-head">
                  <p class="modal-card-title">Ajouter caution</p>
                  <button
                    type="button"
                    class="delete"
                    @click="isDepositModalActive = false"
                  />
                </header>
                <section class="modal-card-body">
                  <b-field label="Type" label-position="on-border">
                    <b-select
                      v-model="tempDeposit.type"
                      placeholder="Select a type"
                    >
                      <option value="cheque">Cheque</option>
                      <option value="transfer">Virement</option>
                      <option value="cash">Liquide</option>
                    </b-select>
                  </b-field>
                  <b-field label="Statut" label-position="on-border">
                    <b-select
                      v-model="tempDeposit.status"
                      placeholder="Select a status"
                    >
                      <option value="pending">En attente</option>
                      <option value="received">Recu</option>
                      <option value="returned">Rendu</option>
                    </b-select>
                  </b-field>
                  <b-field label="Montant" label-position="on-border">
                    <b-input
                      v-model="tempDeposit.amount"
                      placeholder="300"
                    ></b-input>
                  </b-field>
                  <b-field label="Date reception" label-position="on-border">
                    <b-datepicker
                      inline
                      :first-day-of-week="1"
                      icon-pack="fas"
                      v-model="tempDeposit.dateReceived"
                      placeholder="Date de reception"
                    ></b-datepicker>
                  </b-field>
                </section>
                <footer class="modal-card-foot">
                  <b-button
                    :disabled="canAddDeposit == false"
                    type="is-primary"
                    @click="addDeposit()"
                    >Ajouter</b-button
                  >
                </footer>
              </div>
            </b-modal>
          </div>
          <div class="container">
            <hr />

            <!-- EXTRA TRANSACTIONS -->
            <label class="label">Transactions supplémentaires</label>

            <!-- TRANSACTION LIST -->
            <div
              class="container"
              style="margin-bottom:1rem;"
              v-for="cost in booking.costs"
              :key="cost.id"
            >
              <article class="message is-light">
                <div class="message-header">
                  <p>
                    <b-icon
                      style="margin-right:0.5ch;display: inline-table;"
                      pack="fas"
                      :icon="cost.type === 'cost' ? 'arrow-down' : 'arrow-up'"
                      size="is-medium"
                      type="is-grey"
                    ></b-icon>
                    {{ cost.label }}
                    <span class="has-text-grey"
                      >{{ cost.units }} x {{ cost.unitPrice }} €</span
                    >
                  </p>
                  <span
                    :class="
                      'tag ' +
                        (cost.type === 'cost' ? 'is-danger' : 'is-success')
                    "
                  >
                    {{ cost.type === "cost" ? "-" : "+" }}
                    {{ cost.totalPrice }} €
                  </span>
                  <div class="buttons">
                    <b-button
                      icon-pack="fas"
                      icon-left="pencil-alt"
                      type="is-dark"
                      @click="editCost(cost)"
                    >
                    </b-button>
                    <b-button
                      icon-pack="fas"
                      type=" is-danger"
                      icon-left="trash"
                      @click="
                        $delete(booking.costs, booking.costs.indexOf(cost))
                      "
                    >
                    </b-button>
                  </div>
                </div>
              </article>
            </div>

            <!-- ADD TRANSACTION -->
            <b-button @click="isTransactionModalActive = true"
              >Add transaction</b-button
            >

            <b-modal
              :active.sync="isTransactionModalActive"
              has-modal-card
              :destroy-on-hide="false"
              width="50%"
              trap-focus
              scroll="keep"
            >
              <div class="modal-card">
                <header class="modal-card-head">
                  <p class="modal-card-title">Add transaction</p>
                  <button
                    type="button"
                    class="delete"
                    @click="isTransactionModalActive = false"
                  />
                </header>
                <section class="modal-card-body">
                  <b-field label="Type" label-position="on-border">
                    <b-select v-model="tempCost.type" placeholder="Type">
                      <option value="payment">Crédit (+)</option>
                      <option value="cost">Débit (-)</option>
                      <option value="payment-bank"
                        >Paiement via banque (+)</option
                      >
                      <option value="payment-cash"
                        >Paiement par liquide (+)</option
                      >
                    </b-select>
                  </b-field>
                  <b-field label="Label" label-position="on-border">
                    <b-input
                      v-model="tempCost.label"
                      placeholder="Virement"
                    ></b-input>
                  </b-field>
                  <b-field label="Unités" label-position="on-border">
                    <b-input v-model="tempCost.units"></b-input>
                  </b-field>
                  <b-field label="Prix unitaire" label-position="on-border">
                    <b-input v-model="tempCost.unitPrice"></b-input>
                  </b-field>
                  <b-field label="Total" label-position="on-border">
                    <b-numberinput
                      :controls="false"
                      icon-pack="fas"
                      controls-position="compact"
                      step="0.01"
                      placeholder="450"
                      v-model="tempCost.totalPrice"
                    ></b-numberinput>
                  </b-field>
                </section>
                <footer class="modal-card-foot">
                  <b-button
                    :disabled="this.canAddTransaction == false"
                    type="is-primary"
                    @click="addCost()"
                    >Ajouter</b-button
                  >
                </footer>
              </div>
            </b-modal>

            <hr />

            <!-- INTERNAL COSTS -->
            <label class="label">Coût interne</label>

            <!-- INTERNAL COSTS LIST -->
            <div
              class="container"
              style="margin-bottom:1rem;"
              v-for="cost in booking.internalCosts"
              :key="cost.id"
            >
              <article class="message is-light">
                <div class="message-header">
                  <p>
                    <b-icon
                      style="margin-right:0.5ch;display: inline-table;"
                      pack="fas"
                      icon="arrow-down"
                      size="is-medium"
                      type="is-grey"
                    ></b-icon>
                    {{ cost.label }}
                  </p>
                  <span
                    class="is-danger
                    "
                  >
                    {{ cost.totalPrice }} €
                  </span>
                  <div class="buttons">
                    <b-button
                      icon-pack="fas"
                      icon-left="pencil-alt"
                      type="is-dark"
                      @click="editInternalCost(cost)"
                    >
                    </b-button>
                    <b-button
                      icon-pack="fas"
                      type=" is-danger"
                      icon-left="trash"
                      @click="
                        $delete(
                          booking.internalCosts,
                          booking.internalCosts.indexOf(cost)
                        )
                      "
                    >
                    </b-button>
                  </div>
                </div>
              </article>
            </div>

            <!-- ADD INTERNAL COSTS -->
            <b-button @click="isInternalCostModalActive = true"
              >Ajouter coût interne</b-button
            >

            <b-modal
              :active.sync="isInternalCostModalActive"
              has-modal-card
              :destroy-on-hide="false"
              width="50%"
              trap-focus
              scroll="keep"
            >
              <div class="modal-card">
                <header class="modal-card-head">
                  <p class="modal-card-title">Ajouter coût interne</p>
                  <button
                    type="button"
                    class="delete"
                    @click="isInternalCostModalActive = false"
                  />
                </header>
                <section class="modal-card-body">
                  <b-field label="Label" label-position="on-border">
                    <b-input
                      v-model="tempInternalCost.label"
                      placeholder="Ménage"
                    ></b-input>
                  </b-field>
                  <b-field label="Total" label-position="on-border">
                    <b-numberinput
                      :controls="false"
                      icon-pack="fas"
                      controls-position="compact"
                      step="0.01"
                      placeholder="25"
                      v-model="tempInternalCost.totalPrice"
                    ></b-numberinput>
                  </b-field>
                </section>
                <footer class="modal-card-foot">
                  <b-button
                    :disabled="!this.canAddInternalCost"
                    type="is-primary"
                    @click="addInternalCost()"
                    >Ajouter</b-button
                  >
                </footer>
              </div>
            </b-modal>

            <div class="block"></div>
            <br />
          </div>
        </div>

        <!-- INVOICE -->
        <div class="subsection-header has-background-light">
          <h5 class="is-size-5 subtitle has-text-black has-text-weight-medium">
            Edit invoice
          </h5>
        </div>
        <div class="subsection">
          <!-- EXTRA INVOICE -->
          <label class="label">Invoices</label>

          <!-- INVOICE LIST -->
          <div
            class="container"
            style="margin-bottom:1rem;"
            v-for="invoice in invoices"
            :key="invoice.meta.uuid"
          >
            <article class="message is-dark">
              <div class="message-header">
                <p>
                  {{ invoice.main.status }} -
                  {{ formatDate(invoice.meta.creationDate, "ddmmyyyy") }}
                  <span class="has-text-grey">
                    - {{ invoice.main.value }} €</span
                  >
                </p>
                <div>
                  <b-button
                    type=""
                    @click="getInvoice(state, 'save', invoice.meta.uuid)"
                  >
                    REFRESH</b-button
                  >
                  <b-button type="" @click="viewInvoice(invoice)">
                    VIEW</b-button
                  >
                  <b-button
                    type="is-warning"
                    @click="getInvoice(state, 'print', invoice.meta.uuid)"
                  >
                    PRINT</b-button
                  >
                </div>
                <button
                  @click="$delete(invoices, invoices.indexOf(invoice))"
                  class="delete"
                ></button>
              </div>
              <div class="message-body">
                <!-- DATES -->
                <div class="block">
                  <div class="field is-grouped is-grouped-multiline">
                    <div class="control">
                      <div class="tags has-addons">
                        <span class="tag is-dark is-small">Check-in</span>
                        <span class="tag is-light is-small">
                          {{ formatDate(invoice.stay.arrivalDate, "human") }}
                          <b-icon
                            style="margin-left:0.5ch;margin-right:0.5ch;"
                            pack="fas"
                            icon="clock"
                            size="is-small"
                          ></b-icon>
                          {{ humanFormatTime(invoice.stay.arrivalTime) }}
                        </span>
                      </div>
                    </div>
                    <div class="control">
                      <div class="tags has-addons">
                        <span class="tag is-dark is-small">Check-out</span>
                        <span class="tag is-light is-small">
                          {{ formatDate(invoice.stay.departureDate, "human") }}
                          <b-icon
                            style="margin-left:0.5ch;margin-right:0.5ch;"
                            pack="fas"
                            icon="clock"
                            size="is-small"
                          ></b-icon>
                          {{ humanFormatTime(invoice.stay.departureTime) }}
                        </span>
                      </div>
                    </div>
                    <div class="control">
                      <span class="tag is-dark is-small"
                        >{{ invoice.stay.guestAmount.min }}-{{
                          invoice.stay.guestAmount.max
                        }}
                        personnes</span
                      >
                    </div>
                  </div>
                </div>

                <!-- INVOICE MAIN TABLE -->
                <table class="table is-fullwidth is-bordered">
                  <thead>
                    <tr class="has-background-light">
                      <th>Produit</th>
                      <th>Total</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="invoice.stay.total !== 0">
                      <td>Total sejour</td>
                      <td>
                        {{ invoice.stay.total }}
                        €
                      </td>
                    </tr>

                    <!-- MEALS -->
                    <tr v-if="invoice.meals.total !== 0">
                      <td>Total restauration</td>
                      <td>{{ invoice.meals.total }} €</td>
                    </tr>
                  </tbody>

                  <!-- COSTS -->
                  <tbody v-for="cost in invoice.main.costs" :key="cost.id">
                    <tr>
                      <td>
                        {{ cost.label }}
                        <span
                          v-if="
                            (cost.units !== null) & (cost.unitPrice !== null)
                          "
                          class="has-text-grey"
                          style="margin-left:1rem;"
                          >{{ cost.units }} x {{ cost.unitPrice }} €</span
                        >
                      </td>
                      <td>{{ cost.totalPrice }} €</td>
                    </tr>
                  </tbody>

                  <!-- DISCOUNTS -->
                  <tbody
                    v-for="discount in invoice.main.discounts"
                    :key="discount.id"
                  >
                    <tr class="has-text-success has-text-weight-semibold">
                      <td>
                        {{ discount.label }}
                        <span
                          v-if="
                            (discount.units !== null) &
                              (discount.unitPrice !== null)
                          "
                          class="has-text-grey"
                          style="margin-left:1rem;"
                          >{{ discount.units }} x
                          {{ discount.unitPrice }} €</span
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

                      <td
                        class="has-text-darkgrey is-uppercase has-text-weight-bold"
                      >
                        {{ invoice.main.total }}
                        €
                      </td>
                    </tr>
                  </tbody>

                  <!-- PAYMENTS -->
                  <tbody
                    v-for="transaction in invoice.main.transactions"
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
                      <td class="has-text-success has-text-weight-semibold">
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
                        {{ invoice.main.toPay }} €
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </article>
          </div>

          <!-- ADD INVOICE -->
          <b-button @click="isNewInvoiceModalActive = true"
            >Add Invoice</b-button
          >

          <b-modal
            :active.sync="isNewInvoiceModalActive"
            has-modal-card
            :destroy-on-hide="false"
            width="50%"
            trap-focus
            scroll="keep"
          >
            <div class="modal-card">
              <header class="modal-card-head">
                <p class="modal-card-title">Add invoice</p>
                <button
                  type="button"
                  class="delete"
                  @click="isNewInvoiceModalActive = false"
                />
              </header>
              <section class="modal-card-body">
                <div class="block">
                  <b-field label="Creation date" label-position="on-border">
                    <b-datepicker
                      :first-day-of-week="1"
                      inline
                      icon-pack="fas"
                      v-model="tempCreationDate"
                      placeholder="Creation date"
                    ></b-datepicker>
                  </b-field>
                </div>

                <!-- INVOICE OPTIONS -->
                <b-field>
                  <b-checkbox-button
                    v-model="tempInvoice.meta.stayNoPrint"
                    type="is-success"
                  >
                    <b-icon pack="fas" icon="bed" size="is-small"></b-icon>
                    <span>Stay</span>
                  </b-checkbox-button>

                  <b-checkbox-button
                    v-model="tempInvoice.meta.cateringNoPrint"
                    type="is-success"
                  >
                    <b-icon pack="fas" icon="utensils" size="is-small"></b-icon>
                    <span>Catering</span>
                  </b-checkbox-button>

                  <b-checkbox-button
                    v-model="tempInvoice.meta.contractNoPrint"
                    type="is-success"
                  >
                    <b-icon pack="fas" icon="file" size="is-small"></b-icon>
                    <span>Contract</span>
                  </b-checkbox-button>
                </b-field>
              </section>
              <footer class="modal-card-foot">
                <div class="block">
                  <button
                    class="button is-primary"
                    @click="getInvoice(state, 'view')"
                  >
                    <b-icon pack="fas" icon="eye" size="is-small"></b-icon>
                    <span>Check invoice</span>
                  </button>

                  <button
                    class="button is-primary"
                    @click="getInvoice(state, 'save')"
                  >
                    <b-icon pack="fas" icon="save" size="is-small"></b-icon>
                    <span>New invoice</span>
                  </button>
                </div>
              </footer>
            </div>
          </b-modal>

          <div class="block"></div>
          <br />
        </div>

        <b-modal
          :active.sync="isInvoiceModalActive"
          trap-focus
          width="50%"
          style="height:100%;"
        >
          <htmlinvoice></htmlinvoice>
        </b-modal>
      </div>
    </div>
  </section>
</template>

<script>
import Vue from "vue";
import htmlinvoice from "@/htmlinvoice.vue";

import fs from "fs";

import axios from "axios";
import moment from "moment";

export default {
  components: { htmlinvoice },

  data() {
    return {
      editMode: false,
      isDepositModalActive: false,
      isInvoiceModalActive: false,
      isNewInvoiceModalActive: false,
      currentInvoiceUuid: null,
      isTransactionModalActive: false,
      isInternalCostModalActive: false,
      booking: this.$store.state.booking,
      invoices: this.$store.state.invoices,
      state: this.$store.state,
      tempDeposit: {
        id: null,
        status: null,
        type: null,
        amount: null,
        dateReceived: null,
      },
      tempCost: {
        id: null,
        type: null,
        label: null,
        units: null,
        unitPrice: null,
        totalPrice: null,
      },
      tempInternalCost: {
        id: null,
        label: null,
        totalPrice: null,
      },
      tempInvoice: {
        meta: {
          uuid: null,
          lastModificationDate: null,
          creationDate: null,
          cateringNoPrint: !this.$store.state.settings.invoiceData.print
            .catering,
          stayNoPrint: !this.$store.state.settings.invoiceData.print.stay,
          contractNoPrint: !this.$store.state.settings.invoiceData.print
            .contract,
          invoiceNumber: this.$store.state.booking.invoiceNumber,
        },
      },
      tempCreationDate: moment().toDate(),
    };
  },
  computed: {
    canAddDeposit() {
      if (
        this.isEmpty(this.tempDeposit.status) |
        this.isEmpty(this.tempDeposit.type) |
        this.isEmpty(this.tempDeposit.amount)
      ) {
        return false;
      } else {
        return true;
      }
    },
    canAddTransaction() {
      if (
        this.isEmpty(this.tempCost.type) |
        this.isEmpty(this.tempCost.label) |
        isNaN(this.tempCost.totalPrice) |
        this.isEmpty(this.tempCost.totalPrice)
      ) {
        return false;
      } else {
        return true;
      }
    },
    canAddInternalCost() {
      if (
        this.isEmpty(this.tempInternalCost.label) |
        isNaN(this.tempInternalCost.totalPrice) |
        this.isEmpty(this.tempInternalCost.totalPrice)
      ) {
        return false;
      } else {
        return true;
      }
    },
  },
  watch: {},
  mounted: function() {},
  methods: {
    isEmpty: function(formInput) {
      if ((formInput === null) | (formInput === "")) {
        return true;
      } else {
        return false;
      }
    },
    formatDate: function(date, format) {
      if (format == "human") {
        return moment(date).format("ddd D MMM YYYY");
      } else if (format == "ddmmyyyy") {
        return moment.unix(date).format("DD/MM/YYYY");
      }
    },
    humanFormatTime: function(date) {
      return moment(date).format("HH:mm");
    },
    uuidv4: function() {
      return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function(
        c
      ) {
        var r = (Math.random() * 16) | 0,
          v = c == "x" ? r : (r & 0x3) | 0x8;
        return v.toString(16);
      });
    },

    openModal() {
      this.$buefy.modal.open({
        parent: this,
        component: htmlInvoice,
        hasModalCard: false,
      });
    },

    addDeposit: function() {
      var tempDeposit = this.tempDeposit;
      var tempDeposits = this.booking.deposits;
      if (tempDeposits.find((x) => x.id === tempDeposit.id)) {
        Vue.delete(
          this.booking.deposits,
          this.booking.deposits.findIndex((d) => d.id == tempDeposit.id)
        );
      } else {
        tempDeposit.id = this.uuidv4();
      }
      tempDeposits.push(tempDeposit);

      Vue.set(
        this.booking,
        "deposits",
        JSON.parse(JSON.stringify(tempDeposits))
      );
      this.isDepositModalActive = false;
      this.tempDeposit = {
        id: null,
        status: null,
        type: null,
        amount: null,
        dateReceived: null,
      };
    },
    editDeposit: function(deposit) {
      var dep = JSON.parse(JSON.stringify(deposit));
      if (dep.dateReceived) {
        dep.dateReceived = moment(deposit.dateReceived).toDate();
      }

      this.tempDeposit = dep;

      this.isDepositModalActive = true;
    },
    getInvoice: async function(state, action, uuid) {
      const headers = {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json",
      };

      var tempCreationDate = this.tempCreationDate;

      var localState = state;

      var tempInvoice = JSON.parse(JSON.stringify(this.tempInvoice));

      var invoices = localState.invoices;

      if (!!uuid) {
        tempInvoice.meta.uuid = uuid;
        tempInvoice = invoices.find((x) => x.meta.uuid === uuid);
      } else {
        tempInvoice.meta.creationDate = moment(tempCreationDate).unix();
        tempInvoice.meta.lastModificationDate = moment(tempCreationDate).unix();
      }

      if (action == "print") {
        localStorage.setItem("tempInvoice", JSON.stringify(tempInvoice));
        this.printInvoice();
        return 0;
      }

      var request = {};
      request["action"] = "get-invoice";
      request["data"] = localState;
      request["invoice"] = tempInvoice;

      var ApiInvoice = await axios({
        method: "post",
        url: "/api",
        headers: headers,
        data: request,
      })
        .then(function(response) {
          return response.data;
        })
        .catch(function(error) {
          console.log(error);
        });

      if (action == "save") {
        this.$store.commit("updateInvoice", ApiInvoice);
        this.isNewInvoiceModalActive = false;
      }
      localStorage.setItem("tempInvoice", JSON.stringify(ApiInvoice));

      if (action == "view") {
        this.isInvoiceModalActive = true;
      }
      this.$forceUpdate();

      return ApiInvoice;
    },
    viewInvoice: function(invoice) {
      localStorage.setItem("tempInvoice", JSON.stringify(invoice));
      this.isInvoiceModalActive = true;
      this.$forceUpdate();
    },

    printInvoice() {
      var printWindow = window.open("/htmlinvoice");
      printWindow.focus();
      printWindow.print();
    },

    addCost: function() {
      var tempCost = this.tempCost;
      var tempCosts = this.booking.costs;
      if (tempCosts.find((x) => x.id === tempCost.id)) {
        Vue.delete(
          this.booking.costs,
          this.booking.costs.findIndex((d) => d.id == tempCost.id)
        );
      } else {
        tempCost.id = this.uuidv4();
      }

      tempCosts.push(tempCost);

      this.isTransactionModalActive = false;

      Vue.set(this.booking, "costs", JSON.parse(JSON.stringify(tempCosts)));
      this.tempCost = {
        id: null,
        type: null,
        label: null,
        units: null,
        unitPrice: null,
        totalPrice: null,
      };
    },

    editCost: function(cost) {
      var editedCost = JSON.parse(JSON.stringify(cost));
      this.tempCost = editedCost;
      this.editMode = true;
      this.isTransactionModalActive = true;
    },

    addInternalCost: function() {
      var tempInternalCost = this.tempInternalCost;
      var tempInternalCosts = this.booking.internalCosts;

      if (tempInternalCosts.find((x) => x.id === tempInternalCost.id)) {
        Vue.delete(
          this.booking.internalCosts,
          this.booking.internalCosts.findIndex(
            (d) => d.id == tempInternalCost.id
          )
        );
      } else {
        tempInternalCost.id = this.uuidv4();
      }

      tempInternalCosts.push(tempInternalCost);

      this.isInternalCostModalActive = false;

      Vue.set(
        this.booking,
        "internalCosts",
        JSON.parse(JSON.stringify(tempInternalCosts))
      );
      this.tempInternalCost = {
        id: null,
        label: null,
        totalPrice: null,
      };
    },
    editInternalCost: function(internalCost) {
      var editedCost = JSON.parse(JSON.stringify(internalCost));
      this.tempInternalCost = editedCost;

      this.isInternalCostModalActive = true;
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
  },
};
</script>

<style scoped></style>
