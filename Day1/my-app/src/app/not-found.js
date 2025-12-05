import Image from "next/image";

export default function NotFound(){
    return(
 <div className="h-screen flex flex-col items-center justify-center bg-gray-100 text-center p-6">
    <Image 
     
     src="https://i.pinimg.com/1200x/fd/c7/e1/fdc7e12c8a9d9b427fc592368fdc9972.jpg"
     width={400}
     height={400}
     alt="Pinterest Image"
     className="rounded-lg"
     />

    

      <h1 className="text-5xl font-bold text-gray-800">404</h1>
      <p className="text-lg text-gray-600 mt-4">
        Oops! The page you're looking for cannot be found.
      </p>

      <a
        href="/"
        className="mt-6 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
      >
        Go Back Home
      </a>
    </div>

    );
}