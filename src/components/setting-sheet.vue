<template>
  <div class="column">
    <div class="box">
      <!-- HEADER -->
      <div class="level">
        <div class="level-left">
          <b-dropdown aria-role="list">
            <button class="button is-primary" slot="trigger">
              <span>{{ currentSettings.name }}</span>
              <b-icon pack="fas" icon="caret-down"></b-icon>
            </button>
            <div v-for="setting in fileSettings" :key="setting.name">
              <b-dropdown-item
                @click="setSetting(setting.name)"
                aria-role="listitem"
                >{{ setting.name }}
                <div
                  v-if="setting.default"
                  style="margin-left:1rem;"
                  class="tag is-warning"
                >
                  DEFAULT
                </div></b-dropdown-item
              >
            </div>
          </b-dropdown>
        </div>
        <div class="level-right">
          <b-button
            type="is-dark"
            class="has-text-weight-medium is-uppercase level-item"
            @click="editingCurrent = !editingCurrent"
          >
            {{ editingCurrent ? "LOCK" : "UNLOCK" }}
          </b-button>
          <b-button
            type="is-warning"
            v-if="!currentSettings.default"
            class="has-text-weight-medium is-uppercase level-item"
            @click="saveSettings(currentSettings, 'modify-setting')"
          >
            {{ currentSettings.default ? "DEFAULT" : " SET DEFAULT" }}
          </b-button>
          <b-button
            v-if="!currentSettings.default"
            type="is-danger"
            class="has-text-weight-medium is-uppercase level-item"
            @click="saveSettings(currentSettings, 'delete-setting')"
          >
            DELETE
          </b-button>
          <!-- SAVE NEW / DELETE -->
          <b-button
            :disabled="notUpdatable"
            type="is-success"
            @click="isSaveModalActive = true"
            >{{
              fileSettings.some(
                (setting) => setting.name === currentSettings.name
              )
                ? "Update "
                : "New "
            }}
            settings</b-button
          >

          <b-modal
            :active.sync="isSaveModalActive"
            has-modal-card
            :destroy-on-hide="false"
            width="50%"
            trap-focus
            scroll="keep"
          >
            <div class="modal-card">
              <header class="modal-card-head">
                <p class="modal-card-title">Save new profile</p>
                <button
                  type="button"
                  class="delete"
                  @click="isSaveModalActive = false"
                />
              </header>
              <section class="modal-card-body">
                <b-field label="Name" label-position="on-border">
                  <b-input
                    v-model="currentSettings.name"
                    placeholder="default"
                  ></b-input>
                </b-field>
                <div class="block">
                  <span
                    class="has-text-danger has-text-weight-bold"
                    v-if="nameExists"
                    >THIS WILL OVERWRITE {{ currentSettings.name }}</span
                  >
                </div>
              </section>
              <footer class="modal-card-foot">
                <b-button
                  type="is-primary"
                  @click="saveSettings(currentSettings, 'save-setting')"
                  >Ajouter</b-button
                >
              </footer>
            </div>
          </b-modal>
        </div>
      </div>
      <!-- PRICES -->
      <div class="subsection-header has-background-dark">
        <h5 class="is-size-5 subtitle has-text-light has-text-weight-medium">
          Prices
        </h5>
      </div>

      <div class="subsection">
        <b-field grouped grouped-muliline>
          <!-- VILLA -->
          <b-field label="Villa night">
            <b-numberinput
              icon-pack="fas"
              v-model="currentSettings.prices.villa"
              :controls="false"
              min="0"
              type="is-light"
              :disabled="!editingCurrent"
            ></b-numberinput>
          </b-field>

          <!-- GUEST -->
          <b-field label="Guest night">
            <b-numberinput
              icon-pack="fas"
              v-model="currentSettings.prices.guest"
              :controls="false"
              min="0"
              type="is-light"
              :disabled="!editingCurrent"
            ></b-numberinput>
          </b-field>

          <!-- PET -->
          <b-field label="Pet night">
            <b-numberinput
              icon-pack="fas"
              v-model="currentSettings.prices.pet"
              :controls="false"
              min="0"
              type="is-light"
              :disabled="!editingCurrent"
            ></b-numberinput>
          </b-field>

          <!-- EXTRA HOURS -->
          <b-field label="Extra hour">
            <b-numberinput
              icon-pack="fas"
              v-model="currentSettings.prices.extraHour"
              :controls="false"
              min="0"
              type="is-light"
              :disabled="!editingCurrent"
            ></b-numberinput>
          </b-field>

          <!-- TAX -->
          <b-field label="Taxe de Sejour (%)">
            <b-numberinput
              icon-pack="fas"
              v-model="currentSettings.prices.taxeSejour"
              :controls="false"
              min="0"
              type="is-light"
              :step="0.01"
              :disabled="!editingCurrent"
            ></b-numberinput>
          </b-field>
        </b-field>
        <hr />

        <!-- DISCOUNT -->
        <div class="subsection-header has-background-dark">
          <h5 class="is-size-5 subtitle has-text-light has-text-weight-medium">
            Discount per night
          </h5>
        </div>
        <b-field grouped group-multiline>
          <b-field
            :label="nights + ' nights'"
            v-for="(discount, nights) in currentSettings.discountPerNight"
            :key="nights"
          >
            <b-numberinput
              style="max-width:100px"
              icon-pack="fas"
              v-model="currentSettings.discountPerNight[nights]"
              min="0"
              type="is-light"
              :step="0.01"
              :controls="false"
              :disabled="!editingCurrent"
            ></b-numberinput>
          </b-field>
        </b-field>

        <hr />

        <!-- TIMES -->
        <div class="subsection-header has-background-dark">
          <h5 class="is-size-5 subtitle has-text-light has-text-weight-medium">
            Check-in / Check-out
          </h5>
        </div>
        <b-field grouped grouped-multiline>
          <b-field label="Check-in">
            <b-field grouped>
              <b-numberinput
                style="max-width:100px"
                icon-pack="fas"
                v-model="currentSettings.minArrivalTime.hour"
                min="0"
                type="is-light"
                :step="0.01"
                :controls="false"
                :disabled="!editingCurrent"
              ></b-numberinput>
              <span class="is-size-4">:</span>
              <b-numberinput
                style="max-width:100px"
                icon-pack="fas"
                v-model="currentSettings.minArrivalTime.minute"
                min="0"
                type="is-light"
                :step="0.01"
                :controls="false"
                :disabled="!editingCurrent"
              ></b-numberinput>
            </b-field>
          </b-field>

          <b-field label="Check-out">
            <b-field grouped>
              <b-numberinput
                style="max-width:100px"
                icon-pack="fas"
                v-model="currentSettings.maxDepartureTime.hour"
                min="0"
                type="is-light"
                :controls="false"
                :disabled="!editingCurrent"
              ></b-numberinput>
              <span class="is-size-4">:</span>
              <b-numberinput
                style="max-width:100px"
                icon-pack="fas"
                v-model="currentSettings.maxDepartureTime.minute"
                min="0"
                type="is-light"
                :controls="false"
                :disabled="!editingCurrent"
              ></b-numberinput>
            </b-field> </b-field
        ></b-field>

        <hr />

        <!-- INVOICE DATA -->
        <div class="subsection-header has-background-dark">
          <h5 class="is-size-5 subtitle has-text-light has-text-weight-medium">
            Invoice information
          </h5>
        </div>

        <!-- FOOTER MAIN PAGE -->
        <div class="columns">
          <div class="column">
            <b-field label="Footer main invoice page">
              <b-input
                v-model="currentSettings.invoiceData.mainTableFooter"
                type="textarea"
                :disabled="!editingCurrent"
              ></b-input>
            </b-field>
          </div>
          <!-- FOOTER MAIN TABLE -->
          <div class="column">
            <b-field label="Footer main invoice table">
              <b-input
                v-model="currentSettings.invoiceData.mainPageFooter"
                type="textarea"
                :disabled="!editingCurrent"
              ></b-input>
            </b-field>
          </div>
        </div>
        <hr />

        <!-- HOST INFO -->
        <b-field label="Host information"></b-field>
        <b-field grouped group-multiline>
          <b-field label="Name" label-position="on-border">
            <b-input
              v-model="currentSettings.invoiceData.host.name"
              :disabled="!editingCurrent"
            ></b-input>
          </b-field>
          <b-field label="Phone" label-position="on-border">
            <b-input
              v-model="currentSettings.invoiceData.host.phone"
              :disabled="!editingCurrent"
            ></b-input>
          </b-field>
          <b-field label="Email" label-position="on-border">
            <b-input
              v-model="currentSettings.invoiceData.host.email"
              :disabled="!editingCurrent"
            ></b-input>
          </b-field>
          <b-field label="Address line 1" label-position="on-border">
            <b-input
              v-model="currentSettings.invoiceData.host.address1"
              :disabled="!editingCurrent"
            ></b-input>
          </b-field>
          <b-field label="Address line 2" label-position="on-border">
            <b-input
              v-model="currentSettings.invoiceData.host.address2"
              :disabled="!editingCurrent"
            ></b-input>
          </b-field>
        </b-field>
        <hr />

        <!-- PROPERTY INFO -->
        <b-field label="Property information"></b-field>
        <b-field grouped group-multiline>
          <b-field label="Description" label-position="on-border">
            <b-input
              v-model="currentSettings.invoiceData.property.description"
              :disabled="!editingCurrent"
              type="textarea"
            ></b-input>
          </b-field>
          <b-field label="Address" label-position="on-border">
            <b-input
              v-model="currentSettings.invoiceData.property.address"
              :disabled="!editingCurrent"
              type="textarea"
            ></b-input>
          </b-field>
        </b-field>

        <hr />

        <!-- PRINT OPTIONS -->
        <b-field label="Print on invoice :"></b-field>
        <div class="field">
          <b-checkbox
            :disabled="!editingCurrent"
            v-model="currentSettings.invoiceData.print.catering"
          >
            Catering
          </b-checkbox>
          <div class="field"></div>
          <b-checkbox
            :disabled="!editingCurrent"
            v-model="currentSettings.invoiceData.print.contract"
          >
            Contract
          </b-checkbox>
          <div class="field"></div>
          <b-checkbox
            v-model="currentSettings.invoiceData.print.stay"
            :disabled="!editingCurrent"
          >
            Stay
          </b-checkbox>
        </div>
        <hr />

        <!-- CONTRACT CREATION CITY -->
        <b-field label="Invoice made in">
          <b-input
            v-model="currentSettings.invoiceData.creationCity"
            :disabled="!editingCurrent"
          >
          </b-input>
        </b-field>
        <div class="container">
          <!-- <p>"creationDate": 1607507017,</p>
                  <p>"invoiceIndex": "2020-12-005",</p>
                  <p>"invoiceNumber": 5,</p>
                  <p>"lastModificationDate": 1607507036,</p> -->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import settingProfiles from "../scripts/setting-profiles.json";

