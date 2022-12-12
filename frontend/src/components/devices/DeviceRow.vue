<template>
  <tr class="flex transition duration-300 ease-in-out hover:bg-base2 w-full">
    <td class="w-1/3 text-accent font-light px-6 py-4 whitespace-nowrap">
      {{ username }}
    </td>
    <td class="w-1/3 text-accent font-light px-6 py-4 whitespace-nowrap">
      {{ statusText }}
    </td>
    <td class="w-1/3 text-accent font-light px-6 py-4 whitespace-nowrap text-center">
        <router-link 
            class="bg-transparent hover:bg-base font-semibold hover:text-contrast py-2 px-4 border border-strong rounded"
            :to="`/device/${id}`"
        >
            Manage
        </router-link>
    </td>
  </tr>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  props: {
    id: String,
    username: String,
    status: String,
  },
  computed: {
    statusText() {
      switch (this.status) {
        case "unpaired":
          return "Unpaired";
        case "pair_started":
          return "Started Pairing";
        case "paired":
          return "Paired";
        case "failed":
          return "Failed Pairing";
        default:
          return "Unknown";
      }
    },
  },
});
</script>
