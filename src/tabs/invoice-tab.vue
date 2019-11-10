<template>
  <!-- FORM -->
  <section class="section">
    <div class="container">
      <!-- FORM TITLE -->
      <div class="box">
        <h3 class="title is-3">Facture</h3>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  components: {},
  data() {
    return {
      meals: []
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
    }
  }
};
</script>

<style scoped>
</style>