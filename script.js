document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    let step = 0;
    let chatData = {
        source: '',
        destination: '',
        date: ''
    };

    function appendMessage(text, isBot = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isBot ? 'bot-message' : 'user-message'}`;
        messageDiv.textContent = text;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
    }

    function showTypingIndicator() {
        const typingIndicator = document.createElement('div');
        typingIndicator.className = 'message bot-message typing';
        typingIndicator.innerHTML = 'Typing<span class="dots">...</span>';
        chatBox.appendChild(typingIndicator);
        chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom

        // Remove typing indicator after delay
        setTimeout(() => {
            typingIndicator.remove();
        }, 1000); // Adjust delay as needed
    }

    function sendMessage() {
        const text = userInput.value.trim();
        if (text) {
            appendMessage(text);
            userInput.value = '';
            if (step === 0) {
                chatData.source = text;
                appendMessage('Where would you like to go? (Destination)', true);
                step++;
            } else if (step === 1) {
                chatData.destination = text;
                appendMessage('Please provide the travel date (YYYY-MM-DD)', true);
                step++;
            } else if (step === 2) {
                chatData.date = text;
                showTypingIndicator();
                setTimeout(() => {
                    fetch('/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(chatData),
                    })
                    .then(response => response.json())
                    .then(data => {
                        appendMessage(data.reply, true);
                        step = 0; // Reset step for a new query
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        appendMessage('Sorry, something went wrong. Please try again.', true);
                    });
                }, 1000); // Adjust delay as needed
            }
        }
    }

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Initial bot greeting
    appendMessage('Where are you starting your journey? (Source)', true);
});
