<template>
  <!-- FORM -->
  <section class="section" style="height:100%">
    <div class="container">
      <div class="box">
        <!-- FORM TITLE -->
        <h3 class="title is-3">Facture</h3>
        <!-- DEPOSITS -->
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
              <button @click="$delete(booking.deposits, deposit.id)" class="delete"></button>
            </div>
          </article>
        </div>

        <!-- ADD DEPOSIT -->
        <div class="container">
          <b-field grouped group-multiline>
            <b-field label="Statut" label-position="on-border">
              <b-select v-model="tempDeposit.status" placeholder="Select a status">
                <option value="pending">En attente</option>
                <option value="received">Recu</option>
                <option value="returned">Rendu</option>
              </b-select>
            </b-field>
            <b-field label="Montant" label-position="on-border">
              <b-input v-model="tempDeposit.amount"></b-input>
            </b-field>
            <b-field label="Date reception" label-position="on-border">
              <b-datepicker
                icon-pack="fas"
                v-model="tempDeposit.dateReceived"
                placeholder="Date de reception"
              ></b-datepicker>
            </b-field>
            <b-field label="Type" label-position="on-border">
              <b-select v-model="tempDeposit.type" placeholder="Select a type">
                <option value="cheque">Cheque</option>
                <option value="transfer">Virement</option>
                <option value="cash">Liquide</option>
              </b-select>
            </b-field>
            <b-button type="is-primary" @click="addDeposit()">Ajouter</b-button>
          </b-field>

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
                    :icon="cost.type === 'payment' ? 'arrow-up' : 'arrow-down'"
                    size="is-medium"
                    type="is-grey"
                  ></b-icon>
                  {{ cost.label }}
                  <span
                    class="has-text-grey"
                  >{{ cost.units }} x {{ cost.unitPrice }} €</span>
                </p>
                <span
                  :class="
                    'tag ' +
                      (cost.type === 'payment' ? 'is-success' : 'is-danger')
                  "
                >
                  {{ cost.type === "payment" ? "+" : "-" }}
                  {{ cost.totalPrice }} €
                </span>

                <button @click="$delete(booking.costs, cost.id)" class="delete"></button>
              </div>
            </article>
          </div>

          <!-- ADD TRANSACTION -->
          <div class="container">
            <b-field grouped group-multiline>
              <b-field label="Type" label-position="on-border">
                <b-select v-model="tempCost.type" placeholder="Type">
                  <option value="payment">Paiement</option>
                  <option value="cost">Coût</option>
                </b-select>
              </b-field>
              <b-field label="Label" label-position="on-border">
                <b-input v-model="tempCost.label"></b-input>
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
                  v-model="tempCost.totalPrice"
                ></b-numberinput>
              </b-field>
              <b-button type="is-primary" @click="addCost()">Ajouter</b-button>
            </b-field>
          </div>

          <hr />

          <!-- OPEN MODAL -->
          <b-button type="is-primary" @click="isComponentModalActive = true">Open Modal</b-button>

          <b-button type="is-primary" @click="printInvoice()">Print Invoice</b-button>

          <b-modal
            :active.sync="isComponentModalActive"
            trap-focus
            width="90%"
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

export default {
  components: { htmlinvoice },

  data() {
    return {
      isComponentModalActive: false,
      booking: this.$store.state.booking,
      tempDeposit: {
        id: null,
        status: null,
        type: null,
        amount: null,
        dateReceived: null
      },
      tempCost: {
        id: null,
        type: null,
        label: null,
        units: null,
        unitPrice: null,
        totalPrice: null
      }
    };
  },
  computed: {},
  watch: {},

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
        hasModalCard: false
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
      this.tempDeposit = {
        id: null,
        status: null,
        type: null,
        amount: null,
        dateReceived: null
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

      Vue.set(this.booking, "costs", JSON.parse(JSON.stringify(tempCosts)));
      this.tempCost = {
        id: null,
        type: null,
        label: null,
        units: null,
        unitPrice: null,
        totalPrice: null
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
    }
  }
};
</script>

<style scoped></style>
