<template>
  <sign-up></sign-up>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import SignUp from "@/components/SignUp.vue";

export default defineComponent({
  name: "SignUpView",
  components: {
    SignUp,
  },
  title: "Sign up",
});
</script>
