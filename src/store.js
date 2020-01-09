import Vue from "vue";
import Vuex from "vuex";

import moment from "moment";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    contact: {
      email: "",
      name: "",
      phone: "",
      nationality: null
    },
    booking: {
      status: null,
      source: null,
      date: null,
      deposits: [],
      costs: [],
      uuid: null
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
      children: 0,
      guestInfo: "",
      pets: 0
    },
    meals: [],
    prices: {
      villaNight: 100,
      stayNight: 35,
      petNight: 5,
      taxeSejourNight: 1,
      extraHour: 20
    },
    discountPerNight: {
      0: 0,
      1: 0,
      2: 0,
      3: 0.1,
      4: 0.15
    }
  },
  mutations: {
    addUUID(state, uuid) {
      state.booking.uuid = uuid;
    }
  },
  actions: {}
});
