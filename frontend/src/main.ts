import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

// Vuetify
import "vuetify/styles";
import { createVuetify, ThemeDefinition } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import { aliases, mdi } from "vuetify/iconsets/mdi";

const myCustomDarkTheme: ThemeDefinition = {
  dark: true,
  colors: {
    background: "#1E1E1E",
    surface: "#1E1E1E",
    primary: "#D6E5E3",
    "primary-darken-1": "#CACFD6",
    secondary: "#9FD8CB",
    "secondary-darken-1": "#517664",
    error: "#CC5A71",
    info: "#6C698D",
    success: "#698F3F",
    warning: "#FC814A",
  },
};

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: "myCustomDarkTheme",
    themes: {
      myCustomDarkTheme,
    },
  },
  icons: {
    defaultSet: "mdi",
    aliases,
    sets: {
      mdi,
    },
  },
});

createApp(App).use(store).use(router).use(vuetify).mount("#app");
