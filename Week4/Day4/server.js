import { createApp } from "./src/loaders/app.js";
import config from "./src/config/index.js";
import logger from "./src/utils/logger.js";

const startServer = async () => {
  const app = await createApp();

  app.listen(config.port, () => {
    logger.info(`✔ Server started on port ${config.port}`);
  });
};

startServer();
