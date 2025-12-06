import dotenv from "dotenv";
import fs from "fs";
import path from "path";

export function loadEnv() {
  const env = process.env.NODE_ENV || "3000"; // default "local"

  const filePath = path.resolve(process.cwd(), `.env.${env}`);

  if (fs.existsSync(filePath)) {
    dotenv.config({ path: filePath });
    console.log(`Loaded .env.${env}`);
  } else {
    console.log(`Environment file not found: .env.${env}`);
  }

  return env;
}
