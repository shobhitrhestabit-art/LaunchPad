export default function Navbar() {
  return (
    <nav className="h-[100px] w-full bg-gray-800 shadow flex items-center justify-between px-8">

      {/* LEFT SIDE */}
      <h1 className="text-2xl font-semibold text-white tracking-wide">
        Start Bootstrap
      </h1>

      {/* RIGHT SIDE */}
      <div className="flex items-center gap-4">

        {/* Search Input */}
        <input
          type="search"
          placeholder="Search..."
          className="border border-gray-600 bg-gray-700 text-white rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        {/* Button */}
        <button className="bg-blue-600 text-white px-5 py-2 rounded hover:bg-blue-700 transition">
          Button
        </button>

      </div>

    </nav>
  );
}
