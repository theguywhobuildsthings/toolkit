<template>
  <div>
    <devices-table :devices="devices" class="hidden md:block"></devices-table>
    <device-cards :devices="devices" class="block md:hidden"></device-cards>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import DevicesTable from "@/components/devices/DevicesTable.vue";
import DeviceCards from "@/components/devices/DeviceCards.vue";
import { createLogger } from "@evilkiwi/logger";

const logger = createLogger({
  name: "devices-view",
});

export default defineComponent({
  title: "Devices",
  components: {
    DevicesTable,
    DeviceCards
  },
  data() {
      return {
        devices: []
      };
  },
  created() {
    this.axios({
      method: "get",
      url: "http://localhost:8000/pair/list",
    }).then((res) => {
      logger.info("Retrieved the list of pairs", res)
      
      this.devices = res.data
    }).catch((err) => {
      logger.error("Unable to load the pair list", err)
    });
  }
});
</script>
