import { v4 as uuidv4 } from "uuid";

export default function tracingMiddleware(req, res, next) {
  const headerKey = "x-request-id";

  // If client sends an existing ID → reuse it
  const incomingId = req.headers[headerKey];

  // Otherwise generate a new request ID
  const requestId = incomingId || uuidv4();

  // Attach to req object
  req.requestId = requestId;

  // Add to response headers
  res.setHeader("X-Request-ID", requestId);

  console.log(` Request Started → ID: ${requestId} | ${req.method} ${req.originalUrl}`);

  // When response ends, log completion
  res.on("finish", () => {
    console.log(` Request Ended → ID: ${requestId} | Status: ${res.statusCode}`);
  });

  next();
}
