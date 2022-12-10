<template>
  <div
    class="flex min-h-full items-center justify-center py-12 px-4 sm:px-6 lg:px-8"
  >
    <div class="w-full max-w-md justify-center">
      <h2
        class="mt-6 text-center text-3xl font-bold tracking-tight text-contrast md:pb-8"
      >
        Scan the QR code.
      </h2>
      <div class="justify-center">
        <qrcode-vue
          class="border-2 justify-center m-auto w-full"
          :size="200"
          :value="qrDataValue"
          level="H"
        ></qrcode-vue>
      </div>
      <div class="flex items-center justify-center md:pt-8">
        <div class="text-sm">
          <label
            >Or have them enter the code into the
            <a href="#" class="underline text-strong hover:text-contrast">app</a
            >:</label
          >
        </div>
      </div>
      <div class="flex items-center justify-center">
        <div class="text-sm">
          <label>{{ helpValue }}</label>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

import QrcodeVue from "qrcode.vue";

export default defineComponent({
  name: "PairView",
  title: "Toolkit | Pair Device",
  components: {
    QrcodeVue,
  },
  data: () => {
    return {
      qrDataValue: "",
      helpValue: "",
      connection: {} as WebSocket,
    };
  },
  methods: {
    updateQRData(val: string) {
      console.log(`Updating qr data ${val}`);
      this.qrDataValue = val;
    },
    updateHelpTextValue(val: string) {
      console.log(`Updating help data ${val}`);
      this.helpValue = val;
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
    console.log("Starting connection to WebSocket Server");
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
      console.log(event);
    };

    connection.onmessage = function (event: MessageEvent) {
      console.log(event);
      const reqData = JSON.parse(event.data);
      console.log(reqData);
      if (reqData.message == "pair-info") {
        setQrValue(
          `${process.env.VUE_APP_BACKEND_URL}${reqData.data.pair_url_path}`
        );
        setHelpTextValue(`${reqData.data.uuid}`);
      }
      if (reqData.message == "pair-complete") {
        forwardToDevices();
      }
      console.log(reqData);
    };
  },
  beforeUnmount() {
    try {
      console.log("trying to close connection");
      this.connection.close();
    } catch {
      console.log("Unable to close connection");
    }
  },
});
</script>
