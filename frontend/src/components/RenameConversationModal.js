import React, { useState } from 'react';
import { Modal, Button, Form } from 'react-bootstrap';
import { renameConversation } from '../utils/chatApi';

const RenameConversationModal = ({ 
  show, 
  onHide, 
  conversation, 
  onConversationRenamed 
}) => {
  const [newTitle, setNewTitle] = useState(conversation?.title || '');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!newTitle.trim()) {
      setError('Please enter a title');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const updatedConversation = await renameConversation(conversation.id, newTitle.trim());
      onConversationRenamed(updatedConversation);
      onHide();
    } catch (err) {
      setError('Failed to rename conversation. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleShow = () => {
    setNewTitle(conversation?.title || '');
    setError('');
  };

  return (
    <Modal show={show} onHide={onHide} onShow={handleShow} centered>
      <Modal.Header closeButton>
        <Modal.Title>Rename Conversation</Modal.Title>
      </Modal.Header>
      
      <Form onSubmit={handleSubmit}>
        <Modal.Body>
          {error && (
            <div className="alert alert-danger" role="alert">
              {error}
            </div>
          )}
          
          <Form.Group className="mb-3">
            <Form.Label>Conversation Title</Form.Label>
            <Form.Control
              type="text"
              value={newTitle}
              onChange={(e) => setNewTitle(e.target.value)}
              placeholder="Enter new title..."
              disabled={isLoading}
              autoFocus
            />
          </Form.Group>
        </Modal.Body>
        
        <Modal.Footer>
          <Button variant="secondary" onClick={onHide} disabled={isLoading}>
            Cancel
          </Button>
          <Button 
            variant="primary" 
            type="submit" 
            disabled={isLoading || !newTitle.trim()}
          >
            {isLoading ? 'Saving...' : 'Save Changes'}
          </Button>
        </Modal.Footer>
      </Form>
    </Modal>
  );
};

export default RenameConversationModal;
