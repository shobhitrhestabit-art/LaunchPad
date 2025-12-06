// src/middlewares/security.js
import helmet from "helmet";
import cors from "cors";
import rateLimit from "express-rate-limit";
import express from "express";

export function applySecurity(app) {

  // Security headers
  app.use(helmet());

  // Body size limits
  app.use(express.json({ limit: "100kb" }));
  app.use(express.urlencoded({ extended: false, limit: "100kb" }));

  // CORS — update with your frontend origin
  app.use(
    cors({
      origin: ["http://localhost:3000"],
      methods: ["GET", "POST", "PUT", "DELETE"],
      credentials: true
    })
  );

  // Global rate limiting
  const limiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 100,
    message: { error: "Too many requests, try again later." },
    standardHeaders: true,
    legacyHeaders: false,
  });

  app.use(limiter);
}
