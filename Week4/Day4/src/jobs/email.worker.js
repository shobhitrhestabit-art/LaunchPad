import { Worker } from "bullmq";
import { connection } from "./redis.js";

// WORKER PROCESSING LOGIC
const worker = new Worker(
  "emailQueue",
  async job => {
    console.log("Job started:", job.id);

    // Fake email sending logic
    await new Promise(resolve => setTimeout(resolve, 2000)); // simulate slow task

    console.log(` Email sent to ${job.data.to}`);
    console.log(" Job finished:", job.id);

    return { status: "success" };
  },
  { connection }
);

// EVENT LISTENERS FOR DEBUGGING
worker.on("completed", job => {
  console.log(` Job ${job.id} completed`);
});

worker.on("failed", (job, err) => {
  console.error(` Job ${job.id} failed: ${err.message}`);
});

worker.on("stalled", jobId => {
  console.error(`q Job ${jobId} stalled`);
});
