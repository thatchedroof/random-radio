import adapter from "@sveltejs/adapter-static";
import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";
import { resolve } from "path";

/** @type {import('@sveltejs/kit').Config} */
const config = {
  preprocess: vitePreprocess(),

  kit: {
    adapter: adapter({
      fallback: "404.html",
    }),
    alias: {
      "random-radio": resolve("./random-radio"),
    },
    paths: {
      base: process.argv.includes("dev") ? "" : "/random-radio",
    },
  },
};

export default config;
