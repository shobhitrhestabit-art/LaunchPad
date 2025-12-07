const express = require("express");
const mongoose = require("mongoose");

const app = express();
const PORT = 5000;

const mongoUrl = process.env.MONGO_URL || "mongodb://mongo:27017/mydb";

mongoose
  .connect(mongoUrl)
  .then(() => console.log("MongoDB Connected"))
  .catch((err) => console.log("Mongo Error:", err));

app.get("/", (req, res) => {
  res.json({ message: "Hello from Node Server" });
});

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
