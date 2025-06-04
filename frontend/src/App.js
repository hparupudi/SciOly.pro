import React from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import LandingPage from './components/LandingPage.js';
import Aristocrats from './components/Aristocrats.js';
import MenuPage from './components/MenuPage.js';
import MCQPage from './components/MCQPage.js';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage/>}/>
        <Route path="/aristo" element={<Aristocrats/>}/>
        <Route path="/menu" element={<MenuPage/>}/>
        <Route path="/mcq" element={<MCQPage/>}/>
      </Routes>
    </Router>
  );
}

export default App;
