import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Container } from 'react-bootstrap';
import NavigationBar from './components/NavigationBar';
import Home from './pages/Home';
import Chat from './pages/Chat';
import Admin from './pages/Admin';
import Login from './pages/Login';
import Footer from './components/Footer';
import api from './utils/axios';
import './App.css';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Check if user is logged in on app start
  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const response = await api.get('/api/chat/me');
      setUser(response.data.user);
    } catch (error) {
      // User not logged in
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = async () => {
    try {
      await api.post('/api/chat/logout');
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setUser(null);
    }
  };

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ height: '100vh' }}>
        <div className="spinner-border" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  return (
    <Router>
      <div className="App">
        <NavigationBar user={user} onLogout={handleLogout} />
        <main className="flex-grow-1">
          <Container fluid className="mt-4">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route 
                path="/login" 
                element={user ? <Navigate to="/chat" /> : <Login onLogin={handleLogin} />} 
              />
              <Route 
                path="/chat" 
                element={user ? <Chat user={user} /> : <Navigate to="/login" />} 
              />
              <Route 
                path="/admin" 
                element={user ? <Admin user={user} /> : <Navigate to="/login" />} 
              />
            </Routes>
          </Container>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
