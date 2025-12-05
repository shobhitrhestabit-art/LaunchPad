"use client";
export default function NavButton({
  children,
  onClick = () => {},
  disabled = false,
  active = false,
}) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`
        px-4 py-2 border rounded-lg text-sm
        transition
        ${active ? "bg-gray-200 font-semibold" : "bg-white"}
        ${disabled ? "opacity-40 cursor-not-allowed" : "hover:bg-gray-100"}
      `}
    >
      {children}
    </button>
  );
}
