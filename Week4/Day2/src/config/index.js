import { loadEnv } from "./env.js";

const env = loadEnv();

export default {
  env,
  port: process.env.PORT,
  dbUrl: process.env.DB_URL
};
