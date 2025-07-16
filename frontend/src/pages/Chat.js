import React, { useState, useEffect, useRef } from 'react';
import { Row, Col, Card, Form, Button, ListGroup, Modal, Dropdown, Alert } from 'react-bootstrap';
import api from '../utils/axios';
import RenameConversationModal from '../components/RenameConversationModal';

const Chat = ({ user }) => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [conversations, setConversations] = useState([]);
  const [currentConversationId, setCurrentConversationId] = useState(null);
  const [isTyping, setIsTyping] = useState(false);
  const [showConversationModal, setShowConversationModal] = useState(false);
  const [showRenameModal, setShowRenameModal] = useState(false);
  const [selectedConversation, setSelectedConversation] = useState(null);
  const [error, setError] = useState('');
  const messagesEndRef = useRef(null);

  useEffect(() => {
    loadConversations();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadConversations = async () => {
    try {
      const response = await api.get('/api/chat/conversations');
      setConversations(response.data.conversations);
      setError('');
    } catch (error) {
      console.error('Error loading conversations:', error);
      if (error.response && error.response.status === 401) {
        setError('Please login to access your conversations.');
      } else {
        setError('Failed to load conversations.');
      }
    }
  };

  const loadConversation = async (conversationId) => {
    try {
      const response = await api.get(`/api/chat/conversations/${conversationId}/messages`);
      setMessages(response.data.messages);
      setCurrentConversationId(conversationId);
      setError('');
    } catch (error) {
      console.error('Error loading conversation:', error);
      if (error.response && error.response.status === 401) {
        setError('Please login to access conversations.');
      } else {
        setError('Failed to load conversation.');
      }
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    
    if (!inputMessage.trim() || isTyping) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    setIsTyping(true);

    // Add user message to chat immediately
    const newUserMessage = {
      content: userMessage,
      sender_type: 'user',
      timestamp: new Date().toISOString()
    };
    setMessages(prev => [...prev, newUserMessage]);

    try {
      const response = await api.post('/api/chat/send', {
        message: userMessage,
        conversation_id: currentConversationId
      }, {
        withCredentials: true
      });

      // Update conversation ID if this is a new chat
      if (!currentConversationId) {
        setCurrentConversationId(response.data.conversation_id);
        loadConversations(); // Refresh conversation list
      }

      // Add bot response
      const botMessage = {
        content: response.data.response,
        sender_type: 'bot',
        timestamp: response.data.timestamp
      };
      setMessages(prev => [...prev, botMessage]);

    } catch (error) {
      console.error('Error sending message:', error);
      // Add error message with more details
      const errorDetails = error.response?.data?.error || error.message || 'Unknown error';
      const errorMessage = {
        content: `Sorry, I encountered an error: ${errorDetails}. Please try again.`,
        sender_type: 'bot',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const startNewChat = () => {
    setCurrentConversationId(null);
    setMessages([]);
  };

  const handleRenameConversation = (conversation) => {
    setSelectedConversation(conversation);
    setShowRenameModal(true);
  };

  const handleConversationRenamed = (updatedConversation) => {
    setConversations(prevConversations => 
      prevConversations.map(conv => 
        conv.id === updatedConversation.id ? updatedConversation : conv
      )
    );
    setShowRenameModal(false);
    setSelectedConversation(null);
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;

    if (diff < 60000) return 'Just now';
    if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
    return date.toLocaleDateString();
  };

  const renderMessage = (message, index) => {
    const isUser = message.sender_type === 'user';
    return (
      <div key={index} className={`message ${isUser ? 'user' : 'bot'}`}>
        {!isUser && (
          <div className="message-avatar">
            <i className="fas fa-robot"></i>
          </div>
        )}
        <div className="message-bubble">
          {message.content}
          <small className="message-time">
            {formatTimestamp(message.timestamp)}
          </small>
        </div>
        {isUser && (
          <div className="message-avatar">
            <i className="fas fa-user"></i>
          </div>
        )}
      </div>
    );
  };

  return (
    <Row className="h-100">
      {error && (
        <Col md={12} className="mb-3">
          <Alert variant="danger" dismissible onClose={() => setError('')}>
            {error}
          </Alert>
        </Col>
      )}
      
      {/* Sidebar - Conversation List */}
      <Col md={3} className="d-none d-md-block">
        <Card className="h-100">
          <Card.Header className="bg-secondary text-white d-flex justify-content-between align-items-center">
            <h6 className="mb-0">Conversations</h6>
            <Button size="sm" variant="light" onClick={startNewChat}>
              <i className="fas fa-plus"></i>
            </Button>
          </Card.Header>
          <Card.Body className="p-0">
            <ListGroup variant="flush">
              {conversations.length === 0 ? (
                <ListGroup.Item className="text-center text-muted py-4">
                  <i className="fas fa-comment-slash fa-2x mb-2 d-block"></i>
                  No conversations yet
                </ListGroup.Item>
              ) : (
                conversations.map(conv => (
                  <ListGroup.Item
                    key={conv.id}
                    className={`conversation-item d-flex justify-content-between align-items-center ${
                      conv.id === currentConversationId ? 'active' : ''
                    }`}
                  >
                    <div 
                      className="conversation-content flex-grow-1"
                      onClick={() => loadConversation(conv.id)}
                      style={{ cursor: 'pointer' }}
                    >
                      <div className="conversation-title">{conv.title}</div>
                      <div className="conversation-preview">
                        {conv.message_count} messages
                      </div>
                      <small className="text-muted">
                        {formatTimestamp(conv.updated_at)}
                      </small>
                    </div>
                    
                    <Dropdown>
                      <Dropdown.Toggle 
                        variant="outline-secondary" 
                        size="sm" 
                        id={`dropdown-${conv.id}`}
                        style={{ border: 'none', background: 'none' }}
                      >
                        <i className="fas fa-ellipsis-v"></i>
                      </Dropdown.Toggle>

                      <Dropdown.Menu>
                        <Dropdown.Item onClick={() => handleRenameConversation(conv)}>
                          <i className="fas fa-edit me-2"></i>
                          Rename
                        </Dropdown.Item>
                      </Dropdown.Menu>
                    </Dropdown>
                  </ListGroup.Item>
                ))
              )}
            </ListGroup>
          </Card.Body>
        </Card>
      </Col>

      {/* Main Chat Area */}
      <Col md={9}>
        <Card className="chat-container">
          {/* Chat Header */}
          <Card.Header className="bg-primary text-white d-flex justify-content-between align-items-center">
            <h5 className="mb-0">
              <i className="fas fa-robot me-2"></i>
              AI Assistant
            </h5>
            <div>
              <Button
                size="sm"
                variant="light"
                onClick={startNewChat}
                className="me-2"
                title="Clear Chat"
              >
                <i className="fas fa-trash"></i>
              </Button>
              <Button
                size="sm"
                variant="light"
                className="d-md-none"
                onClick={() => setShowConversationModal(true)}
                title="Show Conversations"
              >
                <i className="fas fa-bars"></i>
              </Button>
            </div>
          </Card.Header>

          {/* Chat Messages */}
          <Card.Body className="chat-messages">
            {messages.length === 0 ? (
              <div className="welcome-message">
                <i className="fas fa-robot fa-3x mb-3"></i>
                <h5>Welcome to AI Chatbot!</h5>
                <p>Ask me anything and I'll do my best to help you.</p>
              </div>
            ) : (
              messages.map((message, index) => renderMessage(message, index))
            )}
            {isTyping && (
              <div className="message bot">
                <div className="message-avatar">
                  <i className="fas fa-robot"></i>
                </div>
                <div className="message-bubble">
                  <div className="loading-spinner me-2"></div>
                  AI is typing...
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </Card.Body>

          {/* Chat Input */}
          <Card.Footer>
            <Form onSubmit={sendMessage}>
              <div className="input-group">
                <Form.Control
                  type="text"
                  placeholder="Type your message here..."
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  disabled={isTyping}
                />
                <Button type="submit" variant="primary" disabled={isTyping}>
                  <i className="fas fa-paper-plane"></i>
                </Button>
              </div>
            </Form>
          </Card.Footer>
        </Card>
      </Col>

      {/* Mobile Conversation Modal */}
      <Modal show={showConversationModal} onHide={() => setShowConversationModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Conversations</Modal.Title>
        </Modal.Header>
        <Modal.Body className="p-0">
          <ListGroup variant="flush">
            {conversations.map(conv => (
              <ListGroup.Item
                key={conv.id}
                action
                active={conv.id === currentConversationId}
                onClick={() => {
                  loadConversation(conv.id);
                  setShowConversationModal(false);
                }}
              >
                <div className="conversation-title">{conv.title}</div>
                <div className="conversation-preview">
                  {conv.message_count} messages
                </div>
                <small className="text-muted">
                  {formatTimestamp(conv.updated_at)}
                </small>
              </ListGroup.Item>
            ))}
          </ListGroup>
        </Modal.Body>
      </Modal>

      {/* Rename Conversation Modal */}
      <RenameConversationModal
        show={showRenameModal}
        onHide={() => setShowRenameModal(false)}
        conversation={selectedConversation}
        onConversationRenamed={handleConversationRenamed}
      />
    </Row>
  );
};

export default Chat;
