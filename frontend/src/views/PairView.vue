<template>
  <div
    class="flex min-h-full items-center justify-center py-12 px-4 sm:px-6 lg:px-8"
  >
    <div class="w-full max-w-md justify-center">
      <h2
        class="mt-6 text-center text-3xl font-bold tracking-tight text-contrast pb-8"
      >
        Scan the QR code.
      </h2>
      <div v-if="showQr" class="justify-center">
        <qrcode-vue
          class="border-2 justify-center m-auto w-full"
          :size="200"
          :value="qrDataValue"
          level="H"
        ></qrcode-vue>
      </div>

      <div v-if="!showQr" class="flex justify-center items-center">
        <div
          class="spinner-border animate-spin inline-block w-8 h-8 border-4 rounded-full"
          role="status"
        >
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <div class="flex items-center justify-center pt-8">
        <div class="text-sm" v-if="showQr">
          <label
            >Or enter the code into the
            <a href="#" class="underline text-strong hover:text-contrast">app</a
            >:</label
          >
        </div>
      </div>
      <div class="flex items-center justify-center">
        <div class="text-sm">
          <!-- <label>{{ helpValue }}</label> -->
          <a :href="helpValue">Link</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

import QrcodeVue from "qrcode.vue";
import { createLogger } from "@evilkiwi/logger";

const logger = createLogger({
  name: "router",
});

export default defineComponent({
  name: "PairView",
  title: "Pair Device",
  components: {
    QrcodeVue,
  },
  data: () => {
    return {
      qrDataValue: "",
      helpValue: "",
      connection: {} as WebSocket,
      showQr: true,
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
    updateQrVisibility(val: boolean) {
      this.showQr = val;
    },
  },

  created: function () {
    this.axios({
      method: "get",
      headers: {
        // Authorization: `Bearer ${this.$store.getters.token}`,
      },
      url: "http://localhost:8000/pair/list",
    }).then((res) => {
      logger.info("re: ", res);
    });
    const setQrValue = (val: string) => {
      this.updateQRData(val);
    };
    const setHelpTextValue = (val: string) => {
      this.updateHelpTextValue(val);
    };
    const forwardToDevices = () => {
      this.$router.push({ name: "devices" });
    };
    const setQr = (val: boolean) => {
      this.updateQrVisibility(val);
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
        setQr(false);
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
