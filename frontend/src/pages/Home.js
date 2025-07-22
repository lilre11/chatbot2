import React from 'react';
import { Row, Col, Card, Button } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';

const Home = () => {
  return (
    <Row className="justify-content-center">
      <Col lg={8}>
        {/* Hero Section */}
        <div className="text-center mb-5">
          <h1 className="display-4 text-primary mb-4">
            <i className="fas fa-robot me-3"></i>
            Welcome to AI Chatbot
          </h1>
          <p className="lead text-muted">
            An intelligent chatbot powered by Gemini AI, built with React and Flask
          </p>
        </div>

        {/* Features Section */}
        <Row className="mb-5">
          <Col md={4} className="text-center mb-4">
            <Card className="h-100 shadow-sm">
              <Card.Body>
                <i className="fas fa-brain fa-3x text-primary mb-3"></i>
                <Card.Title>Intelligent Responses</Card.Title>
                <Card.Text>
                  Powered by Google's Gemini AI for natural and helpful conversations.
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
          <Col md={4} className="text-center mb-4">
            <Card className="h-100 shadow-sm">
              <Card.Body>
                <i className="fas fa-database fa-3x text-success mb-3"></i>
                <Card.Title>Persistent Storage</Card.Title>
                <Card.Text>
                  All conversations are stored securely in SQL Server database.
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
          <Col md={4} className="text-center mb-4">
            <Card className="h-100 shadow-sm">
              <Card.Body>
                <i className="fas fa-comments fa-3x text-warning mb-3"></i>
                <Card.Title>Context Aware</Card.Title>
                <Card.Text>
                  Maintains conversation history for more meaningful interactions.
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
        </Row>

        {/* Quick Start */}
        <Card className="shadow-sm mb-5">
          <Card.Header className="bg-primary text-white">
            <h5 className="mb-0">
              <i className="fas fa-rocket me-2"></i>
              Quick Start
            </h5>
          </Card.Header>
          <Card.Body>
            <Card.Text>
              Ready to start chatting? Click the button below to begin your conversation with our AI assistant.
            </Card.Text>
            <LinkContainer to="/chat">
              <Button variant="primary" size="lg">
                <i className="fas fa-comment me-2"></i>
                Start Chatting
              </Button>
            </LinkContainer>
          </Card.Body>
        </Card>

        {/* System Info */}
        <Row>
          <Col md={6}>
            <Card className="shadow-sm">
              <Card.Header>
                <h6 className="mb-0">
                  <i className="fas fa-info-circle me-2"></i>
                  System Information
                </h6>
              </Card.Header>
              <Card.Body>
                <ul className="list-unstyled mb-0">
                  <li><strong>Frontend:</strong> React with Bootstrap</li>
                  <li><strong>Backend:</strong> Python Flask</li>
                  <li><strong>Database:</strong> SQL Server</li>
                  <li><strong>AI Engine:</strong> Google Gemini</li>
                </ul>
              </Card.Body>
            </Card>
          </Col>
          <Col md={6}>
            <Card className="shadow-sm">
              <Card.Header>
                <h6 className="mb-0">
                  <i className="fas fa-cogs me-2"></i>
                  Features
                </h6>
              </Card.Header>
              <Card.Body>
                <ul className="list-unstyled mb-0">
                  <li><i className="fas fa-check text-success me-2"></i>Real-time conversations</li>
                  <li><i className="fas fa-check text-success me-2"></i>Message history</li>
                  <li><i className="fas fa-check text-success me-2"></i>Admin dashboard</li>
                  <li><i className="fas fa-check text-success me-2"></i>RESTful API</li>
                </ul>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Col>
    </Row>
  );
};

export default Home;
