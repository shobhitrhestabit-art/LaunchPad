// src/middlewares/error.middleware.js

import logger from "../utils/logger.js";
import { AppError } from "../utils/errors.js";

export default function errorMiddleware(err, req, res, next) {
  // Log everything (safe)
  try {
    logger.error(`${err?.message || "Unknown error"} - ${req.method} ${req.originalUrl}`);
  } catch {
    console.error("Logger failed. Error:", err);
  }

  // 1️⃣ Custom AppError (NotFoundError, BadRequestError, etc.)
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      success: false,
      message: err.message,
      code: err.code,
      timestamp: new Date().toISOString(),
      path: req.originalUrl,
    });
  }

  // 2️⃣ Zod validation error (if it was not caught earlier)
  if (err?.name === "ZodError" || Array.isArray(err?.issues)) {
    return res.status(400).json({
      success: false,
      message: "Validation failed",
      details: err.issues || [],
      code: "VALIDATION_ERROR",
      timestamp: new Date().toISOString(),
      path: req.originalUrl,
    });
  }

  // 3️⃣ MongoDB errors (optional improvement)
  if (err?.name === "MongoError" || err?.code === 11000) {
    return res.status(400).json({
      success: false,
      message: "Database error",
      code: "DB_ERROR",
      timestamp: new Date().toISOString(),
      path: req.originalUrl,
    });
  }

  // 4️⃣ Unexpected error fallback
  return res.status(500).json({
    success: false,
    message: err?.message || "Internal Server Error",
    code: "SERVER_ERROR",
    timestamp: new Date().toISOString(),
    path: req.originalUrl,
  });
}
