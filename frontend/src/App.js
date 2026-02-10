import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import NewPage from './NewPage';
import AnalysisPage from './AnalysisPage';
import Background from './Background';

function App() {
  return (
    <Router>
      <Background>
        <Routes>
          <Route path="/" element={<NewPage />} />
          <Route path="/analysis" element={<AnalysisPage />} />
        </Routes>
      </Background>
    </Router>
  );
}

export default App;
