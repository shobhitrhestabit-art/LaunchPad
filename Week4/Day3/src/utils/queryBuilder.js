// src/utils/queryBuilder.js

function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

export function buildQueryFromParams(q = {}) {
  const {
    search,
    minPrice,
    maxPrice,
    tags,
    mode = "or",
    sort,
    includeDeleted = "false",
    page = 1,
    limit = 10
  } = q;

  const filter = {};

  // Soft delete
  if (includeDeleted !== "true") {
    filter.deleted = false;
  }

  // Price range
  if (minPrice || maxPrice) {
    filter.price = {};
    if (minPrice) filter.price.$gte = Number(minPrice);
    if (maxPrice) filter.price.$lte = Number(maxPrice);
  }

  // Tags
  if (tags) {
    filter.tags = { $in: tags.split(",") };
  }

  // WORD SEARCH using regex
  if (search) {
    const tokens = search.split(/\s+/).map(t => escapeRegex(t));

    if (mode === "and") {
      filter.$and = tokens.map(t => ({
        $or: [
          { title: { $regex: t, $options: "i" } },
          { description: { $regex: t, $options: "i" } }
        ]
      }));
    } else {
      filter.$or = tokens.flatMap(t => [
        { title: { $regex: t, $options: "i" } },
        { description: { $regex: t, $options: "i" } }
      ]);
    }
  }

  // Sorting
  let sortObj = {};
  if (sort) {
    const [field, dir] = sort.split(":");
    sortObj[field] = dir === "desc" ? -1 : 1;
  } else {
    sortObj.createdAt = -1;
  }

  return {
    filter,
    sort: sortObj,
    pagination: {
      page: Number(page),
      limit: Number(limit),
      skip: (Number(page) - 1) * Number(limit)
    }
  };
}
