// src/middlewares/error.middleware.js

export default function errorMiddleware(err, req, res, next) {
  const status = err.statusCode || 500;
  const code = err.code || "SERVER_ERROR";

  res.status(status).json({
    success: false,
    message: err.message || "Internal Server Error",
    code,
    timestamp: new Date().toISOString(),
    path: req.originalUrl
  });
}
