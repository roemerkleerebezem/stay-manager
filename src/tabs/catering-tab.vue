<template>
  <!-- FORM -->
  <section class="section">
    <div class="container">
      <!-- FORM TITLE -->
      <div class="box ">
        <h3 class="title is-3">Restauration</h3>
      </div>

      <!-- MEAL LIST -->
      <b-collapse
        class="card meal-card"
        v-for="meal in meals"
        :key="meal.id"
        :aria-id="'mealContent' + meal.id"
        :open="false"
      >
        <div
          slot="trigger"
          class="card-header"
          role="button"
          :aria-controls="'mealContent' + meal.id"
        >
          <p class="card-header-title is-size-5">
            <span class="is-uppercase">{{ meal.type }}</span
            ><span class="has-text-dark-grey">
              -{{
                meal.adults * meal.adultPrice + meal.children * meal.childPrice
              }}
              euros
            </span>
          </p>
          <b-button
            icon-pack="fas"
            @click="$delete(meals, meals.indexOf(meal))"
            type="is-medium is-danger"
            icon-left="times"
          ></b-button>
        </div>
        <div class="card-content">
          <b-field label="Date" label-position="on-border">
            <b-datepicker
              icon-pack="fas"
              v-model="meal.date"
              :first-day-of-week="1"
              placeholder="Date du repas"
            ></b-datepicker>
          </b-field>
          <!-- GUESTS -->
          <b-field grouped group-multiline>
            <b-field label="Adultes" label-position="on-border">
              <b-numberinput
                icon-pack="fas"
                v-model="meal.adults"
                min="0"
                controlsPosition="compact"
              ></b-numberinput>
            </b-field>
            <b-field label="Prix adulte" label-position="on-border">
              <b-numberinput
                icon-pack="fas"
                step="0.5"
                min-step="0.01"
                v-model="meal.adultPrice"
                min="0"
                controlsPosition="compact"
              ></b-numberinput>
            </b-field>
          </b-field>

          <!-- CHILDREN -->
          <b-field grouped group-multiline>
            <b-field label="Enfants" label-position="on-border">
              <b-numberinput
                icon-pack="fas"
                v-model="meal.children"
                min="0"
                controlsPosition="compact"
              ></b-numberinput>
            </b-field>
            <b-field label="Prix enfant" label-position="on-border">
              <b-numberinput
                icon-pack="fas"
                step="0.5"
                min-step="0.01"
                v-model="meal.childPrice"
                min="0"
                controlsPosition="compact"
              ></b-numberinput>
            </b-field>
          </b-field>

          <b-field label="Contenu" label-position="on-border">
            <b-input v-model="meal.information" type="textarea"></b-input>
          </b-field>

          <hr />

          <!-- COSTS -->
          <!-- COST LIST -->
          <b-collapse
            class="card meal-card"
            :open="false"
            v-for="cost in meal.costs"
            :key="cost.id"
            :aria-id="'costContent' + cost.id"
          >
            <div
              slot="trigger"
              class="card-header"
              role="button"
              :aria-controls="'costContent' + cost.id"
            >
              <p class="card-header-title">
                {{ cost.name }} : {{ cost.totalPrice }} euros
              </p>
              <b-button
                icon-pack="fas"
                @click="$delete(meal.costs, meal.costs.indexOf(cost))"
                type="is-small is-light"
                icon-left="times"
              ></b-button>
            </div>
            <div class="card-content">
              <div
                v-for="(value, propertyName) in cost"
                v-bind:key="propertyName"
              >
                <span class="tag is-dark is-small">{{ propertyName }}</span>
                <pre>{{ value }}</pre>
              </div>
            </div>
          </b-collapse>

          <!-- COST MODAL -->
          <b-button @click="isCateringCostModalActive = true"
            >Add Cost</b-button
          >

          <b-modal
            :active.sync="isCateringCostModalActive"
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
                  @click="isCateringCostModalActive = false"
                />
              </header>
              <section class="modal-card-body">
                <b-field grouped group-multiline>
                  <b-field label="Type">
                    <b-select
                      v-model="meal.tempCost.type"
                      placeholder="Select a type"
                    >
                      <option value="caterer">Restaurateur</option>
                      <option value="groceries">Courses</option>
                    </b-select>
                  </b-field>
                  <b-field label="Nom">
                    <b-input v-model="meal.tempCost.name"></b-input>
                  </b-field>
                  <b-field label="Unités">
                    <b-input v-model="meal.tempCost.units"></b-input>
                  </b-field>
                  <b-field label="Prix unitaire">
                    <b-input v-model="meal.tempCost.unitPrice"></b-input>
                  </b-field>
                  <b-field label="Prix total">
                    <b-numberinput
                      :controls="false"
                      icon-pack="fas"
                      controls-position="compact"
                      step="0.01"
                      v-model="meal.tempCost.totalPrice"
                    ></b-numberinput>
                  </b-field>
                </b-field>
                <b-field
                  label="Informations supplémentaires"
                  label-position="on-border"
                >
                  <b-input
                    v-model="meal.tempCost.information"
                    type="textarea"
                  ></b-input>
                </b-field>
              </section>
              <footer class="modal-card-foot">
                <b-button type="is-primary" @click="addCost(meal.id)"
                  >Ajouter</b-button
                >
              </footer>
            </div>
          </b-modal>
        </div>
      </b-collapse>

      <!-- ADD MEAL -->
      <div class="box">
        <h5 class="title is-5">
          Ajouter repas
          <b-dropdown aria-role="list" class="is-pulled-right">
            <button class="button is-light is-small" slot="trigger">
              <b-icon pack="fas" icon="plus" size="is-medium"></b-icon>
            </button>

            <b-dropdown-item aria-role="listitem" @click="addMeal('breakfast')"
              >Petit-dejeuner</b-dropdown-item
            >
            <b-dropdown-item aria-role="listitem" @click="addMeal('lunch')"
              >Déjeuner</b-dropdown-item
            >
            <b-dropdown-item aria-role="listitem" @click="addMeal('dinner')"
              >Dîner</b-dropdown-item
            >
          </b-dropdown>
        </h5>
      </div>
    </div>
  </section>
</template>

<script>
import Vue from "vue";

export default {
  components: {},
  data() {
    return {
      meals: this.$store.state.meals,
      isCateringCostModalActive: false,
    };
  },
  computed: {},
  watch: {},

  methods: {
    addMeal: function(mealType) {
      var tempMeal = {
        id: this.uuidv4(),
        type: mealType,
        adults: 10,
        children: 0,
        adultPrice: 17.5,
        childPrice: 15,
        information: null,
        tempCost: {
          type: null,
          name: null,
          units: null,
          unitPrice: null,
          totalPrice: null,
          information: null,
        },
        costs: [],
      };
      this.meals.push(tempMeal);
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

    addCost: function(mealId) {
      var meal = this.meals.find((x) => x.id === mealId);
      var tempCosts = meal.costs;
      meal.tempCost.id = this.uuidv4();
      tempCosts.push(meal.tempCost);

      Vue.set(meal, "costs", JSON.parse(JSON.stringify(tempCosts)));
      meal.tempCost = {
        type: null,
        name: null,
        units: null,
        unitPrice: null,
        totalPrice: null,
        information: null,
      };
      this.isCateringCostModalActive = false;
    },
  },
};
</script>

<style scoped>
.meal-card {
  margin-bottom: 1rem;
}
</style>
