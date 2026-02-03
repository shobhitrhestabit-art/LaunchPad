import { Router } from "express";
import userRoutes from "./user.routes.js";
import productRoutes from "./product.routes.js";

const router = Router();

router.get("/health", (req, res) => {
  res.json({ status: "OK" });
});

router.use("/users", userRoutes);
router.use("/products", productRoutes);

export default router;
