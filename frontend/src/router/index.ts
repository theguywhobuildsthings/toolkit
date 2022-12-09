import { createRouter, createWebHashHistory, RouteRecordRaw } from "vue-router";
import HomeView from "../views/HomeView.vue";
import { checkToken } from "@/utils/auth";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/about",
    name: "about",
    component: HomeView,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/sign-in",
    name: "sign-in",
    component: () => import("../views/SignInView.vue"),
  },
  {
    path: "/sign-up",
    name: "sign-up",
    component: () => import("../views/SignUpView.vue"),
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (localStorage.getItem("auth_token") == null) {
      console.log("No token");
      next({
        path: "/sign-in",
        params: { nextUrl: to.fullPath },
      }); // I get the error at this level it doesn't recognise next as a function
    } else {
      checkToken().then((isValid) => {
        if (isValid) {
          console.log("Valid Token");
          next();
        } else {
          console.log("Invalid Token");
          next({
            path: "/sign-in",
            params: { nextUrl: to.fullPath },
          });
        }
      });
    }
  } else {
    next();
  }
});

export default router;
