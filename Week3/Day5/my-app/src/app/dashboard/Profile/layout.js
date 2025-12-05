export const metadata = {
  title: "Profile",
  description: "Profile section",
};

export default function ProfileLayout({ children }) {
  return (
    <div className="bg-white p-1">
      {children}
    </div>
  );
}
