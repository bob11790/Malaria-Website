import Map from "../Components/Map";
import React, { useState } from "react";
import PredictionPanel from "../Components/PredictionPanel";

const Home = () => {
  const [predictionData, setPredictionData] = useState<any>(null);

  const handlePrediction = (data: any) => {
    setPredictionData(data);
  };

  return (
    <div style={{ height: "100%", width: "100%" }}>
      <Map onPrediction={handlePrediction} />
      {predictionData && <PredictionPanel {...predictionData} />}
    </div>
  );
};

export default Home;
