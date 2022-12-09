import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import "./style.css";
import mixinTitle from "./mixins/title";

createApp(App).use(store).use(router).mixin(mixinTitle).mount("#app");
