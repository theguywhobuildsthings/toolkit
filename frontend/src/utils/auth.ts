import store from "@/store/store";

const checkToken = async (token: string = store.getters.token) => {
  try {
    const res = await fetch(`${process.env.VUE_APP_BACKEND_URL}/auth/status`, {
      method: "HEAD",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });
    if (res.status == 200) {
      return true;
    }
    return false;
  } catch (error) {
    return false;
  }
};

export { checkToken };
