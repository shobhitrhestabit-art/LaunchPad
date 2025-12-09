const express = require("express");
const path = require("path");

const app = express();

// Serve static frontend files
app.use(express.static(path.join(__dirname, "public")));

// API example
app.get("/api/time", (req, res) => {
  res.json({ time: new Date().toLocaleString() });
});

app.listen(3000, () => console.log("Backend running on port 3000"));
