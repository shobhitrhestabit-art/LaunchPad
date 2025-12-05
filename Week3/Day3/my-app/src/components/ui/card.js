export default function Card({ title, color = "bg-white", children }) {
  return (
    <div className={`shadow-md rounded p-4 text-white ${color}`}>
      <h2 className="font-semibold text-lg">{title}</h2>

      {/* If children exist → render them */}
      {children && <div className="mt-3">{children}</div>}
    </div>
  );
}

