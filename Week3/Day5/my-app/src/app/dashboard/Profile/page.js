import Link from "next/link";
import Image from "next/image";
import Button from "@/components/ui/button";

export default function profilePage(){//exporting children is mandatory
   return (
     <div className="m-6 h-screen">
  {/* Back Link */}
  <div className="text-left">
    <Link href="/" className="text-blue-600 underline">
      GO Back
    </Link>
  </div>

  {/* OUTER CARD */}
  <div className="border border-gray-300 mt-4 bg-transparent p-6 rounded-lg">
    
    {/* FLEX CONTAINER */}
    <div className="flex gap-6">
      
      {/* IMAGE */}
      <Image
        src="https://i.pinimg.com/736x/c2/e4/5a/c2e45a2e8954e589342a8b66c19198c2.jpg"
        width={300}
        height={400}
        alt="pic"
        className="border border-gray-100 rounded-lg"
      />

      {/* RIGHT CONTENT */}
      <div className="w-full">
        
        <div className="border border-gray-300 rounded-lg p-6 bg-white">
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            {/* LEFT COLUMN */}
            <div className="space-y-6">
              <div>
                <p className="text-gray-500 text-sm">Name</p>
                <p className="text-lg font-semibold">Courage</p>
                <hr className="mt-2" />
              </div>

              <div>
                <p className="text-gray-500 text-sm">Job Title</p>
                <p className="text-lg font-semibold">Guard</p>
                <hr className="mt-2" />
              </div>

              <div>
                <p className="text-gray-500 text-sm">Email</p>
                <p className="text-blue-600 underline">coward@example.com</p>
                <hr className="mt-2" />
              </div>
            </div>

            {/* RIGHT COLUMN */}
            <div className="space-y-6">
              <div>
                <p className="text-gray-500 text-sm">LinkedIn</p>
                <p className="text-blue-600 underline">linkedin.com</p>
                <hr className="mt-2" />
              </div>

              <div>
                <p className="text-gray-500 text-sm">Twitter</p>
                <p className="text-blue-600 underline">www.x.com</p>
                <hr className="mt-2" />
              </div>

              <div>
                <p className="text-gray-500 text-sm">Facebook</p>
                <p className="text-blue-600 underline">facebook.com</p>
                <hr className="mt-2" />
              </div>
            </div>

          </div>

        </div>

      </div>
    </div>
    <div className="h-[1px] w-full bg-gray-300 mt-1"></div>

    <div className="p-3">
      <span>Bio</span>
      <p>Courage the Cowardly Dog is a timid yet incredibly brave pink dog who lives with Muriel and Eustace in a lonely farmhouse in Nowhere. Though easily frightened, Courage always finds the strength to face terrifying monsters, supernatural creatures, and mysterious events to protect the people he loves. His mix of fear and courage makes him both funny and inspiring—showing that true bravery isn’t the absence of fear, but the willingness to act even when you’re scared. Despite all the bizarre dangers that come their way, Courage never gives up, proving that even the smallest and most frightened among us can be heroes.

      </p>
    </div>

    <div className="h-[1px] w-full bg-gray-300 mt-1"></div>
    <Link href="" className="underline text-small p-1 text-blue-500 mt-2">Edit Profile</Link>
    


    <div>
      
    </div>

  </div>

</div>

   );
}