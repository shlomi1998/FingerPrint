import React, { useEffect, useState } from "react";
import { ImageRecognition } from "../components";

const Home = () => {
  const [showImageRecognition, setShowImageRecognition] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowImageRecognition(true);
    }, 5000);

    // Cleanup function to clear the timer when the component unmounts
    return () => {
      clearTimeout(timer);
    };
  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#000000]">
      <div className="">
        <div className="relative top-[-50px] text-center font-mono font-bold text-[#fff] text-2xl">
          <h1>Digital Fingerprint Sweat-Pore Analysis</h1>
        </div>
        <div className="flex justify-center">
          <img className="w-[500px] h-[300px] rounded-xl" src="./images/img-home.jpeg" alt="not fond" />
        </div>
      </div>

      {showImageRecognition && <ImageRecognition />}
      <div className="w-[150px] h-[60px] rounded-md bg-[#1cfae4] fixed bottom-3 right-4 flex justify-center items-center"> <h1 className="text-black font-mono font-bold text-center text-2xl">Po<span className="text-3xl text-blue-950 ">l</span>y Gene</h1></div>
    </div>
  );
};

export default Home;
