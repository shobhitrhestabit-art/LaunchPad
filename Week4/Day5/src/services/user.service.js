// src/services/user.service.js

import UserRepository from "../repositories/user.repository.js";
import { NotFoundError, BadRequestError } from "../utils/errors.js";

const list = async ({ page = 1, limit = 10, afterId = null }) => {
  // Cursor pagination
  if (afterId) {
    return UserRepository.findPaginatedCursor({
      afterId,
      limit,
    });
  }

  // Normal skip/limit pagination
  return UserRepository.findPaginated({
    page,
    limit,
  });
};

const create = async (payload) => {
  if (!payload.firstName || !payload.lastName) {
    throw new BadRequestError("First name and last name are required");
  }

  // Email exists? (business logic)
  // check using repository
  // OPTIONAL improvement later

  return await UserRepository.create(payload);
};

const getById = async (id) => {
  const user = await UserRepository.findById(id);
  if (!user) throw new NotFoundError("User not found");
  return user;
};

const update = async (id, payload) => {
  const updated = await UserRepository.update(id, payload);
  if (!updated) throw new NotFoundError("User not found");
  return updated;
};

const remove = async (id) => {
  const deleted = await UserRepository.delete(id);
  if (!deleted) throw new NotFoundError("User not found");
  return deleted;
};

export default {
  list,
  create,
  getById,
  update,
  remove,
};
