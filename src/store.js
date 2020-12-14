import Vue from "vue";
import Vuex from "vuex";

import moment from "moment";

import settingProfiles from "./scripts/setting-profiles";

Vue.use(Vuex);

const startState = {
  contact: {
    email: "",
    name: "",
    phone: "",
    nationality: null,
    rating: null,
  },
  booking: {
    status: null,
    source: null,
    date: moment().toDate(),
    deposits: [],
    costs: [],
    internalCosts: [],
    uuid: null,
    invoiceNumber: 0,
  },
  invoices: [],
  stay: {
    arrivalDate: moment()
      .startOf("day")
      .unix(),
    departureDate: moment()
      .startOf("day")
      .add(1, "days")
      .unix(),
    arrivalTime: moment()
      .hour(17)
      .minute(0)
      .unix(),
    departureTime: moment()
      .hour(12)
      .minute(0)
      .unix(),
    stayNightArray: [
      {
        id: 100,
        date: moment()
          .startOf("day")
          .unix(),
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
      },
    ],
    guestInfo: "",
  },
  meals: [],
  settings: settingProfiles.find((x) => x.default === true),
};

export default new Vuex.Store({
  state: startState,
  mutations: {
    addUUID(state, uuid) {
      state.booking.uuid = uuid;
    },
    replaceState(state, newState) {
      newState.booking.date =
        newState.booking.date == null
          ? null
          : moment(newState.booking.date).toDate();
      newState.stay.arrivalDate =
        newState.stay.arrivalDate == null
          ? null
          : moment.unix(newState.stay.arrivalDate).unix();
      newState.stay.departureDate =
        newState.stay.departureDate == null
          ? null
          : moment.unix(newState.stay.departureDate).unix();
      newState.meals.forEach(function(meal) {
        meal.date = meal.date == null ? null : moment(meal.date).toDate();
      });

      Object.assign(state, newState);
    },
    updateInvoice(state, newInvoice) {
      var newUuid = newInvoice.meta.uuid;

      var updated = false;

      state.invoices.forEach(function(invoice, index, thisArray) {
        if (invoice.meta.uuid == newUuid) {
          thisArray[index] = newInvoice;
          updated = true;
        } else {
        }
      });

      if (updated == false) {
        state.invoices.push(newInvoice);
      }
    },
  },
  actions: {},
});
