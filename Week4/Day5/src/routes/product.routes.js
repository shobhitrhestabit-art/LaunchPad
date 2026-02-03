// src/routes/product.routes.js

import { Router } from "express";
import ProductController from "../controllers/product.controller.js";

import { validateSchema } from "../middlewares/validate.js";
import { productCreateSchema } from "../models/Product.validation.js";

const router = Router();

// CREATE product (with validation)
router.post("/", validateSchema({ body: productCreateSchema }), ProductController.create);

// READ all products
router.get("/", ProductController.list);

// READ by ID
router.get("/:id", ProductController.getById);

// UPDATE product
router.put("/:id", ProductController.update);

// DELETE product
router.delete("/:id", ProductController.remove);

export default router;
