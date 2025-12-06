import routes from "../routes/index.js";
import logger from "../utils/logger.js";

export default function loadRoutes(app) {
  app.use("/api", routes);

  // Count endpoints
  let count = 0;
  routes.stack.forEach((layer) => {
    if (layer.route) count++;
  });

  logger.info(`✔ Routes mounted: ${count} endpoints`);
}
