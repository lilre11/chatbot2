// Admin dashboard functionality

class AdminApp {
    constructor() {
        this.refreshInterval = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadSystemStatus();
        this.loadStatistics();
        this.loadLogs();
        this.loadUsers();
        
        // Auto-refresh every 30 seconds
        this.refreshInterval = setInterval(() => {
            this.loadSystemStatus();
            this.loadStatistics();
        }, 30000);
    }

    setupEventListeners() {
        // Log level filter
        const logLevelFilter = document.getElementById('logLevelFilter');
        if (logLevelFilter) {
            logLevelFilter.addEventListener('change', () => this.loadLogs());
        }

        // Tab switches
        const tabButtons = document.querySelectorAll('#adminTabs button');
        tabButtons.forEach(button => {
            button.addEventListener('shown.bs.tab', (e) => {
                const target = e.target.getAttribute('data-bs-target');
                if (target === '#users') {
                    this.loadUsers();
                } else if (target === '#logs') {
                    this.loadLogs();
                }
            });
        });
    }

    async loadSystemStatus() {
        try {
            const response = await App.apiCall('/api/admin/status');
            
            // Update database status
            this.updateStatusDisplay('db', response.database);
            
            // Update AI service status
            this.updateStatusDisplay('ai', response.ai_service);
            
            // Update overall status
            this.updateStatusDisplay('overall', {
                status: response.overall_status,
                healthy: response.overall_status === 'healthy'
            });

        } catch (error) {
            console.error('Error loading system status:', error);
            this.updateStatusDisplay('db', { status: 'error', healthy: false });
            this.updateStatusDisplay('ai', { status: 'error', healthy: false });
            this.updateStatusDisplay('overall', { status: 'error', healthy: false });
        }
    }

    updateStatusDisplay(type, statusData) {
        const statusElement = document.getElementById(`${type}Status`);
        const iconElement = document.getElementById(`${type}Icon`);
        
        if (!statusElement || !iconElement) return;

        // Update status badge
        statusElement.className = 'badge';
        if (statusData.healthy) {
            statusElement.classList.add('badge-success');
            statusElement.textContent = 'Healthy';
            iconElement.className = iconElement.className.replace(/text-\w+/, 'text-success');
        } else {
            statusElement.classList.add('badge-danger');
            statusElement.textContent = 'Error';
            iconElement.className = iconElement.className.replace(/text-\w+/, 'text-danger');
        }
    }

    async loadStatistics() {
        try {
            const response = await App.apiCall('/api/admin/stats');
            
            // Update statistics displays
            this.updateStatistic('userCount', response.users);
            this.updateStatistic('conversationCount', response.conversations);
            this.updateStatistic('messageCount', response.messages);
            this.updateStatistic('activeConversations', response.active_conversations_24h);

        } catch (error) {
            console.error('Error loading statistics:', error);
            this.updateStatistic('userCount', '-');
            this.updateStatistic('conversationCount', '-');
            this.updateStatistic('messageCount', '-');
            this.updateStatistic('activeConversations', '-');
        }
    }

    updateStatistic(elementId, value) {
        const element = document.getElementById(elementId);
        if (element) {
            element.textContent = typeof value === 'number' ? value.toLocaleString() : value;
        }
    }

    async loadLogs() {
        const tableBody = document.getElementById('logsTableBody');
        if (!tableBody) return;

        // Show loading
        App.showLoading(tableBody);

        try {
            const level = document.getElementById('logLevelFilter')?.value || '';
            const url = level ? `/api/admin/logs?level=${level}` : '/api/admin/logs';
            
            const response = await App.apiCall(url);
            
            if (response.logs.length === 0) {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="4" class="text-center text-muted py-4">
                            No logs found
                        </td>
                    </tr>
                `;
            } else {
                tableBody.innerHTML = response.logs.map(log => `
                    <tr>
                        <td>${App.formatTimestamp(log.timestamp)}</td>
                        <td>
                            <span class="badge badge-${this.getLogLevelClass(log.level)}">
                                ${log.level}
                            </span>
                        </td>
                        <td>${App.escapeHtml(log.module || '-')}</td>
                        <td>${App.escapeHtml(log.message)}</td>
                    </tr>
                `).join('');
            }

        } catch (error) {
            console.error('Error loading logs:', error);
            tableBody.innerHTML = `
                <tr>
                    <td colspan="4" class="text-center text-danger py-4">
                        <i class="fas fa-exclamation-triangle me-2"></i>
                        Error loading logs
                    </td>
                </tr>
            `;
        }
    }

    async loadUsers() {
        const tableBody = document.getElementById('usersTableBody');
        if (!tableBody) return;

        // Show loading
        App.showLoading(tableBody);

        try {
            const response = await App.apiCall('/api/admin/users');
            
            if (response.users.length === 0) {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="5" class="text-center text-muted py-4">
                            No users found
                        </td>
                    </tr>
                `;
            } else {
                tableBody.innerHTML = response.users.map(user => `
                    <tr>
                        <td>${user.id}</td>
                        <td>${App.escapeHtml(user.username)}</td>
                        <td>${App.escapeHtml(user.email)}</td>
                        <td>${App.formatTimestamp(user.created_at)}</td>
                        <td>
                            <span class="badge badge-${user.is_active ? 'success' : 'secondary'}">
                                ${user.is_active ? 'Active' : 'Inactive'}
                            </span>
                        </td>
                    </tr>
                `).join('');
            }

        } catch (error) {
            console.error('Error loading users:', error);
            tableBody.innerHTML = `
                <tr>
                    <td colspan="5" class="text-center text-danger py-4">
                        <i class="fas fa-exclamation-triangle me-2"></i>
                        Error loading users
                    </td>
                </tr>
            `;
        }
    }

    getLogLevelClass(level) {
        switch (level) {
            case 'ERROR':
                return 'danger';
            case 'WARNING':
                return 'warning';
            case 'INFO':
                return 'info';
            default:
                return 'secondary';
        }
    }

    destroy() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
        }
    }
}

// Initialize admin app when page loads
document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname.includes('/admin')) {
        new AdminApp();
    }
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (window.adminApp) {
        window.adminApp.destroy();
    }
});
