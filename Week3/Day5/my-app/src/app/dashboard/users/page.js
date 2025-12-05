// import Searchbar from "../../../components/ui";
// import Searchbar from "@/components/ui/Searchbar";
import Searchbar from "@/components/ui/searchbar";
import NavButton from "@/components/ui/Navbutton";




export default function UsersPage(){
    return(
       <div>
        <div className="bold text-4xl md:text-4xl font-extrabold text-gray-900">Users</div>
        <div>
            <Searchbar />
        </div>
        <div className="rounded-lg">

            <div className="p-6 px-1">
      <div className="overflow-x-auto rounded-lg">
        <table className="w-full border border-gray-300 rounded-lg border-collapse">

          {/* HEADER */}
          <thead className="bg-gray-100 text-gray-600 text-sm">
            <tr>
              <th className="p-4 font-semibold text-left">Name ↓</th>
              <th className="p-4 font-semibold text-left">Email ↓</th>
              <th className="p-4 font-semibold text-left">Role ↓</th>
              <th className="p-4 font-semibold text-left">Created at</th>
              <th className="p-4 font-semibold text-left">Updated at</th>
              <th className="p-4 font-semibold text-center">Action</th>
            </tr>
          </thead>

          {/* BODY */}
          <tbody className="text-gray-700 text-sm">

            {/* Repeat rows */}
            {Array(10).fill(0).map((_, i) => (
              <tr key={i} className="hover:bg-gray-50">
                <td className="p-4">User {i + 1}</td>
                <td className="p-4">user{i}@example.com</td>
                <td className="p-4">User</td>
                <td className="p-4">18/10/2024 05:27</td>
                <td className="p-4">18/10/2024 05:27</td>
                <td className="p-4 text-center">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="purple"
                    className="w-5 h-5 inline-block"
                    viewBox="0 0 24 24"
                  >
                    <path d="M12 12c2.21 0 4-1.79 4-4S14.21 4 12 4s-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 
                      0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                  </svg>
                </td>
              </tr>
            ))}

          </tbody>

        </table>
      </div>
    </div>

    <div className="flex gap-2 flex justify-end">
      <NavButton disabled>◀</NavButton>
      <NavButton active>1</NavButton>
      <NavButton>2</NavButton>
      <NavButton>3</NavButton>
      <NavButton>▶</NavButton>
    </div>
   
            
        </div>
       </div>
    );
}