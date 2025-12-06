import ProductRepository from "../repositories/product.repository.js";

const list = async (req, res, next) => {
  try {
    const { page, limit, afterId } = req.query;

    // Cursor Pagination
    if (afterId) {
      const { data, nextCursor } =
        await ProductRepository.findPaginatedCursor({
          afterId,
          limit: Number(limit) || undefined,
        });

      return res.json({ data, nextCursor });
    }

    // Skip/Limit Pagination
    const result = await ProductRepository.findPaginated({
      page: Number(page) || 1,
      limit: Number(limit) || 10,
    });

    res.json(result);
  } catch (err) {
    next(err);
  }
};

const create = async (req, res, next) => {
  try {
    const doc = await ProductRepository.create(req.body);
    res.status(201).json(doc);
  } catch (err) {
    next(err);
  }
};

const getById = async (req, res, next) => {
  try {
    const doc = await ProductRepository.findById(req.params.id);
    if (!doc) return res.status(404).json({ message: "Not found" });

    res.json(doc);
  } catch (err) {
    next(err);
  }
};

const update = async (req, res, next) => {
  try {
    const doc = await ProductRepository.update(req.params.id, req.body);
    if (!doc) return res.status(404).json({ message: "Not found" });

    res.json(doc);
  } catch (err) {
    next(err);
  }
};

const remove = async (req, res, next) => {
  try {
    const doc = await ProductRepository.delete(req.params.id);

    if (!doc) return res.status(404).json({ message: "Not found" });

    res.json({ message: "Deleted" });
  } catch (err) {
    next(err);
  }
};

export default { list, create, getById, update, remove };
