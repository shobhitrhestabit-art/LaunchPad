import User from "../models/User.js";
import mongoose from "mongoose";


const defaultLimit = 10;


export const UserRepository = {
async create(payload) {
const doc = await User.create(payload);
return doc;
},


async findById(id) {
if (!mongoose.Types.ObjectId.isValid(id)) return null;
return User.findById(id).exec();
},


// Offset-based pagination (skip/limit)
async findPaginated({ page = 1, limit = defaultLimit, filter = {} } = {}) {
const skip = (page - 1) * limit;
const [data, total] = await Promise.all([
User.find(filter).sort({ createdAt: -1 }).skip(skip).limit(limit).exec(),
User.countDocuments(filter)
]);


return {
data,
page,
limit,
total,
totalPages: Math.ceil(total / limit)
};
},


// Cursor-based pagination using _id (afterId means fetch docs with _id > afterId)
async findPaginatedCursor({ afterId = null, limit = defaultLimit, filter = {} } = {}) {
const query = { ...filter };
if (afterId && mongoose.Types.ObjectId.isValid(afterId)) {
query._id = { $gt: afterId };
}


const data = await User.find(query).sort({ _id: 1 }).limit(limit).exec();
const nextCursor = data.length ? data[data.length - 1]._id : null;


return { data, nextCursor };
},


async update(id, payload) {
if (!mongoose.Types.ObjectId.isValid(id)) return null;
return User.findByIdAndUpdate(id, payload, { new: true, runValidators: true }).exec();
},


async delete(id) {
if (!mongoose.Types.ObjectId.isValid(id)) return null;
return User.findByIdAndDelete(id).exec();
}
};


export default UserRepository;