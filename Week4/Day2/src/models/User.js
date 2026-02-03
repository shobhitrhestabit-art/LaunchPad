import mongoose from "mongoose";
import bcrypt from "bcrypt";


const { Schema } = mongoose;


const userSchema = new Schema(
{
firstName: { type: String, required: true, trim: true },
lastName: { type: String, required: true, trim: true },


email: {
type: String,
required: true,
unique: true,
sparse: true, // optional but combined with unique allows missing emails
lowercase: true,
trim: true,
match: /.+@.+\..+/
},


password: { type: String, required: true, minlength: 6 },


status: { type: String, enum: ["active", "pending", "blocked"], default: "pending" },


createdAt: { type: Date, default: Date.now }
},
{
toJSON: { virtuals: true },
toObject: { virtuals: true }
}
);


// Virtual: fullName
userSchema.virtual("fullName").get(function () {
return `${this.firstName} ${this.lastName}`;
});


// Indexes
userSchema.index({ status: 1, createdAt: -1 }); // compound index for queries like find({status}).sort({createdAt:-1})


// Example of sparse unique pattern (unique enforced only when field exists)
userSchema.index({ email: 1 }, { unique: true, sparse: true });


// Pre-save hook: hash password
userSchema.pre("save", async function (next) {
if (!this.isModified("password")) return next();
try {
const salt = await bcrypt.genSalt(10);
this.password = await bcrypt.hash(this.password, salt);
return next();
} catch (err) {
return next(err);
}
});


// Method to compare password
userSchema.methods.comparePassword = async function (candidate) {
return bcrypt.compare(candidate, this.password);
};


const User = mongoose.model("User", userSchema);
export default User;