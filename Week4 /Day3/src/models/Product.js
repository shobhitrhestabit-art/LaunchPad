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
status: { type: String, enum: ["active", "draft", "archived"], default: "active" },
category: { type: String, index: true },
reviews: [reviewSchema], // embedded small reviews example
createdAt: { type: Date, default: Date.now },
deleted: { type: Boolean, default: false },
deletedAt: { type: Date, default: null }

},
{
toJSON: { virtuals: true },
toObject: { virtuals: true }
}
);


// Virtual computedRating (average)
productSchema.virtual("computedRating").get(function () {
if (!this.reviews || this.reviews.length === 0) return 0;
const sum = this.reviews.reduce((acc, r) => acc + r.rating, 0);
return Math.round((sum / this.reviews.length) * 10) / 10; // rounded to 1 decimal
});


// Compound index for typical queries
productSchema.index({ status: 1, createdAt: -1 });


// Example TTL index for a "flashSaleEndsAt" field (uncomment to use)
// productSchema.index({ flashSaleEndsAt: 1 }, { expireAfterSeconds: 0 });


const Product = mongoose.model("Product", productSchema);
export default Product;