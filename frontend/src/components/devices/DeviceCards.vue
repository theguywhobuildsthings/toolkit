<template>
  <div
    aria-label="group of cards"
    tabindex="0"
    class="grid focus:outline-none py-8 w-full h-[85vh] md:grid-cols-3"
  >
    <div
      v-for="device in devices"
      :key="device.uuid"
      class="focus:outline-none lg:mr-7 lg:mb-6 mb-7 border border-strong pt-6 shadow rounded cursor-pointer text-contrast"
    >
      <div class="flex items-center mb-6">
        <div class="h-10 w-12 text-center">
          <font-awesome-icon
            icon="fa-solid fa-plug w-12 h-12 rounded-full border-10 border-strong text-strong"
          />
        </div>
        <div class="flex items-start justify-between w-full">
          <div class="pl-3 w-full">
            <p
              tabindex="0"
              class="focus:outline-none text-xl font-medium leading-5 text-contrast"
            >
              {{ device.username || "No Username" }}
            </p>
            <p
              tabindex="0"
              class="focus:outline-none text-sm leading-normal pt-2 text-gray-500"
            >
              {{ device.pair_status }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { library } from "@fortawesome/fontawesome-svg-core";
import { faPlug } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

library.add(faPlug);

library.add();
// or .add(brands, solid) if you need the whole solid style icons library/module

import { defineComponent, PropType } from "vue";

interface Device {
  id: number;
  uuid: string;
  username: string;
  pair_status: string;
}

export default defineComponent({
  props: {
    devices: Array as PropType<Array<Device>>,
  },
  components: {
    FontAwesomeIcon,
  },
});
</script>
