export default function Navbar() {
  return (
    <div className="w-full bg-white shadow p-4">
      <div className="flex justify-between items-center max-w-7xl mx-auto">
        
        {/* Left Side (Logo or Title) */}
        <h1 className="text-xl font-semibold">MyApp</h1>

        {/* Right Side Search Bar */}
        <div className="flex items-center border border-gray-300 rounded-full px-4 py-2 w-72">
          <input
            type="text"
            placeholder="Search..."
            className="w-full outline-none"
          />
        </div>
      </div>
    </div>
  );
}
