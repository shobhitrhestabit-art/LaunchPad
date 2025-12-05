export const metadata = {
  title: "Dashboard",
  description: "Dashboard section pages",
};

export default function DashboardLayout({ children }) {
  return (
    <div className="flex flex-col space-y-6 w-full text-black">
      {children}
    </div>
  );
}
