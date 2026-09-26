import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import LoginPage from './presentation/pages/Auth/LoginPage';
import RegisterPage from './presentation/pages/Auth/RegisterPage';

import HomePage from './presentation/pages/HomePage';
import AboutPage from './presentation/pages/AboutPage';
import ModelsPage from './presentation/pages/ModelsPage';
import ContactsPage from './presentation/pages/ContactPage';
import PrivateRoute from "./PrivateRoute";
import './styles/App.css';

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/home" element={<HomePage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/models" element={<ModelsPage />} />
          <Route path="/contacts" element={<ContactsPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/login" element={<LoginPage />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;