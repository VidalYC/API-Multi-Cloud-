import React, { useState } from 'react';
import './styles/App.css';  // ← CAMBIADO
import LandingPage from './components/landing/LandingPage';
import ToolPage from './components/tools/ToolPage';

function App() {
  const [showLanding, setShowLanding] = useState(true);

  return (
    <div className="App">
      {showLanding ? (
        <LandingPage onStart={() => setShowLanding(false)} />
      ) : (
        <ToolPage onBackToHome={() => setShowLanding(true)} />
      )}
    </div>
  );
}

export default App;