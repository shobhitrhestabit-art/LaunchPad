import express from "express";
import loadMiddlewares from "./middleware.js";
import connectDB from "./db.js";
import loadRoutes from "./routes.js";
import logger from "../utils/logger.js";

import errorMiddleware from "../middlewares/error.middleware.js"; // ⭐ NEW


export async function createApp() {
  const app = express();

  loadMiddlewares(app);
  logger.info("✔ Middlewares loaded");

  await connectDB();

  loadRoutes(app);
  app.use(errorMiddleware);

  return app;
}
