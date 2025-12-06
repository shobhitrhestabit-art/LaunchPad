import express from "express";
import cors from "cors";

export default function loadMiddlewares(app) {
  app.use(express.json());
  app.use(cors());
}
