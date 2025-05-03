import React from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import LandingPage from './components/LandingPage.js'
import Aristocrats from './components/Aristocrats.js'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage/>}/>
        <Route path="/code" element={<Aristocrats/>}/>
      </Routes>
    </Router>
  );
}

export default App;
