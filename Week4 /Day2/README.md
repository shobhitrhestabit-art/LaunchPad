   # Day2  -Database Modeling, Indexing & Advanced CRUD


   ### This project implements MongoDB schema design, Mongoose hooks, indexes, repository pattern, and pagination strategies using Node.js, Express, and Mongoose.


   ---

   # Project Structure 

   ![Structure](ScreenShot/Indexes/Structure.png)

   ---

   ## Features Implemented

### 1. Schema Design
- User model with validations and transformations  
- Product model  
- Timestamps (createdAt, updatedAt)  
- Indexing support (unique, sparse, compound, TTL)

### 2. Mongoose Features
- Pre-save hooks  
- Virtual fields  
- Compound indexes  
- Sparse + unique indexes  
- Optional TTL index

### 3. Repository Pattern

UserRepository:
- `create()`
- `findById()`
- `findPaginated()`
- `findPaginatedCursor()`
- `update()`
- `delete()`

ProductRepository:
- Same set of methods

### 4. Pagination
- Skip/Limit pagination  
- Cursor-based pagination (afterId)

---

## Index Screenshots

__user Index__
![index](ScreenShot/Indexes/useres_index.png)


__Product Index__

![index](ScreenShot/Indexes/products_index.png)


---

## Summary

This project includes:

- MongoDB schema modeling  
- Indexing strategies  
- Repository architecture  
- Pagination (skip + cursor)  
- Mongoose hooks & virtuals  
- Clean Node.js/Express structure  




   