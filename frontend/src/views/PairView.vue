<template>
  <div
    class="flex min-h-full items-center justify-center py-12 px-4 sm:px-6 lg:px-8"
  >
    <div class="w-full max-w-md justify-center">
      <h2
        class="mt-6 text-center text-3xl font-bold tracking-tight text-contrast"
      >
        Scan the QR code with your device.
      </h2>
      <div class="justify-center">
        <qrcode-vue
          class="border-2 justify-center m-auto w-full"
          size="200"
          :value="qrDataValue"
          level="H"
        ></qrcode-vue>
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
    };
  },
  methods: {
    updateQRData(val: string) {
      console.log(`Updating qr data ${val}`);
      this.qrDataValue = val;
    },
  },

  created: function () {
    const setQrValue = (val: string) => {
      this.updateQRData(val);
    };
    console.log("Starting connection to WebSocket Server");
    const token = this.$store.getters.token;
    const connection = new WebSocket(`ws://localhost:8000/pair/${token}`);

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
        console.log("here");
        setQrValue(
          `${process.env.VUE_APP_BACKEND_URL}${reqData.data.pair_url_path}`
        );
        // element.qrCodeUrl = JSON.stringify(reqData.data);
      }
      console.log(reqData);
    };
  },
});
</script>
