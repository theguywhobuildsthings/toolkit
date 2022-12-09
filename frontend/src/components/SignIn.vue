<template>
  <div
    class="flex min-h-full items-center justify-center py-12 px-4 sm:px-6 lg:px-8"
  >
    <div class="w-full max-w-md space-y-8">
      <div>
        <img
          class="mx-auto h-12 w-auto"
          src="@/../assets/logo_transparent_wordless.png"
          alt="Toolkit Sign In"
        />
        <h2
          class="mt-6 text-center text-3xl font-bold tracking-tight text-contrast"
        >
          Sign in to your account
        </h2>
      </div>
      <input type="hidden" name="remember" value="true" />
      <div class="-space-y-px rounded-md shadow-sm">
        <div>
          <label for="username" class="sr-only">UserName</label>
          <input
            id="username"
            name="username"
            type="username"
            v-model="username"
            autocomplete="username"
            required
            class="relative block w-full appearance-none rounded-none rounded-t-md border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
            placeholder="User Name"
          />
        </div>
        <div>
          <label for="password" class="sr-only">Password</label>
          <input
            id="password"
            name="password"
            type="password"
            v-model="password"
            autocomplete="current-password"
            required
            class="relative block w-full appearance-none rounded-none rounded-b-md border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
            placeholder="Password"
          />
        </div>
      </div>

      <div class="flex items-center justify-center">
        <div class="text-sm">
          <label>Don't have an account?&nbsp;&nbsp;&nbsp;</label>
          <router-link
            to="/sign-up"
            class="font-medium text-indigo-600 hover:text-indigo-500 justify-end"
            >Sign up</router-link
          >
        </div>
      </div>

      <div>
        <button
          type="submit"
          class="group relative flex w-full justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
          @click="login"
        >
          Sign in
        </button>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "SignIn",
  props: {
    msg: String,
  },
  data: () => {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    async login() {
      const bodyFormData = new FormData();
      bodyFormData.append("username", this.username);
      bodyFormData.append("password", this.password);
      this.axios({
        method: "post",
        url: "http://localhost:8000/auth/token",
        data: bodyFormData,
      })
        .then((res) => {
          console.log("saving");
          localStorage.auth_token = res.data.access_token;
          this.$store.dispatch("setToken", res.data.access_token);
          this.$router.push({ name: "home" });
        })
        .catch(() => {
          console.error("Unable to log in");
        });
    },
  },
});
</script>
