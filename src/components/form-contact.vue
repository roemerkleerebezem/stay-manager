<template>
  <div class="container">
    <!-- FORM SECTION TITLE -->
    <div class="subsection-header has-background-light">
      <h5 class="is-size-5 subtitle has-text-dark has-text-weight-medium">
        Contact
      </h5>
    </div>
    <div class="subsection">
      <!-- EMAIL -->
      <b-field label="Email" label-position="on-border">
        <b-input
          type="email"
          placeholder="Email"
          v-model="contact.email"
        ></b-input>
      </b-field>
      <!-- NAME -->
      <b-field label="Nom" label-position="on-border">
        <b-input placeholder="Nom" v-model="contact.name"></b-input>
      </b-field>
      <!-- PHONE -->
      <b-field label="Téléphone" label-position="on-border">
        <b-input placeholder="Téléphone" v-model="contact.phone"></b-input>
      </b-field>
      <!-- NATIONALITY -->
      <b-field label="Nationalité" label-position="on-border">
        <b-select v-model="contact.nationality" placeholder="Nationalité">
          <option value="french">Francais</option>
          <option value="dutch">Néerlandais</option>
          <option value="german">Allemand</option>
          <option value="other">Autre</option>
        </b-select>
      </b-field>
      <!-- RATING -->
      <b-field label="Avis" label-position>
        <b-rate icon-pack="fas" v-model="contact.rating" custom-text></b-rate>
      </b-field>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      contact: this.$store.state.contact,
    };
  },
  computed: {},
};
</script>

<style scoped></style>
