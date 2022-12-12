import { createRouter, createWebHashHistory, RouteRecordRaw } from "vue-router";
import HomeView from "../views/HomeView.vue";
import PairView from "../views/PairView.vue";
import DevicesView from "../views/DevicesView.vue";
import DeviceDetailsView from "../views/DeviceDetailsView.vue";
import { checkToken } from "@/utils/auth";
import { createLogger } from "@evilkiwi/logger";

const logger = createLogger({
  name: "router",
});

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/pair",
    name: "pair",
    component: PairView,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/devices",
    name: "devices",
    component: DevicesView,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/device/:id',
    component: DeviceDetailsView,
    props: true,
    meta: {
      requiresAuth: true,
    }
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
      logger.debug(`No token in localstorage.  User is not signed in`);
      next({
        path: "/sign-in",
        params: { nextUrl: to.fullPath },
      }); // I get the error at this level it doesn't recognise next as a function
    } else {
      checkToken().then((isValid) => {
        if (isValid) {
          logger.debug(`Checked token, it is valid.  You are signed in.`);
          next();
        } else {
          logger.debug(`Token is invalid.`);
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
