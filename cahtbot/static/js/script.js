document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    let step = 0;
    let chatData = {
        source: '',
        destination: '',
        date: '',
        next_step: null
    };

    function appendMessage(text, isBot = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isBot ? 'bot-message' : 'user-message'}`;
        messageDiv.innerHTML = text; // Use innerHTML to allow links
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
                        if (data.reset) {
                            step = 0; // Reset step for a new query
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        appendMessage('Sorry, something went wrong. Please try again.', true);
                    });
                }, 1000); // Adjust delay as needed
            } else if (step === 3) {
                chatData.next_step = text.toLowerCase().includes('buses') ? 'search_buses' : 'chatgpt';
                chatData.user_input = text;
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
                        if (data.reset) {
                            step = 0; // Reset step for a new query
                        }
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
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});
