<template>
    <div class="w-full justify-center">
        <h2
        class="mt-6 text-center text-3xl font-bold tracking-tight text-contrast pb-8"
      >
        Devices
      </h2>
<div class="container border rounded border-accent">

	<table class="text-left w-full">
		<thead class="bg-base border-b border-accent flex text-white w-full">
			<tr class="flex w-full mb-1">
				<th class="p-4 w-1/3">User Name</th>
				<th class="p-4 w-1/3">Status</th>
				<th class="p-4 w-1/3"></th>
			</tr>
		</thead>
		<tbody class="flex flex-col items-center overflow-y-scroll w-full" style="height: 50vh;">
            <device-row 
                v-for="device in devices"
                :key="device.uuid"
                :id="device.uuid"
                :username="device.username"
                :status="device.pair_status"
            ></device-row>
		</tbody>
	</table>
</div>
</div>



  <!-- <div class="container w-100">
    <div class=" flex mx-0 overflow-hidden rounded-lg border border-strong">
        <table class="w-full">
            <thead class="border-b border-strong bg-base-dark">
                <tr class="w-full">
                    <th
                        scope="col"
                        class="w-1/3 text-sm font-medium text-accent px-2 px-6 py-4 text-left">
                        User Name
                    </th>
                    <th
                        scope="col"
                        class="w-1/3 text-sm font-medium text-accent px-2 px-6 py-4 text-left">
                        Status
                    </th>
                    <th
                        scope="col"
                        class="w-1/3 text-sm font-medium text-accent px-2 px-6 py-4 text-left">
                    </th>
                </tr>
            </thead>
            <tbody class="bg-grey-light flex flex-col items-center justify-between overflow-y-scroll w-full" style="height: 50vh;">
                <tr class="w-full">
                    <td>
                        hey
                    </td>
                    <td>
                        dude
                    </td>
                </tr>
                <tr class="w-full">
                    <td>
                        hey
                    </td>
                    <td>
                        dude
                    </td>
                </tr>
                <tr class="w-full">
                    <td>
                        hey
                    </td>
                    <td>
                        dude
                    </td>
                </tr>
                <tr class="w-full">
                    <td>
                        hey
                    </td>
                    <td>
                        dude
                    </td>
                </tr>

                <tr class="w-full">
                    <td>
                        hey
                    </td>
                    <td>
                        dude
                    </td>
                </tr>
                <tr class="w-full">
                    <td>
                        hey
                    </td>
                    <td>
                        dude
                    </td>
                </tr>
                <tr class="w-full">
                    <td>
                        hey
                    </td>
                    <td>
                        dude
                    </td>
                </tr>
                <var>v</var>
            </tbody>
        </table> -->
        <!-- <table>
        <thead class="border-b border-strong bg-base-dark">
            <tr>
            <th
                scope="col"
                class="w-1/3 text-sm font-medium text-accent px-2 px-6 py-4 text-left"
            >
                User Name
            </th>
            </tr>
        </thead>
        <tbody>
        </tbody>
    </table> -->
    <!-- </div> -->
      <!-- <div class="py-2 inline-block min-w-full sm:px-6 lg:px-8">
        <div class="">
          <table class="min-w-full bg-base-dark">
            
            
          </table>
        </div>
      </div>
    </div> -->
  <!-- </div> -->
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import DeviceRow from "./DeviceRow.vue";

interface Device {
    id: Number,
    uuid: string,
    username?: string,
    pair_status: string
}

export default defineComponent({
  components: {
    DeviceRow,
  },
  props: {
    devices: Array as PropType<Array<Device>>
  }
});
</script>
