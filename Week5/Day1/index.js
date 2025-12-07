
const express = require("express");
const app = express();

app.get("/", (req, res) => {
  res.send("Node app running inside Docker container!");
});

app.listen(3000, () => {
  console.log("Server running on port 3000");
});
