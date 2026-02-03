import UserService from "../services/user.service.js";

const list = async (req, res, next) => {
  try {
    console.log(`[${req.requestId}] Fetching users list`);

    const { page, limit, afterId } = req.query;

    const result = await UserService.list({
      page: Number(page) || 1,
      limit: Number(limit) || 10,
      afterId
    });

    console.log(
      `[${req.requestId}] Users list returned count=${result.data?.length || 0}`
    );

    res.json(result);
  } catch (err) {
    console.error(`[${req.requestId}] Error in list:`, err.message);
    next(err);
  }
};

const create = async (req, res, next) => {
  try {
    console.log(`[${req.requestId}] Creating a new user`);

    const user = await UserService.create(req.body);

    console.log(`[${req.requestId}] User created: ${user._id}`);

    res.status(201).json(user);
  } catch (err) {
    console.error(`[${req.requestId}] Error in create:`, err.message);
    next(err);
  }
};

const getById = async (req, res, next) => {
  try {
    console.log(`[${req.requestId}] Fetching user ${req.params.id}`);

    const user = await UserService.getById(req.params.id);

    console.log(`[${req.requestId}] User returned: ${user._id}`);

    res.json(user);
  } catch (err) {
    console.error(`[${req.requestId}] Error in getById:`, err.message);
    next(err);
  }
};

const update = async (req, res, next) => {
  try {
    console.log(`[${req.requestId}] Updating user ${req.params.id}`);

    const updatedUser = await UserService.update(req.params.id, req.body);

    console.log(`[${req.requestId}] User updated: ${updatedUser._id}`);

    res.json(updatedUser);
  } catch (err) {
    console.error(`[${req.requestId}] Error in update:`, err.message);
    next(err);
  }
};

const remove = async (req, res, next) => {
  try {
    console.log(`[${req.requestId}] Removing user ${req.params.id}`);

    const deletedUser = await UserService.remove(req.params.id);

    console.log(`[${req.requestId}] User removed: ${deletedUser._id}`);

    res.json({
      message: "Deleted",
      data: deletedUser
    });
  } catch (err) {
    console.error(`[${req.requestId}] Error in remove:`, err.message);
    next(err);
  }
};

export default { list, create, getById, update, remove };
