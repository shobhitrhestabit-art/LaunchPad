const express = require("express");
const app = express();

const PORT = 3000;

app.get("/api", (req, res) => {
  res.json({
    message: "Hello from backend instance!",
    instance: process.env.INSTANCE_ID || "unknown"
  });
});

app.listen(PORT, () => {
  console.log(`Backend running on port ${PORT}`);
});
