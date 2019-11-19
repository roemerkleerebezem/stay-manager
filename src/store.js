import Vue from "vue";
import Vuex from "vuex";

import moment from "moment";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    contact: {
      email: null,
      name: null,
      phone: null,
      nationality: null
    },
    booking: {
      source: null,
      date: null
    },
    stay: {
      arrivalDatetime: moment()
        .hour(17)
        .minute(0)
        .toDate(),
      departureDatetime: moment()
        .hour(14)
        .minute(0)
        .toDate(),
      baseGuests: 10,
      stayNightArray: [],
      children: null,
      guestInfo: null,
      pets: null
    },
    meals: []
  },
  mutations: {},
  actions: {}
});
