import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { LandingPage } from './pages/LandingPage';
import { NeuroSimPage } from './pages/NeuroSimPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/neurosim" element={<NeuroSimPage />} />
      </Routes>
    </Router>
  );
}

export default App;

