// Utility functions for chat API operations
import axios from 'axios';

/**
 * Rename a conversation
 * @param {number} conversationId - The ID of the conversation to rename
 * @param {string} newTitle - The new title for the conversation
 * @returns {Promise<Object>} - The updated conversation object
 */
export const renameConversation = async (conversationId, newTitle) => {
  try {
    const response = await axios.put(`/api/chat/conversations/${conversationId}`, {
      title: newTitle
    });
    return response.data.conversation;
  } catch (error) {
    console.error('Error renaming conversation:', error);
    throw error;
  }
};

/**
 * Get all conversations for the current user
 * @returns {Promise<Array>} - Array of conversation objects
 */
export const getConversations = async () => {
  try {
    const response = await axios.get('/api/chat/conversations');
    return response.data.conversations;
  } catch (error) {
    console.error('Error fetching conversations:', error);
    throw error;
  }
};

/**
 * Create a new conversation
 * @param {string} title - Optional title for the new conversation
 * @returns {Promise<Object>} - The new conversation object
 */
export const createNewConversation = async (title = null) => {
  try {
    const response = await axios.post('/api/chat/new-conversation', {
      title: title
    });
    return response.data.conversation;
  } catch (error) {
    console.error('Error creating new conversation:', error);
    throw error;
  }
};

/**
 * Get messages for a specific conversation
 * @param {number} conversationId - The ID of the conversation
 * @returns {Promise<Object>} - Object containing messages and conversation details
 */
export const getConversationMessages = async (conversationId) => {
  try {
    const response = await axios.get(`/api/chat/conversations/${conversationId}/messages`);
    return response.data;
  } catch (error) {
    console.error('Error fetching conversation messages:', error);
    throw error;
  }
};

/**
 * Send a message to the chatbot
 * @param {string} message - The message to send
 * @param {number} conversationId - Optional conversation ID
 * @returns {Promise<Object>} - The bot's response
 */
export const sendMessage = async (message, conversationId = null) => {
  try {
    const response = await axios.post('/api/chat/send', {
      message: message,
      conversation_id: conversationId
    });
    return response.data;
  } catch (error) {
    console.error('Error sending message:', error);
    throw error;
  }
};
