// src/models/Product.validation.js

import { z } from "zod";

export const productCreateSchema = z.object({
  title: z.string().min(1),
  description: z.string().optional(),
  price: z.number().nonnegative(),
  category: z.string().optional(),
  tags: z.string().optional(), // comma-separated string → will split later
});
