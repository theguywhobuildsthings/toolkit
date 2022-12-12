<template>
  <div v-if="pairStatus == 'not-started'" class="justify-center">
    <h2
      class="mt-6 text-center text-3xl font-bold tracking-tight text-contrast pb-8"
    >
      Scan the QR code.
    </h2>
    <qrcode-vue
      class="border-2 justify-center m-auto w-full"
      :size="200"
      :value="qrDataValue"
      level="H"
    ></qrcode-vue>
    <div class="text-sm justify-center text-center pt-8">
      <label
        >Or enter the code into the
        <a href="#" class="underline text-strong hover:text-contrast">app</a
        >:</label
      >
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

export default defineComponent({
  props: {
    helpValue: String,
    qrDataValue: String,
    pairStatus: String,
  },
  components: {
    QrcodeVue,
  },
});
</script>
