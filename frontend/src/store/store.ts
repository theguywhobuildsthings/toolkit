import { createStore } from "vuex";

const store = createStore({
  state: {
    token: localStorage.auth_token,
  },
  getters: {
    token: (state) => state.token,
  },
  mutations: {
    UPDATE_TOKEN(state, payload) {
      state.token = payload;
    },
  },
  actions: {
    setToken: (context, token) => {
      context.commit("UPDATE_TOKEN", token);
    },
  },
  modules: {},
});

export default store;
