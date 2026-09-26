import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import authService from "../../../infrastructure/services/authServices";
import "../../../styles/LoginPage.css";


function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      await authService.login(username, password);
      console.log("Login exitoso");

      navigate('/home');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="ring">
      <i style={{ "--clr": "#f8f8f8" }}></i>
      <i style={{ "--clr": "#b8ff89" }}></i>
      <i style={{ "--clr": "#fffd44" }}></i>

      <div className="login">
        <h2>Iniciar Sesión</h2>

        <form onSubmit={handleLogin}>
          <div className="inputBx">
            <input 
              type="text" 
              placeholder="Nombre de usuario" 
              value={username}
              onChange={(e) => setUsername(e.target.value)} 
              required 
            />
          </div>

          <div className="inputBx">
            <input 
              type="password" 
              placeholder="Contraseña" 
              value={password}
              onChange={(e) => setPassword(e.target.value)} 
              required 
            />
          </div>

          <div className="inputBx">
            <input 
              type="submit" 
              value={loading ? "Iniciando..." : "Iniciar Sesión"} 
              disabled={loading}
            />
          </div>

          {error && <p style={{ color: 'red', textAlign: 'center', marginTop: '10px' }}>{error}</p>}

          <div className="links">
            <a href="/forgot-password">¿Olvidaste tu contraseña?</a>
            <a href="/register">¿No tienes cuenta? Regístrate</a>
          </div>
        </form>
      </div>
    </div>
  );
}

export default LoginPage;