import mongoose from "mongoose";
import config from "../config/index.js";
import logger from "../utils/logger.js";

export default async function connectDB() {
  try {
    console.log("🔍 Connecting to:", config.dbUrl); // debug

    await mongoose.connect(config.dbUrl, {
      serverSelectionTimeoutMS: 15000
    });

    logger.info("✔ Database connected");
  } catch (err) {
    logger.error("❌ Database connection failed");
    console.log("🔻 FULL ERROR BELOW:");
    console.error(err);   // <--- PRINT FULL ERROR (THIS IS WHAT I NEED)
  }
}
