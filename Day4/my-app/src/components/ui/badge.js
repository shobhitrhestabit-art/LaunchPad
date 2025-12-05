export default function Badge({ children }) {
  return (
    <span className="inline-block px-3 py-1 text-sm rounded-full bg-gray-200 text-gray-700">
      {children}
    </span>
  );
}
