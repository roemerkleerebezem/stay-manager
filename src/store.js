import Vue from "vue";
import Vuex from "vuex";

import moment from "moment";

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
    uuid: null,
    invoiceNumber: 0,
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
    minArrivalTime: {
      hour: 17,
      minute: 0,
    },
    maxDepartureTime: {
      hour: 12,
      minute: 0,
    },
    baseGuests: 10,
    stayNightArray: [],
    children: 0,
    guestInfo: "",
    pets: 0,
  },
  meals: [],
  prices: {
    villaNight: 100,
    stayNight: 35,
    petNight: 5,
    taxeSejourNight: 0.4,
    extraHour: 25,
  },
  discountPerNight: {
    0: 0,
    1: 0,
    2: 0,
    3: 0.1,
    4: 0.15,
    5: 0.2,
    6: 0.25,
    7: 0.3,
    8: 0.35,
    9: 0.4,
  },
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
      newState.stay.arrivalDatetime =
        newState.stay.arrivalDatetime == null
          ? null
          : moment(newState.stay.arrivalDatetime).toDate();
      newState.stay.departureDatetime =
        newState.stay.departureDatetime == null
          ? null
          : moment(newState.stay.departureDatetime).toDate();

      Object.assign(state, newState);
    },
  },
  actions: {},
});
