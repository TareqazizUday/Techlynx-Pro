// Custom JavaScript - Add your custom JS here

// Dark mode toggle example
function toggleDarkMode() {
    document.documentElement.classList.toggle('dark');
    localStorage.setItem('darkMode', document.documentElement.classList.contains('dark'));
}

// Load dark mode preference
if (localStorage.getItem('darkMode') === 'true') {
    document.documentElement.classList.add('dark');
}

// ========================================
// MOBILE MENU
// ========================================

function initMobileMenu() {
    const menuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    const mobileMenuOverlay = document.getElementById('mobile-menu-overlay');
    const menuClose = document.getElementById('mobile-menu-close');

    if (!menuButton || !mobileMenu || !mobileMenuOverlay || !menuClose) {
        return; // Elements not found, skip initialization
    }

    // Open mobile menu
    function openMenu() {
        mobileMenu.classList.remove('translate-x-full');
        mobileMenuOverlay.classList.remove('hidden');
        document.body.style.overflow = 'hidden'; // Prevent body scroll
    }

    // Close mobile menu
    function closeMenu() {
        mobileMenu.classList.add('translate-x-full');
        mobileMenuOverlay.classList.add('hidden');
        document.body.style.overflow = ''; // Restore body scroll
    }

    // Event listeners
    menuButton.addEventListener('click', openMenu);
    menuClose.addEventListener('click', closeMenu);
    mobileMenuOverlay.addEventListener('click', closeMenu);

    // Close menu when clicking on a link
    const mobileMenuLinks = mobileMenu.querySelectorAll('a');
    mobileMenuLinks.forEach(link => {
        link.addEventListener('click', () => {
            setTimeout(closeMenu, 100); // Small delay for better UX
        });
    });

    // Close menu on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && !mobileMenu.classList.contains('translate-x-full')) {
            closeMenu();
        }
    });
}

// ========================================
// TECHLYNX CHATBOT
// ========================================

class TechlynxChatbot {
    constructor() {
        this.chatBubble = document.getElementById('chat-bubble');
        this.chatWindow = document.getElementById('chat-window');
        this.chatClose = document.getElementById('chat-close');
        this.chatForm = document.getElementById('chat-form');
        this.chatInput = document.getElementById('chat-input');
        this.chatMessages = document.getElementById('chat-messages');
        this.typingIndicator = document.getElementById('typing-indicator');
        this.isOpen = false;
        
        // Check if all required elements exist
        if (!this.chatBubble || !this.chatWindow || !this.chatClose || 
            !this.chatForm || !this.chatInput || !this.chatMessages || !this.typingIndicator) {
            console.error('Chatbot: Required elements not found');
            return;
        }
        
        // Initialize event listeners
        this.init();
    }

