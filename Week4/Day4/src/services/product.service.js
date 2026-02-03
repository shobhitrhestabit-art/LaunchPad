// src/services/product.service.js

import ProductRepository from "../repositories/product.repository.js";
import { NotFoundError, BadRequestError } from "../utils/errors.js";

const list = async (qb) => {
  const { filter, sort, pagination } = qb;
  return ProductRepository.findPaginated({
    filter,
    sort,
    page: pagination.page,
    limit: pagination.limit
  });
};

const create = async (payload) => {
  if (!payload.title) {
    throw new BadRequestError("Title is required");
  }

  return ProductRepository.create(payload);
};

const getById = async (id, includeDeleted = false) => {
  const doc = await ProductRepository.findById(id, includeDeleted);
  if (!doc) throw new NotFoundError("Product not found");
  return doc;
};

const update = async (id, payload) => {
  const doc = await ProductRepository.update(id, payload);
  if (!doc) throw new NotFoundError("Product not found");
  return doc;
};

const remove = async (id) => {
  const doc = await ProductRepository.softDelete(id);
  if (!doc) throw new NotFoundError("Product not found");
  return doc;
};

export default {
  list,
  create,
  getById,
  update,
  remove
};
