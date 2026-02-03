import { createApp } from "./loaders/app.js";
import config from "./config/index.js";
import logger from "./utils/logger.js";

const startServer = async () => {
  const app = await createApp();

  app.listen(config.port, () => {
    logger.info(`✔ Server started on port ${config.port}`);
  });
};

startServer();
