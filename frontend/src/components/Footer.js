import React from 'react';
import { Container } from 'react-bootstrap';

const Footer = () => {
  return (
    <footer className="bg-light text-center text-muted py-3 mt-5">
      <Container>
        <p className="mb-0">&copy; 2025 AI Chatbot. Powered by Gemini AI and Flask.</p>
      </Container>
    </footer>
  );
};

export default Footer;
