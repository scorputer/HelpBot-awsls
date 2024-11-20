let currentBranch = 'branch_1';
let conversationHistory = [];
let currentRole = 'general'; // Set 'general' as the default role

function setupInputEventHandlers() {
    const inputField = document.getElementById('user-input');
    const customPromptInputField = document.getElementById('custom-prompt-input');

    inputField.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent default Enter behavior
            if (!event.shiftKey) {
                sendMessage(); // Send message when Shift is not pressed
            }
        }
    });

    customPromptInputField.addEventListener('keydown', function (event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            sendCustomPrompt();
        }
    });
}

function sendMessage() {
    const userInput = document.getElementById('user-input').value.trim();
    if (userInput === '') {
        alert("Please enter a message.");
        return;
    }

    // Add user message to conversation history
    conversationHistory.push({ role: 'user', content: userInput });

    // Display the user's message immediately with double line space after
    displayMessage("Guest", userInput, true, true);

    // Clear input field
    document.getElementById('user-input').value = '';

    const messageData = {
        input: userInput,
        role: currentRole,
        current_branch: currentBranch,
        history: conversationHistory
    };

    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(messageData),
    })
        .then(response => response.json())
        .then(data => {
            // Add bot message to conversation history
            conversationHistory.push({ role: 'bot', content: data.response });

            // Display the HelpBot's response with double line space after
            displayMessage(`${getRoleName(currentRole)} HelpBot`, data.response, true, true);
        })
        .catch(error => {
            console.error('Error:', error);
            displayMessage('Error', 'Could not get a response from the HelpBot.', false, false);
        });
}

function getRoleName(roleValue) {
    const selector = document.getElementById('role-selector');
    const option = selector.querySelector(`option[value="${roleValue}"]`);
    return option ? option.textContent : 'General Use'; // Default to 'General Use'
}

function displayMessage(sender, message, isSenderBold, addDoubleSpaceAfter) {
    const chatWindow = document.getElementById('conversation-tab');
    const messageWrapper = document.createElement("div");
    messageWrapper.classList.add('message-wrapper');

    if (isSenderBold) {
        const senderSpan = document.createElement("span");
        senderSpan.textContent = `${sender}: `;
        senderSpan.classList.add('sender');
        messageWrapper.appendChild(senderSpan);
    }

    const messageLines = message.split(/[\r\n]+/);
    messageLines.forEach((line, index) => {
        const messageText = document.createElement("div");
        messageText.textContent = line;
        messageText.classList.add('message-text');
        messageWrapper.appendChild(messageText);
        if (index < messageLines.length - 1) {
            const breakLine = document.createElement("div");
            breakLine.classList.add('line-break');
            messageWrapper.appendChild(breakLine);
        }
    });

    if (addDoubleSpaceAfter) {
        const doubleSpace = document.createElement("div");
        doubleSpace.classList.add('double-space');
        messageWrapper.appendChild(doubleSpace);
    }

    chatWindow.appendChild(messageWrapper);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function loadRoles() {
    fetch('/roles')
        .then(response => response.json())
        .then(data => {
            const selector = document.getElementById('role-selector');
            data.forEach(role => {
                const option = document.createElement('option');
                option.value = role.value;
                option.textContent = role.name;
                selector.appendChild(option);
            });
            selector.value = currentRole; // Set the default selected role
            selectRole(); // Trigger selection of default role
        });
}

function selectRole() {
    const selector = document.getElementById('role-selector');
    currentRole = selector.value || currentRole; // Use selector value or default
    conversationHistory = []; // Clear conversation history
    currentBranch = 'branch_1'; // Reset to the first branch

    fetch(`/prompt/${currentRole}`) // Fetch the initial prompt
        .then(response => response.json())
        .then(data => {
            if (data.initial_prompt) {
                displayMessage(`${getRoleName(currentRole)} HelpBot`, data.initial_prompt, true);
            } else {
                // Default message if no initial prompt is found
                displayMessage(`${getRoleName(currentRole)} HelpBot`, "How can I assist you today?", true);
            }
            document.getElementById('user-input').disabled = false;
            document.querySelector('button[onclick="sendMessage()"]').disabled = false;
        })
        .catch(error => {
            console.error('Error fetching initial prompt:', error);
        });
}

function downloadConversation() {
    let conversationText = conversationHistory.map(entry => `${entry.role.toUpperCase()}: ${entry.content}`).join('\n');
    let blob = new Blob([conversationText], { type: "text/plain;charset=utf-8" });
    let url = URL.createObjectURL(blob);

    let a = document.createElement('a');
    a.href = url;
    a.download = 'HelpBot-Conversation.txt';
    a.click();

    URL.revokeObjectURL(url);
}
window.onload = function () {
    loadRoles();
    setupInputEventHandlers();
};
