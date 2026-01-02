class ChatBot {
    constructor() {
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.chatMessages = document.getElementById('chatMessages');
        this.typingIndicator = document.getElementById('typingIndicator');
        
        this.initializeEventListeners();
        this.focusInput();
    }

    initializeEventListeners() {
        // Send button click
        this.sendButton.addEventListener('click', () => this.sendMessage());
        
        // Enter key press
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Input focus effects
        this.messageInput.addEventListener('focus', () => {
            this.messageInput.parentElement.style.transform = 'translateY(-2px)';
        });

        this.messageInput.addEventListener('blur', () => {
            this.messageInput.parentElement.style.transform = 'translateY(0)';
        });

        // Auto-resize input (optional enhancement)
        this.messageInput.addEventListener('input', () => {
            if (this.messageInput.value.trim()) {
                this.sendButton.style.background = 'linear-gradient(135deg, #10b981, #059669)';
            } else {
                this.sendButton.style.background = 'linear-gradient(135deg, #4f46e5, #7c3aed)';
            }
        });
    }

    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message) return;

        // Clear input and disable send button
        this.messageInput.value = '';
        this.sendButton.disabled = true;
        this.sendButton.style.background = 'linear-gradient(135deg, #4f46e5, #7c3aed)';

        // Add user message to chat
        this.addMessage(message, 'user');

        // Show typing indicator
        this.showTypingIndicator();

        try {
            // Send message to backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            // Hide typing indicator
            this.hideTypingIndicator();

            // Add bot response
            this.addMessage(data.response, 'bot');

        } catch (error) {
            console.error('Error:', error);
            this.hideTypingIndicator();
            
            // Show error message
            this.addMessage('Sorry, I encountered an error. Please try again.', 'bot', true);
        } finally {
            // Re-enable send button
            this.sendButton.disabled = false;
            this.focusInput();
        }
    }

    addMessage(content, sender, isError = false) {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${sender}-message`;
        
        const currentTime = new Date().toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit' 
        });

        const avatarContent = sender === 'user' ? '' : '🤖';
        const errorClass = isError ? ' error' : '';

        messageElement.innerHTML = `
            <div class="message-avatar">${avatarContent}</div>
            <div class="message-content${errorClass}">
                <p>${this.formatMessage(content)}</p>
                <span class="message-time">${currentTime}</span>
            </div>
        `;

        // Add loading animation initially
        messageElement.classList.add('loading');
        this.chatMessages.appendChild(messageElement);
        this.scrollToBottom();

        // Remove loading animation after a short delay
        setTimeout(() => {
            messageElement.classList.remove('loading');
        }, 300);
    }

    formatMessage(message) {
        // Basic text formatting
        return message
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>');
    }

    showTypingIndicator() {
        this.typingIndicator.classList.add('visible');
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        this.typingIndicator.classList.remove('visible');
    }

    scrollToBottom() {
        setTimeout(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }, 100);
    }

    focusInput() {
        setTimeout(() => {
            this.messageInput.focus();
        }, 100);
    }

    // Add some demo functionality for testing without backend
    addDemoMessage() {
        const demoResponses = [
            "That's an interesting question! Let me think about it...",
            "I understand what you're asking. Here's my perspective...",
            "Great point! I'd be happy to help with that.",
            "That's a complex topic. Let me break it down for you...",
            "I see what you mean. Here's what I think..."
        ];

        const randomResponse = demoResponses[Math.floor(Math.random() * demoResponses.length)];
        this.addMessage(randomResponse, 'bot');
    }
}

// Enhanced demo mode for testing
class DemoChatBot extends ChatBot {
    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message) return;

        // Clear input and disable send button
        this.messageInput.value = '';
        this.sendButton.disabled = true;

        // Add user message to chat
        this.addMessage(message, 'user');

        // Show typing indicator
        this.showTypingIndicator();

        // Simulate API delay
        setTimeout(() => {
            this.hideTypingIndicator();
            
            // Generate demo response
            const demoResponses = [
                `I received your message: "${message}". This is a demo response!`,
                "That's an interesting question! In demo mode, I can only provide sample responses.",
                "Thanks for your message! To get real AI responses, please start the backend server.",
                "I understand what you're saying. This is just a demo interface showing how the chat works.",
                "Great question! The real AI chatbot will be much more helpful once connected to the backend."
            ];

            const randomResponse = demoResponses[Math.floor(Math.random() * demoResponses.length)];
            this.addMessage(randomResponse, 'bot');

            // Re-enable send button
            this.sendButton.disabled = false;
            this.focusInput();
        }, 1500 + Math.random() * 1000); // Random delay between 1.5-2.5 seconds
    }
}

// Initialize the chatbot when the page loads
document.addEventListener('DOMContentLoaded', () => {
    // Try to detect if backend is available
    fetch('/chat', { method: 'GET' })
        .then(() => {
            // Backend is available, use full functionality
            window.chatBot = new ChatBot();
            console.log('Connected to backend server');
        })
        .catch(() => {
            // Backend not available, use demo mode
            window.chatBot = new DemoChatBot();
            console.log('Running in demo mode - start the backend server for full functionality');
            
            // Add a demo message after a short delay
            setTimeout(() => {
                const demoMessageElement = document.createElement('div');
                demoMessageElement.className = 'message bot-message';
                demoMessageElement.innerHTML = `
                    <div class="message-avatar">🤖</div>
                    <div class="message-content">
                        <p><strong>Demo Mode:</strong> The backend server is not running. Start the Flask server to enable real AI responses!</p>
                        <span class="message-time">Just now</span>
                    </div>
                `;
                document.getElementById('chatMessages').appendChild(demoMessageElement);
                window.chatBot.scrollToBottom();
            }, 1000);
        });
});

// Add some keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl+/ or Cmd+/ to focus input
    if ((e.ctrlKey || e.metaKey) && e.key === '/') {
        e.preventDefault();
        document.getElementById('messageInput').focus();
    }
    
    // Escape to blur input
    if (e.key === 'Escape') {
        document.getElementById('messageInput').blur();
    }
});

// Add smooth scrolling behavior
document.getElementById('chatMessages').addEventListener('scroll', function() {
    const isAtBottom = this.scrollHeight - this.scrollTop === this.clientHeight;
    
    // Add shadow effect when not at bottom
    if (!isAtBottom) {
        this.style.boxShadow = 'inset 0 -10px 10px -10px rgba(0,0,0,0.1)';
    } else {
        this.style.boxShadow = 'none';
    }
});

// Export for potential external use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ChatBot, DemoChatBot };
}