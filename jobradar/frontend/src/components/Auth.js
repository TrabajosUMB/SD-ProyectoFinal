import React, { useState } from 'react';
import './Auth.css';

function Auth({ onLogin }) {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    password2: ''
  });
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const endpoint = isLogin ? 'login' : 'register';
      const response = await fetch(`http://localhost:8000/api/auth/${endpoint}/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(isLogin ? {
          username: formData.username,
          password: formData.password
        } : formData)
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem('token', data.access);
        onLogin(data.user);
      } else {
        setError(data.detail || 'Error en la autenticación');
      }
    } catch (err) {
      setError('Error al conectar con el servidor');
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-box">
        <div className="auth-header">
          <h2>Bienvenido a JobRadar</h2>
          <p>Encuentra las mejores oportunidades laborales</p>
        </div>

        <div className="auth-tabs">
          <button 
            className={isLogin ? 'active' : ''} 
            onClick={() => setIsLogin(true)}
          >
            Iniciar Sesión
          </button>
          <button 
            className={!isLogin ? 'active' : ''} 
            onClick={() => setIsLogin(false)}
          >
            Registrarse
          </button>
        </div>

        {error && <div className="auth-error">{error}</div>}

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label>Usuario</label>
            <input
              type="text"
              value={formData.username}
              onChange={(e) => setFormData({...formData, username: e.target.value})}
              placeholder="Ingresa tu usuario"
              required
            />
          </div>

          {!isLogin && (
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                placeholder="Ingresa tu email"
                required={!isLogin}
              />
            </div>
          )}

          <div className="form-group">
            <label>Contraseña</label>
            <input
              type="password"
              value={formData.password}
              onChange={(e) => setFormData({...formData, password: e.target.value})}
              placeholder="Ingresa tu contraseña"
              required
            />
          </div>

          {!isLogin && (
            <div className="form-group">
              <label>Confirmar Contraseña</label>
              <input
                type="password"
                value={formData.password2}
                onChange={(e) => setFormData({...formData, password2: e.target.value})}
                placeholder="Confirma tu contraseña"
                required={!isLogin}
              />
            </div>
          )}

          <button type="submit" className="auth-submit">
            {isLogin ? 'Iniciar Sesión' : 'Registrarse'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default Auth;
