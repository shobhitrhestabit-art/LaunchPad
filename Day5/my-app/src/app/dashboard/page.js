import Card from "../../components/ui/card";
import AreaChart from "../../components/ui/AreaChart";
import BarChart from "../../components/ui/BarChart";
// import Card from "../../components/ui/card";



export default function DashboardPage() {
  return (
    <div className="flex flex-col space-y-6 w-full">

      {/* Dashboard Title */}
      <h1 className="text-4xl font-bold">Dashboard</h1>

      {/* Breadcrumb */}
      <div className="bg-gray-100 rounded p-3 text-gray-600">
        Dashboard
      </div>

      {/* CARDS SECTION */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card title="Primary Card" color="bg-blue-600">
           <button className="underline text-sm">View Details →</button>
        </Card>

        <Card title="Warning Card" color="bg-yellow-500">
            <button className="underline text-sm">View Details →</button>
        </Card>

        <Card title="Success Card" color="bg-green-500">
            <button className="underline text-sm">View Details →</button>
        </Card>

<Card title="Danger Card" color="bg-red-600">
  <button className="underline text-sm">View Details →</button>
</Card>

        

      </div>


      {/* CHARTS SECTION */}
      {/* CHARTS SECTION */}

      {/* CHARTS SECTION */}
<div className="grid grid-cols-1 md:grid-cols-2 gap-6">

  {/* Area Chart */}
  <Card color="bg-white">
    <h3 className="font-semibold mb-3 text-black">📈 Area Chart Example</h3>
    <AreaChart />
  </Card>

  {/* Bar Chart */}
  <Card color="bg-white">
    <h3 className="font-semibold mb-3 text-black">📊 Bar Chart Example</h3>
    <BarChart />
  </Card>

</div>



      

        

     

    </div>
  );
}
