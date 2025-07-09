// Chat functionality

class ChatApp {
    constructor() {
        this.currentConversationId = null;
        this.conversations = [];
        this.isTyping = false;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadConversations();
    }

    setupEventListeners() {
        // Chat form submission
        const chatForm = document.getElementById('chatForm');
        if (chatForm) {
            chatForm.addEventListener('submit', (e) => this.handleSendMessage(e));
        }

        // New chat button
        const newChatBtn = document.getElementById('newChatBtn');
        if (newChatBtn) {
            newChatBtn.addEventListener('click', () => this.startNewChat());
        }

        // Clear chat button
        const clearChatBtn = document.getElementById('clearChatBtn');
        if (clearChatBtn) {
            clearChatBtn.addEventListener('click', () => this.clearCurrentChat());
        }

        // Show sidebar button (mobile)
        const showSidebarBtn = document.getElementById('showSidebarBtn');
        if (showSidebarBtn) {
            showSidebarBtn.addEventListener('click', () => this.showConversationModal());
        }

        // Enter key to send message
        const messageInput = document.getElementById('messageInput');
        if (messageInput) {
            messageInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.handleSendMessage(e);
                }
            });
        }
    }

    async handleSendMessage(e) {
        e.preventDefault();
        
        const messageInput = document.getElementById('messageInput');
        const message = messageInput.value.trim();
        
        if (!message || this.isTyping) {
            return;
        }

        // Clear input and show typing indicator
        messageInput.value = '';
        this.setTyping(true);
        
        // Add user message to chat
        this.addMessageToChat(message, 'user');

        try {
            const response = await App.apiCall('/api/chat/send', {
                method: 'POST',
                body: JSON.stringify({
                    message: message,
                    conversation_id: this.currentConversationId
                })
            });

            // Update conversation ID if this is a new chat
            if (!this.currentConversationId) {
                this.currentConversationId = response.conversation_id;
                this.loadConversations(); // Refresh conversation list
            }

            // Add bot response to chat
            this.addMessageToChat(response.response, 'bot', response.timestamp);

        } catch (error) {
            console.error('Error sending message:', error);
            this.addMessageToChat('Sorry, I encountered an error. Please try again.', 'bot');
            App.showToast('Failed to send message', 'danger');
        } finally {
            this.setTyping(false);
        }
    }

    addMessageToChat(content, senderType, timestamp = null) {
        const chatMessages = document.getElementById('chatMessages');
        const welcomeMessage = chatMessages.querySelector('.welcome-message');
        
        // Remove welcome message if it exists
        if (welcomeMessage) {
            welcomeMessage.remove();
        }

        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${senderType}`;
        
        const avatar = senderType === 'user' ? 
            '<div class="message-avatar"><i class="fas fa-user"></i></div>' :
            '<div class="message-avatar"><i class="fas fa-robot"></i></div>';
        
        const timeStr = timestamp ? App.formatTimestamp(timestamp) : App.formatTimestamp(new Date().toISOString());
        
        messageDiv.innerHTML = `
            ${avatar}
            <div class="message-bubble">
                ${App.escapeHtml(content)}
                <small class="message-time">${timeStr}</small>
            </div>
        `;

        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    setTyping(isTyping) {
        this.isTyping = isTyping;
        const typingIndicator = document.getElementById('typingIndicator');
        const sendBtn = document.getElementById('sendBtn');
        
        if (typingIndicator) {
            typingIndicator.style.display = isTyping ? 'block' : 'none';
        }
        
        if (sendBtn) {
            sendBtn.disabled = isTyping;
        }
    }

    async loadConversations() {
        try {
            const response = await App.apiCall('/api/chat/conversations');
            this.conversations = response.conversations;
            this.renderConversationList();
        } catch (error) {
            console.error('Error loading conversations:', error);
        }
    }

    renderConversationList() {
        const conversationList = document.getElementById('conversationList');
        const mobileConversationList = document.getElementById('mobileConversationList');
        
        if (!conversationList) return;

        if (this.conversations.length === 0) {
            conversationList.innerHTML = `
                <div class="list-group-item text-center text-muted py-4">
                    <i class="fas fa-comment-slash fa-2x mb-2 d-block"></i>
                    No conversations yet
                </div>
            `;
        } else {
            const conversationHTML = this.conversations.map(conv => `
                <div class="list-group-item conversation-item ${conv.id === this.currentConversationId ? 'active' : ''}" 
                     data-conversation-id="${conv.id}">
                    <div class="conversation-title">${App.escapeHtml(conv.title)}</div>
                    <div class="conversation-preview">${conv.message_count} messages</div>
                    <small class="text-muted">${App.formatTimestamp(conv.updated_at)}</small>
                </div>
            `).join('');

            conversationList.innerHTML = conversationHTML;
            
            // Add click listeners
            conversationList.querySelectorAll('.conversation-item').forEach(item => {
                item.addEventListener('click', () => {
                    const conversationId = parseInt(item.dataset.conversationId);
                    this.loadConversation(conversationId);
                });
            });
        }

        // Update mobile list if it exists
        if (mobileConversationList) {
            mobileConversationList.innerHTML = conversationList.innerHTML;
        }
    }

    async loadConversation(conversationId) {
        try {
            const response = await App.apiCall(`/api/chat/conversations/${conversationId}/messages`);
            
            this.currentConversationId = conversationId;
            this.clearChatMessages();
            
            // Update chat title
            const chatTitle = document.getElementById('chatTitle');
            if (chatTitle) {
                chatTitle.textContent = response.conversation.title;
            }

            // Load messages
            response.messages.forEach(msg => {
                this.addMessageToChat(msg.content, msg.sender_type, msg.timestamp);
            });

            // Update conversation list active state
            this.renderConversationList();

        } catch (error) {
            console.error('Error loading conversation:', error);
            App.showToast('Failed to load conversation', 'danger');
        }
    }

    startNewChat() {
        this.currentConversationId = null;
        this.clearChatMessages();
        
        const chatTitle = document.getElementById('chatTitle');
        if (chatTitle) {
            chatTitle.textContent = 'AI Assistant';
        }

        // Show welcome message
        const chatMessages = document.getElementById('chatMessages');
        chatMessages.innerHTML = `
            <div class="welcome-message text-center text-muted py-5">
                <i class="fas fa-robot fa-3x mb-3"></i>
                <h5>New Conversation</h5>
                <p>Ask me anything and I'll do my best to help you.</p>
            </div>
        `;

        // Update conversation list active state
        this.renderConversationList();
    }

    clearCurrentChat() {
        if (confirm('Are you sure you want to clear this chat?')) {
            this.startNewChat();
        }
    }

    clearChatMessages() {
        const chatMessages = document.getElementById('chatMessages');
        if (chatMessages) {
            chatMessages.innerHTML = '';
        }
    }

    showConversationModal() {
        const modal = new bootstrap.Modal(document.getElementById('conversationModal'));
        modal.show();
    }
}

// Initialize chat app when page loads
document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname.includes('/chat')) {
        new ChatApp();
    }
});
