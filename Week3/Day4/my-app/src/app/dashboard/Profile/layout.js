export const metadata = {
  title: "Profile",
  description: "Profile section",
};

export default function ProfileLayout({ children }) {
  return (
    <div className="flex flex-col">
      {children}
    </div>
  );
}
