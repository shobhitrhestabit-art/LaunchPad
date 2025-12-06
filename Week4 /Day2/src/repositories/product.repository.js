import Product from "../models/Product.js";
import mongoose from "mongoose";


const defaultLimit = 10;


export const ProductRepository = {
async create(payload) {
const doc = await Product.create(payload);
return doc;
},


async findById(id) {
if (!mongoose.Types.ObjectId.isValid(id)) return null;
return Product.findById(id).exec();
},


async findPaginated({ page = 1, limit = defaultLimit, filter = {} } = {}) {
const skip = (page - 1) * limit;
const [data, total] = await Promise.all([
Product.find(filter).sort({ createdAt: -1 }).skip(skip).limit(limit).exec(),
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


async findPaginatedCursor({ afterId = null, limit = defaultLimit, filter = {} } = {}) {
const query = { ...filter };
if (afterId && mongoose.Types.ObjectId.isValid(afterId)) {
query._id = { $gt: afterId };
}


const data = await Product.find(query).sort({ _id: 1 }).limit(limit).exec();
const nextCursor = data.length ? data[data.length - 1]._id : null;


return { data, nextCursor };
},


async update(id, payload) {
if (!mongoose.Types.ObjectId.isValid(id)) return null;
return Product.findByIdAndUpdate(id, payload, { new: true, runValidators: true }).exec();
},


async delete(id) {
if (!mongoose.Types.ObjectId.isValid(id)) return null;
return Product.findByIdAndDelete(id).exec();
}
};


export default ProductRepository;