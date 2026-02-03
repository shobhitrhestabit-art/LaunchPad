// src/controllers/product.controller.js

import ProductService from "../services/product.service.js";
import { buildQueryFromParams } from "../utils/queryBuilder.js";

const list = async (req, res, next) => {
  try {
    // Build dynamic filters + sorting + pagination
    const qb = buildQueryFromParams(req.query);

    // Support cursor pagination
    if (req.query.afterId) {
      const result = await ProductService.listWithCursor({
        afterId: req.query.afterId,
        limit: qb.pagination.limit,
        filter: qb.filter,
        sort: qb.sort
      });
      return res.json(result);
    }

    // Normal pagination
    const result = await ProductService.list(qb);
    res.json(result);

  } catch (err) {
    next(err);
  }
};

const create = async (req, res, next) => {
  try {
    const result = await ProductService.create(req.body);
    res.status(201).json(result);
  } catch (err) {
    next(err);
  }
};

const getById = async (req, res, next) => {
  try {
    const includeDeleted = req.query.includeDeleted === "true";
    const result = await ProductService.getById(req.params.id, includeDeleted);
    res.json(result);
  } catch (err) {
    next(err);
  }
};

const update = async (req, res, next) => {
  try {
    const result = await ProductService.update(req.params.id, req.body);
    res.json(result);
  } catch (err) {
    next(err);
  }
};

const remove = async (req, res, next) => {
  try {
    const result = await ProductService.remove(req.params.id); // soft delete
    res.json({ message: "Deleted", data: result });
  } catch (err) {
    next(err);
  }
};

export default {
  list,
  create,
  getById,
  update,
  remove
};
