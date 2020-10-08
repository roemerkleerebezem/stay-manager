<template>
  <!-- FORM -->
  <section class="section" style="height:100%">
    <div class="container">
      <div class="box">
        <!-- FORM TITLE -->
        <h3 class="title is-3">Facture</h3>

        <!-- PETS -->
        <b-field label="Invoice number">
          <b-numberinput
            icon-pack="fas"
            v-model="booking.invoiceNumber"
            min="0"
            controlsPosition="compact"
          ></b-numberinput>
        </b-field>

        <hr />

        <!-- DEPOSITS -->
        <label class="label">Deposit</label>

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
                    (deposit.status === 'pending' ? 'is-warning' : 'is-success')
                "
              >
                {{
                  deposit.dateReceived === null
                    ? ""
                    : deposit.dateReceived.substring(0, 10) + ", "
                }}
                {{ deposit.status }}
              </span>
              <button
                @click="
                  $delete(booking.deposits, booking.deposits.indexOf(deposit))
                "
                class="delete"
              ></button>
            </div>
          </article>
        </div>

        <!-- ADD DEPOSIT -->
        <div class="container">
          <b-button @click="isDepositModalActive = true">Add deposit</b-button>

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
                <p class="modal-card-title">Add deposit</p>
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
                <b-button type="is-primary" @click="addDeposit()"
                  >Ajouter</b-button
                >
              </footer>
            </div>
          </b-modal>

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
                    'tag ' + (cost.type === 'cost' ? 'is-danger' : 'is-success')
                  "
                >
                  {{ cost.type === "cost" ? "-" : "+" }}
                  {{ cost.totalPrice }} €
                </span>

                <button
                  @click="$delete(booking.costs, booking.costs.indexOf(cost))"
                  class="delete"
                ></button>
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
                <b-button type="is-primary" @click="addCost()"
                  >Ajouter</b-button
                >
              </footer>
            </div>
          </b-modal>

          <hr />

          <!-- INVOICE OPTIONS -->
          <b-field>
            <b-checkbox-button v-model="stayNoPrint" type="is-success">
              <b-icon pack="fas" icon="bed" size="is-small"></b-icon>
              <span>Stay</span>
            </b-checkbox-button>

            <b-checkbox-button v-model="cateringNoPrint" type="is-success">
              <b-icon pack="fas" icon="utensils" size="is-small"></b-icon>
              <span>Catering</span>
            </b-checkbox-button>

            <b-checkbox-button v-model="contractNoPrint" type="is-success">
              <b-icon pack="fas" icon="file" size="is-small"></b-icon>
              <span>Contract</span>
            </b-checkbox-button>
          </b-field>

          <hr />

          <!-- OPEN MODAL -->
          <div class="block">
            <button
              class="button is-primary"
              @click="isInvoiceModalActive = true"
            >
              <b-icon pack="fas" icon="eye" size="is-small"></b-icon>
              <span>Check invoice</span>
            </button>

            <button class="button is-primary" @click="printInvoice()">
              <b-icon pack="fas" icon="print" size="is-small"></b-icon>
              <span>Print Invoice</span>
            </button>
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
    </div>
  </section>
</template>

<script>
import Vue from "vue";
import htmlinvoice from "@/htmlinvoice.vue";

import fs from "fs";

export default {
  components: { htmlinvoice },

  data() {
    return {
      isDepositModalActive: false,
      isInvoiceModalActive: false,
      isTransactionModalActive: false,
      booking: this.$store.state.booking,
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
      cateringNoPrint: false,
      stayNoPrint: false,
      contractNoPrint: false,
    };
  },
  computed: {},
  watch: {
    cateringNoPrint: {
      handler() {
        localStorage.setItem("cateringNoPrint", this.cateringNoPrint);
      },
    },
    stayNoPrint: {
      handler() {
        localStorage.setItem("stayNoPrint", this.stayNoPrint);
      },
    },
    contractNoPrint: {
      handler() {
        localStorage.setItem("contractNoPrint", this.contractNoPrint);
      },
    },
  },
  mounted() {
    localStorage.setItem("cateringNoPrint", this.cateringNoPrint);
    localStorage.setItem("stayNoPrint", this.stayNoPrint);
    localStorage.setItem("contractNoPrint", this.contractNoPrint);
  },
  methods: {
    getId: function(object) {
      var arr = [];
      for (var obj in object) {
        arr.push(parseInt(obj));
      }
      return Math.max(-1, ...arr) + 1;
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
      tempDeposit.id = this.getId(tempDeposits);
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

    printInvoice() {
      var printWindow = window.open("/htmlinvoice");
      printWindow.focus();
      printWindow.print();
    },

    addCost: function() {
      var tempCost = this.tempCost;
      var tempCosts = this.booking.costs;
      tempCost.id = this.getId(tempCosts);
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
