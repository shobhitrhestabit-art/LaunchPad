// src/models/Product.js

import mongoose from "mongoose";
const { Schema } = mongoose;

const reviewSchema = new Schema(
  {
    user: { type: Schema.Types.ObjectId, ref: "User" },
    rating: { type: Number, min: 1, max: 5, required: true },
    comment: String,
    createdAt: { type: Date, default: Date.now }
  },
  { _id: false }
);

const productSchema = new Schema(
  {
    title: { type: String, required: true, trim: true },
    description: String,
    price: { type: Number, required: true, min: 0 },

    // ⭐ FIXED — Added tags field
    tags: [{ type: String }],

    status: { type: String, enum: ["active", "draft", "archived"], default: "active" },
    category: { type: String, index: true },

    reviews: [reviewSchema],

    createdAt: { type: Date, default: Date.now },

    // Soft delete fields
    deleted: { type: Boolean, default: false },
    deletedAt: { type: Date, default: null }
  },
  {
    toJSON: { virtuals: true },
    toObject: { virtuals: true }
  }
);

// ⭐ Virtual – computedRating
productSchema.virtual("computedRating").get(function () {
  if (!this.reviews || this.reviews.length === 0) return 0;
  const sum = this.reviews.reduce((acc, r) => acc + r.rating, 0);
  return Math.round((sum / this.reviews.length) * 10) / 10;
});

// ⭐ Compound index
productSchema.index({ status: 1, createdAt: -1 });

const Product = mongoose.model("Product", productSchema);
export default Product;
