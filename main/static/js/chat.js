document.addEventListener('DOMContentLoaded', function () {
    const chatBtn = document.getElementById('chat-widget-btn');
    const chatContainer = document.getElementById('chat-widget-container');
    const chatMessages = document.getElementById('chat-widget-messages');
    const chatInput = document.getElementById('chat-widget-input');
    const chatSendBtn = document.getElementById('chat-widget-send');

    // Toggle chat window
    chatBtn.addEventListener('click', function () {
        chatContainer.classList.toggle('active');
        if (chatContainer.classList.contains('active')) {
            setTimeout(() => chatInput.focus(), 100);
        }
    });

    // Send message function
    function sendMessage() {
        const message = chatInput.value.trim();
        if (!message) return;

        // Add user message
        addMessage(message, 'user');
        chatInput.value = '';

        // Show typing indicator
        const typingHTML = `<div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>`;
        const typingElement = addMessage(typingHTML, 'bot', true);

        // Call Backend API
        fetch('/chatbot/predict/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        })
            .then(response => response.json())
            .then(data => {
                // Remove typing indicator
                if (typingElement) typingElement.remove();
                // Fallback: Remove any stray typing indicators
                document.querySelectorAll('.typing-indicator').forEach(el => el.closest('.chat-message')?.remove());

                // Add bot response
                if (data.answer) {
                    addMessage(data.answer, 'bot', true);
                } else {
                    addMessage("Sorry, I encountered an error.", 'bot');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                if (typingElement) typingElement.remove();
                addMessage("Error connecting to server.", 'bot');
            });
    }

    // Helper to add message to UI
    function addMessage(text, sender, isHTML = false) {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('chat-message', sender);

        if (isHTML) {
            msgDiv.innerHTML = text;
        } else {
            msgDiv.textContent = text;
        }

        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return msgDiv;
    }

    // Event Listeners
    chatSendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') sendMessage();
    });

    // Close on click outside
    document.addEventListener('click', function (event) {
        if (!chatContainer.contains(event.target) && !chatBtn.contains(event.target) && chatContainer.classList.contains('active')) {
            chatContainer.classList.remove('active');
        }
    });
});
