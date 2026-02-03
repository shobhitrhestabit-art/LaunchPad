// src/routes/user.routes.js

import { Router } from "express";
import UserController from "../controllers/user.controller.js";

import { validateSchema } from "../middlewares/validate.js";
import { userCreateSchema } from "../models/User.validation.js";

const router = Router();

// CREATE user (with schema validation)
router.post("/", validateSchema({ body: userCreateSchema }), UserController.create);

// READ all users
router.get("/", UserController.list);

// READ single user
router.get("/:id", UserController.getById);

// UPDATE user
router.put("/:id", UserController.update);

// DELETE user
router.delete("/:id", UserController.remove);

export default router;
