<template>
  <!-- FORM -->
  <section class="section" style="height:100%">
    <div class="container">
      <!-- FORM TITLE -->
      <div class="box">
        <h3 class="title is-3">Settings</h3>
      </div>

      <div class="box has-background-light">
        <div class="columns">
          <setting-sheet></setting-sheet>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import Vue from "vue";

import fs from "fs";

import axios from "axios";
import moment from "moment";

import settingSheet from "../components/setting-sheet.vue";

export default {
  components: {
    settingSheet,
  },

  data() {
    return {
      tempInvoice: {
        meta: {
          uuid: null,
          lastModificationDate: null,
          creationDate: null,
          cateringNoPrint: false,
          stayNoPrint: false,
          contractNoPrint: false,
          invoiceNumber: this.$store.state.booking.invoiceNumber,
        },
      },
    };
  },
  computed: {},
  watch: {},
  mounted() {},
  methods: {},
};
</script>

<style scoped>
.b-numberinput {
  max-width: 300px;
}
</style>
