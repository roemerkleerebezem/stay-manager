<template>
  <!-- FORM -->
  <section class="section">
    <div class="container">
      <!-- FORM TITLE -->
      <div class="box">
        <h3 class="title is-3">Restauration</h3>
      </div>

      <!-- MEAL LIST -->
      <div class="card meal-card" v-for="meal in meals" :key="meal.id">
        <div class="card-header">
          <p class="card-header-title">{{ meal.type }}</p>
          <b-button @click="$delete(meals, meal.id)" type="is-medium is-danger" icon-left="times"></b-button>
        </div>
        <div class="card-content">
          <b-field label="Date" label-position="on-border">
            <b-datepicker v-model="meal.date" placeholder="Date du repas"></b-datepicker>
          </b-field>
          <!-- GUESTS -->
          <b-field grouped group-multiline>
            <b-field label="Adultes" label-position="on-border">
              <b-numberinput v-model="meal.adults" min="0" controlsPosition="compact"></b-numberinput>
            </b-field>
            <b-field label="Prix adulte" label-position="on-border">
              <b-numberinput
                step="0.5"
                v-model="meal.adultPrice"
                min="0"
                controlsPosition="compact"
              ></b-numberinput>
            </b-field>
          </b-field>

          <!-- CHILDREN -->
          <b-field grouped group-multiline>
            <b-field label="Enfants" label-position="on-border">
              <b-numberinput v-model="meal.children" min="0" controlsPosition="compact"></b-numberinput>
            </b-field>
            <b-field label="Prix enfant" label-position="on-border">
              <b-numberinput
                step="0.5"
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
          <div class="card meal-card" v-for="cost in meal.costs" :key="cost.id">
            <div class="card-header">
              <p class="card-header-title">{{cost.name}} : {{cost.totalPrice}} euros</p>
              <b-button
                @click="$delete(meal.costs, cost.id)"
                type="is-small is-light"
                icon-left="times"
              ></b-button>
            </div>
            <div class="card-content">
              <div v-for="(value, propertyName) in cost" v-bind:key="propertyName">
                <span class="tag is-dark is-small">{{propertyName}}</span>
                <pre>{{value}}</pre>
              </div>
            </div>
          </div>

          <b-field grouped group-multiline>
            <b-field label="Type">
              <b-select v-model="meal.tempCost.type" placeholder="Select a type">
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
              <b-input v-model="meal.tempCost.totalPrice"></b-input>
            </b-field>
          </b-field>
          <b-field label="Informations supplémentaires" label-position="on-border">
            <b-input v-model="meal.tempCost.information" type="textarea"></b-input>
          </b-field>
          <b-button @click="addCost(meal.id)">Ajouter</b-button>
        </div>
      </div>

      <!-- ADD MEAL -->
      <div class="box">
        <h5 class="title is-5">
          Ajouter repas
          <b-dropdown aria-role="list" class="is-pulled-right">
            <button class="button is-light is-small" slot="trigger">
              <b-icon icon="plus"></b-icon>
            </button>

            <b-dropdown-item aria-role="listitem" @click="addMeal('breakfast')">Petit-dejeuner</b-dropdown-item>
            <b-dropdown-item aria-role="listitem" @click="addMeal('lunch')">Déjeuner</b-dropdown-item>
            <b-dropdown-item aria-role="listitem" @click="addMeal('dinner')">Dîner</b-dropdown-item>
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
      meals: this.$store.state.meals
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
    addMeal: function(mealType) {
      var tempMeal = {
        id: this.getId(this.meals),
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
          information: null
        },
        costs: []
      };
      this.meals.push(tempMeal);
    },
    addCost: function(mealId) {
      var meal = this.meals.find(x => x.id === mealId);
      var tempCosts = meal.costs;
      meal.tempCost.id = this.getId(meal.costs);
      tempCosts.push(meal.tempCost);

      Vue.set(meal, "costs", JSON.parse(JSON.stringify(tempCosts)));
      meal.tempCost = {
        type: null,
        name: null,
        units: null,
        unitPrice: null,
        totalPrice: null,
        information: null
      };
    }
  }
};
</script>

<style scoped>
.meal-card {
  margin-bottom: 1rem;
}
</style>