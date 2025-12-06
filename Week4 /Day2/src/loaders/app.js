import express from "express";
import loadMiddlewares from "./middleware.js";
import connectDB from "./db.js";
import loadRoutes from "./routes.js";
import logger from "../utils/logger.js";

export async function createApp() {
  const app = express();

  loadMiddlewares(app);
  logger.info("✔ Middlewares loaded");

  await connectDB();

  loadRoutes(app);

  return app;
}
