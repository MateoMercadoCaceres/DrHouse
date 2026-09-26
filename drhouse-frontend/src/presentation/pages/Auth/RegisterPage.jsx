import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import authService from "../../../infrastructure/services/authServices";
import "../../../styles/LoginPage.css";

function RegisterPage() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [fullName, setFullName] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setError(null);

    // Validar que las contraseñas coincidan
    if (password !== confirmPassword) {
      setError("Las contraseñas no coinciden");
      return;
    }

    // Validar longitud mínima de contraseña
    if (password.length < 6) {
      setError("La contraseña debe tener al menos 6 caracteres");
      return;
    }

    setLoading(true);

    try {
      await authService.register(username, email, fullName, password);
      console.log("Registro exitoso");

      // Redirigir a login o home después del registro exitoso
      navigate('/login');
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
        <h2>Registro</h2>

        <form onSubmit={handleRegister}>
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
              type="email" 
              placeholder="Correo electrónico" 
              value={email}
              onChange={(e) => setEmail(e.target.value)} 
              required 
            />
          </div>

          <div className="inputBx">
            <input 
              type="text" 
              placeholder="Nombre completo" 
              value={fullName}
              onChange={(e) => setFullName(e.target.value)} 
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
              type="password" 
              placeholder="Confirmar contraseña" 
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)} 
              required 
            />
          </div>

          <div className="inputBx">
            <input 
              type="submit" 
              value={loading ? "Registrando..." : "Registrarse"} 
              disabled={loading}
            />
          </div>

          {error && <p style={{ color: 'red', textAlign: 'center', marginTop: '10px' }}>{error}</p>}

          <div className="links">
            <a href="/login">¿Ya tienes cuenta? Inicia sesión</a>
          </div>
        </form>
      </div>
    </div>
  );
}

export default RegisterPage;