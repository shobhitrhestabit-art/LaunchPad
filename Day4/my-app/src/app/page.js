import Image from "next/image";
import Link from "next/link";


export default function Home() {
  return (

    <div className="w-full">

      {/* ----------------- HERO SECTION ----------------- */}
      <section className="min-h-screen flex flex-col items-center justify-center text-center px-6 bg-gradient-to-b from-white to-gray-100">
  <h1 className="text-5xl font-extrabold leading-tight max-w-3xl">
    Build Faster, Launch Smarter with
  </h1>

  <div className="flex justify-center items-center mt-10">
    <button className="px-4 py-2 text-sm text-purple-600 font-semibold rounded-full border border-purple-200 bg-white transition-transform duration-300 ease-in-out hover:bg-purple-600 hover:border-transparent hover:text-white focus:outline-none focus:ring-2 focus:ring-purple-600 focus:ring-offset-2">
      <div className="text-animation">
        <span>N</span>
        <span>e</span>
        <span>x</span>
        <span>t</span>
        <span>.</span>
        <span>j</span>
        <span>s</span>
      </div>
    </button>
  </div>

      
        <p className="mt-4 text-gray-600 max-w-xl">
          A modern landing page built with Tailwind CSS + Next.js.  
          Fully responsive, clean, and optimized.
        </p>

        <div className="mt-8 flex gap-4">
          <button className="px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition">
            Get Started
          </button>
          <button className="px-6 py-3 border border-gray-400 rounded-xl hover:bg-gray-200 transition">
            Learn More
          </button>
        </div>

        <div className="mt-12">
          <Image
            src="https://i.pinimg.com/1200x/09/51/d9/0951d9a4fbab95285b55ba9702bb5a1e.jpg"
             width={900}
             height={500}
             alt="Hero illustration"
             className="rounded-xl shadow-xl w-full h-auto"
             sizes="(max-width: 640px) 100vw,
              (max-width: 1024px) 80vw,
               900px"
            
          />
        </div>
      </section>

      {/* ----------------- FEATURES SECTION ----------------- */}
      <section className="py-20 px-6 bg-white">
        <h2 className="text-4xl font-bold text-center">Powerful Features</h2>
        <p className="text-center text-gray-600 mt-2">
          Everything you need to build beautiful experiences.
        </p>

        <div className="mt-12 grid md:grid-cols-3 gap-10 max-w-6xl mx-auto">
          {/* Feature 1 */}
          <div className="p-8 shadow-md rounded-2xl bg-gray-50 hover:shadow-lg transition">
            <h3 className="text-xl font-bold mb-2">⚡ Super Fast</h3>
            <p className="text-gray-600">
              Built with Next.js for optimized performance.
            </p>
          </div>

          {/* Feature 2 */}
          <div className="p-8 shadow-md rounded-2xl bg-gray-50 hover:shadow-lg transition">
            <h3 className="text-xl font-bold mb-2">📱 Fully Responsive</h3>
            <p className="text-gray-600">
              Works smoothly on mobile, tablet, and desktop.
            </p>
          </div>

          {/* Feature 3 */}
          <div className="p-8 shadow-md rounded-2xl bg-gray-50 hover:shadow-lg transition">
            <h3 className="text-xl font-bold mb-2">🎨 Beautiful UI</h3>
            <p className="text-gray-600">
              Clean, modern design with Tailwind CSS.
            </p>
          </div>
        </div>
      </section>

      {/* ----------------- CTA SECTION ----------------- */}
      <section className="py-28 px-6 bg-blue-600 text-white text-center">
        <h2 className="text-4xl font-bold">Ready to build your project?</h2>
        <p className="mt-3 text-gray-100 max-w-xl mx-auto">
          Start building with the most powerful Next.js landing page template.
        </p>

        <Link href="https://nextjs.org/">
        <button className="mt-8 px-8 py-3 bg-white text-blue-600 font-semibold rounded-xl hover:bg-gray-200 transition">
          Start Now
        </button>
        </Link>

        
      </section>

      {/* ----------------- FOOTER ----------------- */}
      <footer className="py-10 text-center text-gray-500 bg-gray-100">
        © 2025 YourBrand • All rights reserved.
      </footer>
    </div>
  );
}