    init() {
        if (!this.chatBubble) return; // Safety check
        
        // Toggle chat window
        this.chatBubble.addEventListener('click', () => {
            console.log('Chat bubble clicked');
            this.toggleChat();
        });
        this.chatClose.addEventListener('click', () => {
            this.toggleChat();
        });

        // Handle form submission
        this.chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendMessage();
        });

        // Handle Enter key (Shift+Enter for new line)
        this.chatInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Handle Escape key to close chat
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.toggleChat();
            }
        });
    }

    toggleChat() {
        if (!this.chatWindow || !this.chatInput) return; // Safety check
        
        this.isOpen = !this.isOpen;
        console.log('Toggle chat - isOpen:', this.isOpen);
        
        if (this.isOpen) {
            this.chatWindow.classList.remove('hidden');
            this.chatInput.focus();
            // Scroll to bottom
            this.scrollToBottom();
        } else {
            // Clear history when closing
            this.clearHistory();
            this.chatWindow.classList.add('hidden');
        }
    }

    async sendMessage() {
        if (!this.chatInput) return; // Safety check
        
        const message = this.chatInput.value.trim();
        
        if (!message) return;

        // Validate message length
        if (message.length > 500) {
            this.displayMessage('Message is too long. Please keep it under 500 characters.', false, true);
            return;
        }

        // Clear input
        this.chatInput.value = '';

        // Display user message
        this.displayMessage(message, true);

        // Show typing indicator
        this.showTypingIndicator();

        try {
            // Get CSRF token
            const csrfToken = this.getCookie('csrftoken');

            // Send request to backend
            const response = await fetch('/api/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ message: message })
            });

            // Hide typing indicator
            this.hideTypingIndicator();

            if (!response.ok) {
                const errorData = await response.json();
                
                if (response.status === 429) {
                    this.displayMessage('You have reached the query limit. Please try again later.', false, true);
                } else {
                    this.displayMessage(errorData.error || 'Sorry, I encountered an error. Please try again.', false, true);
                }
                return;
            }

            const data = await response.json();
            
            // Display bot response
            this.displayMessage(data.response, false);

        } catch (error) {
            console.error('Chatbot error:', error);
            this.hideTypingIndicator();
            this.displayMessage('Network error. Please check your connection and try again.', false, true);
        }
    }

    displayMessage(text, isUser = false, isError = false) {
        if (!this.chatMessages) return; // Safety check
        
        const messageDiv = document.createElement('div');
        messageDiv.className = 'flex gap-3';
        
        if (isUser) {
            messageDiv.classList.add('justify-end');
            messageDiv.innerHTML = `
                <div class="bg-primary text-white rounded-2xl rounded-tr-none px-4 py-3 max-w-[80%] shadow-sm">
                    <p class="text-sm">${this.escapeHtml(text)}</p>
                </div>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="size-8 bg-primary rounded-full flex items-center justify-center flex-shrink-0">
                    <span class="material-symbols-outlined text-white text-sm">smart_toy</span>
                </div>
                <div class="bg-white dark:bg-slate-900 rounded-2xl rounded-tl-none px-4 py-3 max-w-[80%] shadow-sm ${isError ? 'border-2 border-red-300' : ''}">
                    <p class="text-sm text-slate-700 dark:text-slate-300 ${isError ? 'text-red-600 dark:text-red-400' : ''}">${this.formatBotMessage(text)}</p>
                </div>
            `;
        }

        // Remove welcome message if this is the first real message
        const welcomeMessages = this.chatMessages.querySelectorAll('.flex.gap-3');
        if (welcomeMessages.length === 1 && isUser) {
            // Keep welcome message
        }

        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    formatBotMessage(text) {
        // Escape HTML first to prevent XSS
        text = this.escapeHtml(text);
        
        // Remove bullet point markers (* or -) and keep as simple lines
        text = text.replace(/^\s*[\*\-]\s+/gm, '');
        
        // Convert markdown-style formatting to HTML
        // Bold: **text** or __text__
        text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        text = text.replace(/__(.*?)__/g, '<strong>$1</strong>');
        
        // Line breaks (paragraph breaks)
        text = text.replace(/\n\n/g, '</p><p class="mt-3">');
        text = text.replace(/\n/g, '<br>');
        
        // Wrap in paragraph if not already wrapped
        if (!text.startsWith('<p')) {
            text = '<p>' + text + '</p>';
        }
        
        // Links (optional - if Gemini returns URLs)
        text = text.replace(/(https?:\/\/[^\s<]+)/g, '<a href="$1" target="_blank" class="text-primary underline hover:text-primary/80">$1</a>');
        
        return text;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    showTypingIndicator() {
        if (!this.typingIndicator) return; // Safety check
        this.typingIndicator.classList.remove('hidden');
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        if (!this.typingIndicator) return; // Safety check
        this.typingIndicator.classList.add('hidden');
    }

    scrollToBottom() {
        if (!this.chatMessages) return; // Safety check
        setTimeout(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }, 100);
    }

    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    saveHistory() {
        if (!this.chatMessages) return; // Safety check
        
        // Save chat messages to sessionStorage
        const messages = [];
        const messageElements = this.chatMessages.querySelectorAll('.flex.gap-3');
        
        messageElements.forEach(el => {
            if (el.querySelector('.bg-primary.text-white')) {
                // User message
                const text = el.querySelector('.bg-primary.text-white p').textContent;
                messages.push({ type: 'user', text: text });
            } else if (el.querySelector('.bg-white.dark\\:bg-slate-900 p')) {
                // Bot message
                const text = el.querySelector('.bg-white.dark\\:bg-slate-900 p').innerHTML;
                messages.push({ type: 'bot', text: text });
            }
        });

        sessionStorage.setItem('chatbot_history', JSON.stringify(messages));
    }

    loadHistory() {
        if (!this.chatMessages) return; // Safety check
        
        const history = sessionStorage.getItem('chatbot_history');
        if (!history) return;

        try {
            const messages = JSON.parse(history);
            
            // Clear current messages except welcome
            this.chatMessages.innerHTML = `
                <div class="flex gap-3">
                    <div class="size-8 bg-primary rounded-full flex items-center justify-center flex-shrink-0">
                        <span class="material-symbols-outlined text-white text-sm">smart_toy</span>
                    </div>
                    <div class="bg-white dark:bg-slate-900 rounded-2xl rounded-tl-none px-4 py-3 max-w-[80%] shadow-sm">
                        <p class="text-sm text-slate-700 dark:text-slate-300">Hi! I'm Techlynx Assistant. Ask me about our services, pricing, or anything else!</p>
                    </div>
                </div>
            `;

            // Restore messages
            messages.forEach(msg => {
                if (msg.type === 'user') {
                    this.displayMessage(msg.text, true);
                } else {
                    // For bot messages, use innerHTML directly since it's already formatted
                    const messageDiv = document.createElement('div');
                    messageDiv.className = 'flex gap-3';
                    messageDiv.innerHTML = `
                        <div class="size-8 bg-primary rounded-full flex items-center justify-center flex-shrink-0">
                            <span class="material-symbols-outlined text-white text-sm">smart_toy</span>
                        </div>
                        <div class="bg-white dark:bg-slate-900 rounded-2xl rounded-tl-none px-4 py-3 max-w-[80%] shadow-sm">
                            <p class="text-sm text-slate-700 dark:text-slate-300">${msg.text}</p>
                        </div>
                    `;
                    this.chatMessages.appendChild(messageDiv);
                }
            });

            this.scrollToBottom();
        } catch (error) {
            console.error('Error loading chat history:', error);
        }
    }

    clearHistory() {
        if (!this.chatMessages) return; // Safety check
        
        // Clear sessionStorage
        sessionStorage.removeItem('chatbot_history');
        
        // Reset chat messages to welcome message only
        this.chatMessages.innerHTML = `
            <div class="flex gap-3">
                <div class="size-8 bg-primary rounded-full flex items-center justify-center flex-shrink-0">
                    <span class="material-symbols-outlined text-white text-sm">smart_toy</span>
                </div>
                <div class="bg-white dark:bg-slate-900 rounded-2xl rounded-tl-none px-4 py-3 max-w-[80%] shadow-sm">
                    <p class="text-sm text-slate-700 dark:text-slate-300">Hi! I'm Techlynx Assistant. Ask me about our services, pricing, or anything else!</p>
                </div>
            </div>
        `;
        
        console.log('Chat history cleared');
    }
}

// Initialize all components when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize mobile menu
    initMobileMenu();
    
    // Initialize chatbot
    window.techlynxChatbot = new TechlynxChatbot();
});

