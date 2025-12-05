"use client";

import { useState } from "react";

export default function Modal() {
  const [open, setOpen] = useState(false);

  return (
    <>
      {/* Open Modal Button */}
      <button
        onClick={() => setOpen(true)}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Open Modal
      </button>

      {/* Modal Overlay */}
      {open && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">

          {/* Modal Box */}
          <div className="bg-white p-6 rounded shadow-lg min-w-[300px]">
            <h2 className="text-lg font-semibold mb-4">Modal Title</h2>
            <p className="mb-4">This is a simple modal in Next.js</p>

            <button
              onClick={() => setOpen(false)}
              className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
            >
              Close
            </button>
          </div>

        </div>
      )}
    </>
  );
}
