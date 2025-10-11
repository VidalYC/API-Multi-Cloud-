import React, { useState } from 'react';
import './App.css';
import LandingPage from './components/LandingPage';
import ToolPage from './components/ToolPage';

function App() {
    const [showTool, setShowTool] = useState(false);

    return (
        <div className="App">
            {!showTool ? (
                <LandingPage onStart={() => setShowTool(true)} />
            ) : (
                <ToolPage onBackToHome={() => setShowTool(false)} />
            )}
        </div>
    );
}

export default App;