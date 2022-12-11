<template>
  <sign-in></sign-in>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import SignIn from "@/components/SignIn.vue";

export default defineComponent({
  name: "SignInView",
  components: {
    SignIn,
  },
  title: "Sign in",
});
</script>
