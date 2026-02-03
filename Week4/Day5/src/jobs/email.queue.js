import {Queue} from "bullmq";
import {connection} from "./redis.js";

export const emailQueue = new Queue("emailQueue",{ connection });//creating emailQueue here using Queue class


export async function addEmailJob({ to, subject, message }) {
  await emailQueue.add("sendEmail", 
    { to, subject, message },
    {
      attempts: 3,         // retry 3 times
      backoff: {
        type: "exponential",
        delay: 3000        // 3 seconds delay before retry
      },
      removeOnComplete: true,
      removeOnFail: false
    }
  );
  console.log("📩 Email job added to queue");
}