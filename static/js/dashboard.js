// Dashboard JavaScript functionality

class MemoryForensicsDashboard {
    constructor() {
        this.statsUpdateInterval = null;
        this.activityUpdateInterval = null;
        this.init();
    }

    init() {
        this.loadStats();
        this.setupEventListeners();
        this.startAutoRefresh();
        this.setupTooltips();
    }

    // Load real-time statistics
    loadStats() {
        fetch('/api/stats')
            .then(response => response.json())
            .then(data => {
                this.updateStatsDisplay(data);
            })
            .catch(error => {
                console.error('Error loading stats:', error);
                this.showError('Failed to load statistics');
            });
    }

    // Update stats display
    updateStatsDisplay(data) {
        const elements = {
            'reportCount': data.total_files || '0',
            'ruleCount': data.yara_rules || '0',
            'lastScan': data.last_scan || 'Never',
            'threatCount': '0' // Placeholder for threat count
        };

        Object.keys(elements).forEach(id => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = elements[id];
            }
        });
    }

    // Setup event listeners
    setupEventListeners() {
        // Tool launch buttons
        const volatilityForm = document.querySelector('form[action="/run-volatility"]');
        const yaraForm = document.querySelector('form[action="/run-yara"]');

        if (volatilityForm) {
            volatilityForm.addEventListener('submit', (e) => this.handleToolLaunch(e, 'volatility'));
        }

        if (yaraForm) {
            yaraForm.addEventListener('submit', (e) => this.handleToolLaunch(e, 'yara'));
        }

        // File download buttons
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-download]')) {
                e.preventDefault();
                this.downloadFile(e.target.dataset.download);
            }
        });

        // Refresh buttons
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-refresh]')) {
                e.preventDefault();
                this.loadStats();
                this.showSuccess('Statistics refreshed');
            }
        });
    }

    // Handle tool launch
    handleToolLaunch(event, tool) {
        event.preventDefault();
        
        const button = event.target.querySelector('button[type="submit"]');
        const originalText = button.innerHTML;
        
        // Show loading state
        button.innerHTML = '<span class="loading-spinner"></span> Launching...';
        button.disabled = true;

        fetch(`/run-${tool}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                this.showSuccess(`${tool.charAt(0).toUpperCase() + tool.slice(1)} GUI launched successfully!`);
            } else {
                this.showError(`Error: ${data.message}`);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            this.showError(`Error launching ${tool} GUI`);
        })
        .finally(() => {
            // Restore button state
            button.innerHTML = originalText;
            button.disabled = false;
        });
    }

    // Download file
    downloadFile(filePath) {
        const link = document.createElement('a');
        link.href = filePath;
        link.download = filePath.split('/').pop();
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    // Start auto-refresh
    startAutoRefresh() {
        // Refresh stats every 30 seconds
        this.statsUpdateInterval = setInterval(() => {
            this.loadStats();
        }, 30000);

        // Refresh activity every 60 seconds
        this.activityUpdateInterval = setInterval(() => {
            this.loadRecentActivity();
        }, 60000);
    }

    // Load recent activity
    loadRecentActivity() {
        fetch('/api/recent-activity')
            .then(response => response.json())
            .then(data => {
                this.updateActivityDisplay(data);
            })
            .catch(error => {
                console.error('Error loading activity:', error);
            });
    }

    // Update activity display
    updateActivityDisplay(activities) {
        const activityContainer = document.querySelector('.recent-activity');
        if (!activityContainer) return;

        activityContainer.innerHTML = activities.map(activity => `
            <div class="activity-item">
                <div class="d-flex justify-content-between">
                    <span>
                        <i class="fas fa-${this.getActivityIcon(activity.type)} me-2"></i>
                        ${activity.action}
                    </span>
                    <small class="text-muted">${activity.timestamp}</small>
                </div>
            </div>
        `).join('');
    }

    // Get activity icon
    getActivityIcon(type) {
        const icons = {
            'info': 'info-circle',
            'success': 'check-circle',
            'warning': 'exclamation-triangle',
            'error': 'times-circle'
        };
        return icons[type] || 'info-circle';
    }

    // Setup tooltips
    setupTooltips() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Show success message
    showSuccess(message) {
        this.showNotification(message, 'success');
    }

    // Show error message
    showError(message) {
        this.showNotification(message, 'danger');
    }

    // Show notification
    showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(notification);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    // Cleanup
    destroy() {
        if (this.statsUpdateInterval) {
            clearInterval(this.statsUpdateInterval);
        }
        if (this.activityUpdateInterval) {
            clearInterval(this.activityUpdateInterval);
        }
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.dashboard = new MemoryForensicsDashboard();
});

// Export for global access
window.MemoryForensicsDashboard = MemoryForensicsDashboard; 