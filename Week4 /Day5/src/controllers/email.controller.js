import { addEmailJob } from "../jobs/email.queue.js";

export const sendEmail = async (req, res, next) => {
  try {
    // Log when request starts processing
    console.log(`[${req.requestId}] Queuing email for ${req.body.to}`);

    // Add job + attach traceId for worker logs
    await addEmailJob({
      ...req.body,
      traceId: req.requestId
    });

    // Log after job is queued
    console.log(`[${req.requestId}] Email job added to queue`);

    res.json({
      success: true,
      message: "Email job queued successfully"
    });

  } catch (err) {
    next(err);
  }
};
