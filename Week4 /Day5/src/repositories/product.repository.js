import Product from "../models/Product.js";
import mongoose from "mongoose";

const defaultLimit = 10;

export const ProductRepository = {
  // ⭐ Create
  async create(payload) {
    const doc = await Product.create(payload);
    return doc;
  },

  // ⭐ Updated findById with includeDeleted support
  async findById(id, includeDeleted = false) {
    if (!mongoose.Types.ObjectId.isValid(id)) return null;

    const filter = includeDeleted
      ? { _id: id }
      : { _id: id, deleted: false };

    return Product.findOne(filter).exec();
  },

  // ⭐ Skip/Limit Pagination
  async findPaginated({ page = 1, limit = defaultLimit, filter = {}, sort = { createdAt: -1 } } = {}) {
    const skip = (page - 1) * limit;

    const [data, total] = await Promise.all([
      Product.find(filter)
        .sort(sort)
        .skip(skip)
        .limit(limit)
        .exec(),

      Product.countDocuments(filter)
    ]);

    return {
      data,
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit)
    };
  },

  // ⭐ Cursor Pagination
  async findPaginatedCursor({ afterId = null, limit = defaultLimit, filter = {} } = {}) {
    const query = { ...filter };

    if (afterId && mongoose.Types.ObjectId.isValid(afterId)) {
      query._id = { $gt: afterId };
    }

    const data = await Product.find(query)
      .sort({ _id: 1 })
      .limit(limit)
      .exec();

    const nextCursor = data.length ? data[data.length - 1]._id : null;

    return { data, nextCursor };
  },

  // ⭐ Update
  async update(id, payload) {
    if (!mongoose.Types.ObjectId.isValid(id)) return null;

    return Product.findByIdAndUpdate(
      id,
      payload,
      { new: true, runValidators: true }
    ).exec();
  },

  // ⭐ HARD DELETE (rarely used)
  async delete(id) {
    if (!mongoose.Types.ObjectId.isValid(id)) return null;
    return Product.findByIdAndDelete(id).exec();
  },

  // ⭐ SOFT DELETE (Day-3 requirement)
  async softDelete(id) {
    if (!mongoose.Types.ObjectId.isValid(id)) return null;

    return Product.findByIdAndUpdate(
      id,
      { deleted: true, deletedAt: new Date() },
      { new: true }
    ).exec();
  },

  // ⭐ Helper for service
  isValidObjectId(id) {
    return mongoose.Types.ObjectId.isValid(id);
  }
};

export default ProductRepository;
