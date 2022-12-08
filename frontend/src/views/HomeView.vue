<template>
  <sign-up></sign-up>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import SignUp from "@/components/SignUp.vue"; // @ is an alias to /src

export default defineComponent({
  name: "HomeView",
  components: {
    SignUp,
  },
});
</script>
