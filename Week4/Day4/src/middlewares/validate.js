// src/middlewares/validate.js
import { ZodError } from "zod";

export const validateSchema = (schemaObject = {}) => {
  return (req, res, next) => {
    try {
      if (schemaObject.params) {
        req.params = schemaObject.params.parse(req.params);
      }
      if (schemaObject.query) {
        req.query = schemaObject.query.parse(req.query);
      }
      if (schemaObject.body) {
        req.body = schemaObject.body.parse(req.body);
      }
      next();
    } catch (err) {
      // ZOD validation error
      if (err instanceof ZodError) {
        return res.status(400).json({
          success: false,
          error: "Validation failed",
          details: err.errors.map(e => ({
            path: e.path.join("."),
            message: e.message
          }))
        });
      }

      // NON-ZOD error fallback
      return res.status(400).json({
        success: false,
        error: err.message || "Invalid input format"
      });
    }
  };
};
