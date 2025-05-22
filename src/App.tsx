import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./Pages/Home.tsx";
import Header from "./Components/Header.tsx";

function App() {
  return (
    <div style={{ height: "100vh", width: "100%" }}>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          {/* Add more routes here */}
        </Routes>
      </Router>
    </div>
  );
}

export default App;
