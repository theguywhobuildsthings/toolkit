module.exports = {
  content: ["./public/index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        base: "#1E1E1E",
        base2: "#2D2D2D",
        "base-dark": "#191919",
        foreground: "#D6E5E3",
        contrast: "#CACFD6",
        accent: "#9FD8CB",
        strong: "#517664",
      },
    },
  },
  plugins: [require("tw-elements/dist/plugin")],
};
