import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { LandingPage } from './pages/LandingPage';
import { NeuroSimPage } from './pages/NeuroSimPage';
import { STLViewerPage } from './pages/STLViewerPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/NeuroSim" element={<NeuroSimPage />} />
        <Route path="/stl-viewer" element={<STLViewerPage />} />
      </Routes>
    </Router>
  );
}

export default App;

