import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store/store";
import "./style.css";
import mixinTitle from "./mixins/title";
import axios from "axios";
import VueAxios from "vue-axios";

const token = localStorage.auth_header;
if (token) {
  axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
}

const app = createApp(App);

app
  .use(store)
  .provide("$store", store)
  .use(router)
  .use(VueAxios, axios)
  .mixin(mixinTitle)
  .mount("#app");
