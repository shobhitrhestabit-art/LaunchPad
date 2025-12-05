import Link from "next/link";

export default function Sidebar() {
  return (
    <aside className="w-64 h-screen bg-gray-900 text-gray-300 px-4 py-6 flex flex-col">

      {/* CORE */}
      <div>
        <h2 className="text-xs font-semibold text-gray-500 mb-2">CORE</h2>
        <Link
          href="/dashboard"
          className="flex items-center gap-3 px-2 py-2 rounded hover:bg-gray-800 hover:text-white"
        >
          
          <span className="text-sm">Dashboard</span>
        </Link>
      </div>

      {/* INTERFACE */}
      <div className="mt-6">
        <h2 className="text-xs font-semibold text-gray-500 mb-2">INTERFACE</h2>

        <Link
          href="/layouts"
          className="flex items-center gap-3 px-2 py-2 rounded hover:bg-gray-800 hover:text-white"
        >
         
          <span className="text-sm">Layouts</span>
        </Link>

        <Link
          href="/pages"
          className="flex items-center gap-3 px-2 py-2 rounded hover:bg-gray-800 hover:text-white"
        >
          
          <span className="text-sm">Pages</span>
        </Link>
      </div>

      {/* ADDONS */}
      <div className="mt-6">
        <h2 className="text-xs font-semibold text-gray-500 mb-2">ADDONS</h2>

        <Link
          href="/charts"
          className="flex items-center gap-3 px-2 py-2 rounded hover:bg-gray-800 hover:text-white"
        >
          
          <span className="text-sm">Charts</span>
        </Link>

        <Link
          href="/tables"
          className="flex items-center gap-3 px-2 py-2 rounded hover:bg-gray-800 hover:text-white"
        >
         
          <span className="text-sm">Tables</span>
        </Link>
      </div>
    </aside>
  );
}
