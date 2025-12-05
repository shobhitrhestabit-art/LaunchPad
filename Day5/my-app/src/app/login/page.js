"use client";
import { FaUser, FaLock } from "react-icons/fa";

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 px-4">
      <div className="w-full max-w-sm bg-white p-8 rounded-xl shadow">
        
        {/* Username */}
        <div className="mb-4">
          <div className="flex items-center border rounded-lg px-4 py-3 bg-gray-50">
            <FaUser className="text-gray-400 mr-3" />
            <input
              type="text"
              placeholder="Username"
              className="w-full bg-transparent focus:outline-none"
            />
          </div>
        </div>

        {/* Password */}
        <div className="mb-4">
          <div className="flex items-center border rounded-lg px-4 py-3 bg-gray-50">
            <FaLock className="text-gray-400 mr-3" />
            <input
              type="password"
              placeholder="Password"
              className="w-full bg-transparent focus:outline-none"
            />
          </div>
        </div>

        {/* Remember Me + Forgot Password */}
        <div className="flex justify-between items-center text-sm mb-6">
          <label className="flex items-center gap-2">
            <input type="checkbox" className="accent-gray-600" />
            <span className="text-gray-700">Remember me</span>
          </label>

          <button className="text-gray-500 hover:underline">
            Forgot Password?
          </button>
        </div>

        {/* Login Button */}
        <button className="w-full bg-green-500 text-white py-3 rounded-lg hover:bg-green-600 transition font-semibold">
          LOGIN
        </button>
      </div>
    </div>
  );
}
