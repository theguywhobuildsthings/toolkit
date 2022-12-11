<template>
  <div class="layout">
    <nav-bar class="sticky"></nav-bar>
    <router-view
      class="main flex z-10 relative mx-0 md:mx-32 my-3 overflow-x-hidden overflow-y-auto text-contrast dark:base"
    />
    <footer-bar></footer-bar>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import NavBar from "@/components/NavBar.vue";
import FooterBar from "@/components/FooterBar.vue";

export default defineComponent({
  name: "App",
  components: {
    NavBar,
    FooterBar,
  },
  mounted() {
    this.axios.interceptors.request.use((config) => {
      if (config && config.headers) {
        const token = this.$store.getters.token;
        config.headers.Authorization = token ? `Bearer ${token}` : "";
      }

      return config;
    });
  },
});
</script>

<style lang="scss">
@import "/assets/styles/colors.scss";
#app {
  height: 100%;
}

.layout {
  position: absolute;
  overflow: hidden;
  background-color: $base-color;
  width: 100%;
  height: 100%;
  padding: 0;
}

.body {
  margin: 0;
}
</style>
