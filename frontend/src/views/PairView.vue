<template>
  <div
    class="flex min-h-full items-center justify-center py-12 px-4 sm:px-6 lg:px-8"
  >
    <div class="w-full max-w-md justify-center">
      <pair-qr
        v-if="pairStatus == 'not-started'"
        :help-value="helpValue"
        :pair-status="pairStatus"
        :qr-data-value="qrDataValue"
      ></pair-qr>
      <pairing v-if="pairStatus == 'pair-start'"></pairing>
      <pair-complete v-if="pairStatus == 'pair-complete'"></pair-complete>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import PairQr from "@/components/pair/PairQr.vue";
import Pairing from "@/components/pair/Pairing.vue";
import PairComplete from "@/components/pair/PairComplete.vue";
import { createLogger } from "@evilkiwi/logger";

const logger = createLogger({
  name: "pair-view",
});

export default defineComponent({
  name: "PairView",
  title: "Pair Device",
  components: {
    PairQr,
    Pairing,
    PairComplete,
  },
  data: () => {
    return {
      qrDataValue: "",
      helpValue: "",
      connection: {} as WebSocket,
      pairStatus: "not-started",
    };
  },
  methods: {
    updateQRData(val: string) {
      logger.debug(`Updating qr data ${val}`);
      this.qrDataValue = val;
    },
    updateHelpTextValue(val: string) {
      logger.debug(`Updating help data ${val}`);
      this.helpValue = val;
    },
    updatePairStatus(val: string) {
      this.pairStatus = val;
    },
  },

  created: function () {
    const setQrValue = (val: string) => {
      this.updateQRData(val);
    };
    const setHelpTextValue = (val: string) => {
      this.updateHelpTextValue(val);
    };
    const forwardToDevices = () => {
      this.$router.push({ name: "devices" });
    };
    const setPairStatus = (val: string) => {
      this.updatePairStatus(val);
    };
    logger.info("Starting connection to WebSocket Server");
    const token = this.$store.getters.token;
    let connection = this.connection;
    connection = new WebSocket(`ws://localhost:8000/pair/${token}`);

    connection.onopen = function () {
      connection.send(
        JSON.stringify({
          type: "request",
          request: {
            type: "pair-data",
          },
        })
      );
    };

    connection.onclose = function (event) {
      logger.info("Closing socket", event);
    };

    connection.onmessage = function (event: MessageEvent) {
      const reqData = JSON.parse(event.data);
      logger.info(`Received Message`, reqData);
      if (reqData.message == "pair-info") {
        setQrValue(
          `${process.env.VUE_APP_BACKEND_URL}${reqData.data.pair_url_path}`
        );
        setHelpTextValue(`${reqData.data.uuid}`);
        setHelpTextValue(
          `${process.env.VUE_APP_BACKEND_URL}${reqData.data.pair_url_path}`
        );
      }
      if (reqData.message == "pair-start") {
        setPairStatus("pair-start");
      }
      if (reqData.message == "pair-complete") {
        setPairStatus("pair-complete");
      }
      if (reqData.message == "pair-confirm") {
        forwardToDevices();
      }
    };
  },
  beforeUnmount() {
    try {
      logger.debug("trying to close connection");
      this.connection.close();
    } catch {
      logger.debug("Unable to close connection");
    }
  },
});
</script>
