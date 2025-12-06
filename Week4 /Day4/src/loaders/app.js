import express from "express";
import connectDB from "./db.js";

import routes from "../routes/index.js";  
import loadMiddlewares from "./middleware.js";
import { applySecurity } from "../middlewares/security.js";
import errorMiddleware from "../middlewares/error.middleware.js";

// ⭐ NEW: Request tracing
import tracingMiddleware from "../utils/tracing.js";

export async function createApp() {
  const app = express();

  // 1️⃣ Apply security (Helmet, CORS, rate limits)
  applySecurity(app);

  // 2️⃣ Apply request tracing — every request gets X-Request-ID
  app.use(tracingMiddleware);

  // 3️⃣ Load middlewares (JSON parser, URL parser, etc.)
  loadMiddlewares(app);

  // 4️⃣ Connect Database
  await connectDB();

  // 5️⃣ Load all API routes under /api
  app.use("/api", routes);

  // 6️⃣ Global error handler (last middleware)
  app.use(errorMiddleware);

  return app;
}
