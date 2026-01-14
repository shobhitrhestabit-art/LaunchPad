const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());

mongoose.connect(process.env.MONGO_URI);

const TodoSchema = new mongoose.Schema({
  text: String
});
const Todo = mongoose.model("Todo", TodoSchema);


app.get("/health", (req, res) => {
  res.status(200).send("OK");
});


app.get("/api/todos", async (req, res) => {
  res.json(await Todo.find());
});

app.post("/api/todos", async (req, res) => {
  const todo = await Todo.create({ text: req.body.text });
  res.json(todo);
});

app.delete("/api/todos/:id", async (req, res) => {
  await Todo.findByIdAndDelete(req.params.id);
  res.sendStatus(204);
});

app.listen(process.env.PORT, () =>
  console.log("Backend running on port", process.env.PORT)
);
