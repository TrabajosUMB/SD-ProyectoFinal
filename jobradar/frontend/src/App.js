import { useState, useEffect } from 'react';
import './App.css';
import Auth from './components/Auth';

function App() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [user, setUser] = useState(null);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      fetch('http://localhost:8000/api/users/me/', {
        headers: { 'Authorization': `Bearer ${token}` }
      })
        .then(response => response.json())
        .then(data => setUser(data))
        .catch(() => localStorage.removeItem('token'));
    }

    fetch('http://localhost:8000/api/jobs/')
      .then(response => response.json())
      .then(data => {
        setJobs(data.results || []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error:', error);
        setError('Error cargando ofertas de trabajo');
        setLoading(false);
      });
  }, []);

  return (
    <div className="App">
      {!user ? (
        <Auth onLogin={handleLogin} />
      ) : (
        <>
          <header className="App-header">
            <h1>JobRadar - Encuentra tu próximo trabajo</h1>
            <div className="auth-buttons">
              <div className="user-info">
                <span>Bienvenido, {user.username}</span>
                <button onClick={() => {
                  localStorage.removeItem('token');
                  setUser(null);
                }}>Cerrar sesión</button>
              </div>
            </div>
          </header>
          
          <main className="App-main">
            {loading && <p>Cargando ofertas de trabajo...</p>}
            {error && <p className="error">{error}</p>}
            
            <div className="job-list">
              {Array.isArray(jobs) && jobs.map(job => (
                <div key={job.id} className="job-card">
                  <h3>{job.title}</h3>
                  <h4>{job.company}</h4>
                  <p className="location">{job.location}</p>
                  <p className="salary">
                    Salario: ${job.salary_min.toLocaleString()} - ${job.salary_max.toLocaleString()}
                  </p>
                  <p className="description">{job.description}</p>
                  <div className="skills">
                    {job.skills_required.map(skill => (
                      <span key={skill} className="skill-tag">{skill}</span>
                    ))}
                  </div>
                  <div className="job-details">
                    <span>Modalidad: {job.modality}</span>
                    <span>Contrato: {job.contract_type}</span>
                    <span>Experiencia: {job.experience_years} años</span>
                  </div>
                  <a href={job.url} target="_blank" rel="noopener noreferrer" className="apply-button">
                    Aplicar
                  </a>
                </div>
              ))}
            </div>
          </main>
        </>
      )}
    </div>
  );
}

export default App;
