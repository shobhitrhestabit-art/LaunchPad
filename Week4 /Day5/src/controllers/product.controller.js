import ProductService from "../services/product.service.js";
import { buildQueryFromParams } from "../utils/queryBuilder.js";

const list = async (req, res, next) => {
  try {
    console.log(`[${req.requestId}] Fetching product list`);

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

      console.log(
        `[${req.requestId}] Product list (cursor) returned count=${result.data?.length || 0}`
      );

      return res.json(result);
    }

    // Normal pagination
    const result = await ProductService.list(qb);

    console.log(
      `[${req.requestId}] Product list returned count=${result.data?.length || 0}`
    );

    res.json(result);

  } catch (err) {
    console.error(`[${req.requestId}] Error in list:`, err.message);
    next(err);
  }
};

const create = async (req, res, next) => {
  try {
    console.log(`[${req.requestId}] Creating product`);

    const result = await ProductService.create(req.body);

    console.log(`[${req.requestId}] Product created: ${result._id}`);

    res.status(201).json(result);

  } catch (err) {
    console.error(`[${req.requestId}] Error in create:`, err.message);
    next(err);
  }
};

const getById = async (req, res, next) => {
  try {
    console.log(`[${req.requestId}] Fetching product ${req.params.id}`);

    const includeDeleted = req.query.includeDeleted === "true";
    const result = await ProductService.getById(req.params.id, includeDeleted);

    console.log(`[${req.requestId}] Product returned: ${result._id}`);

    res.json(result);

  } catch (err) {
    console.error(`[${req.requestId}] Error in getById:`, err.message);
    next(err);
  }
};

const update = async (req, res, next) => {
  try {
    console.log(`[${req.requestId}] Updating product ${req.params.id}`);

    const result = await ProductService.update(req.params.id, req.body);

    console.log(`[${req.requestId}] Product updated: ${result._id}`);

    res.json(result);

  } catch (err) {
    console.error(`[${req.requestId}] Error in update:`, err.message);
    next(err);
  }
};

const remove = async (req, res, next) => {
  try {
    console.log(`[${req.requestId}] Soft-deleting product ${req.params.id}`);

    const result = await ProductService.remove(req.params.id);

    console.log(`[${req.requestId}] Product soft-deleted: ${result._id}`);

    res.json({ message: "Deleted", data: result });

  } catch (err) {
    console.error(`[${req.requestId}] Error in remove:`, err.message);
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
