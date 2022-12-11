<template>
  <nav
    class="bg-white border-gray-200 px-2 sm:px-4 py-2.5 rounded dark:bg-base h-14"
  >
    <div class="container flex flex-wrap items-center justify-between mx-auto">
      <a href="" class="flex items-center">
        <img
          src="@/../assets/logo_transparent_wordless.png"
          class="h-6 mr-3 sm:h-9"
          alt="Toolkit Logo"
        />
        <span
          class="self-center text-xl tw font-semibold whitespace-nowrap dark:text-white"
          >Toolkit</span
        >
      </a>
      <button
        data-bs-toggle="collapse"
        data-bs-target="#navbar-default"
        aria-expanded="false" 
        aria-controls="navbar-default"
        type="button"
        class="inline-flex items-center p-2 ml-3 text-sm text-gray-500 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600"
      >
        <span class="sr-only">Open main menu</span>
        <svg
          class="w-6 h-6"
          aria-hidden="true"
          fill="currentColor"
          viewBox="0 0 20 20"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            fill-rule="evenodd"
            d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"
            clip-rule="evenodd"
          ></path>
        </svg>
      </button>
      <div
        class="invisible md:visible w-full md:block md:w-auto"
        id="navbar-default"
      >
        <ul
          v-if="!loggedIn"
          class="flex flex-col p-4 mt-4 border border-gray-100 rounded-lg bg-base md:flex-row md:space-x-8 md:mt-0 md:text-sm md:font-medium md:border-0 md:base dark:base md:dark:base dark:border-gray-700"
        >
          <li>
            <router-link
              class="block py-2 pl-3 pr-4 text-contrast bg-base rounded md:bg-transparent md:text-contrast md:p-0 dark:text-white hover:bg-base2"
              aria-current="page"
              to="/sign-in"
              >Sign In</router-link
            >
          </li>
        </ul>
        <ul
          v-if="loggedIn"
          class="flex flex-col p-4 mt-4 border border-gray-100 rounded-lg bg-base md:flex-row md:space-x-8 md:mt-0 md:text-sm md:font-medium md:border-0 md:base dark:base md:dark:base dark:border-gray-700"
        >
          <li>
            <router-link
              class="block py-2 pl-3 pr-4 text-contrast bg-base rounded md:bg-transparent md:text-contrast md:p-0 dark:text-white hover:bg-base2"
              aria-current="page"
              to="/devices"
              >Devices</router-link
            >
          </li>
          <li>
            <router-link
              class="block py-2 pl-3 pr-4 text-contrast bg-base rounded md:bg-transparent md:text-contrast md:p-0 dark:text-white hover:bg-base2"
              aria-current="page"
              to="/pair"
              >Pair Device</router-link
            >
          </li>
          <li>
            <a
              class="block py-2 pl-3 pr-4 text-contrast bg-base rounded md:bg-transparent md:text-contrast md:p-0 dark:text-white hover:bg-base2"
              aria-current="page"
              @click="logout"
              >Sign Out</a
            >
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { checkToken } from "@/utils/auth";
import 'tw-elements';

export default defineComponent({
  name: "NavBar",
  computed: {
    token() {
      checkToken(this.$store.getters.token).then((validtoken) => {
        this.loggedIn = validtoken;
      });
    },
  },
  data: () => {
    return {
      loggedIn: false,
    };
  },
  watch: {
    token() {
      checkToken(this.$store.getters.token).then((validtoken) => {
        this.loggedIn = validtoken;
      });
    },
  },
  methods: {
    logout() {
      this.$store.dispatch("setToken", "");
      localStorage.auth_token = undefined;
      this.$router.push({ name: "home" });
    },
  },
});
</script>