import Vue from "vue";

import axios from "axios";

import assert from "assert";

export default {
  data() {
    return {
      editingCurrent: false,
      fileSettings: settingProfiles,
      isSaveModalActive: false,
    };
  },
  computed: {
    currentSettings: function() {
      return this.$store.state.settings;
    },
    nameExists: function() {
      return this.fileSettings.some(
        (setting) => setting.name === this.currentSettings.name
      );
    },
    notUpdatable: function() {
      var savedSetting = this.fileSettings.find(
        (x) => x.name === this.currentSettings.name
      );

      savedSetting = savedSetting;
      var currentSettings = this.currentSettings;

      var updatable = this.deepEqual(savedSetting, currentSettings);
      return updatable;
    },
  },

  methods: {
    deepEqual: function(a, b) {
      try {
        assert.deepEqual(a, b);
      } catch (error) {
        if (error.name === "AssertionError") {
          return false;
        }
        throw error;
      }
      return true;
    },

    setSetting: function(name) {
      const settings = JSON.parse(JSON.stringify(this.fileSettings));
      Vue.set(
        this.$store.state,
        "settings",
        settings.find((x) => x.name === name)
      );
    },
    saveSettings: async function(settings, action) {
      const headers = {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json",
      };

      var request = {};
      request["action"] = action;
      request["data"] = settings;

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

      this.$forceUpdate();

      this.setSetting(settings.name);

      return ApiInvoice;
    },
  },
};
</script>

<style scoped></style>
