import React from 'react';
import { Navbar, Nav, Container, Button } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';

const NavigationBar = ({ user, onLogout }) => {
  return (
    <Navbar bg="primary" variant="dark" expand="lg">
      <Container>
        <LinkContainer to="/">
          <Navbar.Brand>
            <i className="fas fa-robot me-2"></i>
            AI Chatbot
          </Navbar.Brand>
        </LinkContainer>
        
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <LinkContainer to="/">
              <Nav.Link>Home</Nav.Link>
            </LinkContainer>
            {user && (
              <>
                <LinkContainer to="/chat">
                  <Nav.Link>Chat</Nav.Link>
                </LinkContainer>
                <LinkContainer to="/admin">
                  <Nav.Link>Admin</Nav.Link>
                </LinkContainer>
              </>
            )}
          </Nav>
          
          <Nav className="ms-auto">
            {user ? (
              <>
                <Navbar.Text className="me-3">
                  Welcome, {user.username}!
                </Navbar.Text>
                <Button variant="outline-light" size="sm" onClick={onLogout}>
                  Logout
                </Button>
              </>
            ) : (
              <LinkContainer to="/login">
                <Nav.Link>Login</Nav.Link>
              </LinkContainer>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default NavigationBar;
