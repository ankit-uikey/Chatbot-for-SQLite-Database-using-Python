document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    const themeToggle = document.getElementById("theme-toggle");
    const conversationList = document.getElementById("conversation-list");
    const newConversationBtn = document.getElementById("new-conversation");

    let conversations = [];
    let currentConversation = [];

    // Load saved conversations
    if (localStorage.getItem("conversations")) {
        conversations = JSON.parse(localStorage.getItem("conversations"));
        updateConversationList();
    }

    // Toggle Theme
    themeToggle.addEventListener("click", () => {
        document.body.classList.toggle("dark-mode");
        themeToggle.textContent = document.body.classList.contains("dark-mode") ? "☀️" : "🌙";
    });

    // Send Message
    sendBtn.addEventListener("click", () => {
        const message = userInput.value.trim();
        if (message) {
            addMessage("user", message);
            fetchBotResponse(message);
            userInput.value = "";
        }
    });

    // Add Message to Chat
    function addMessage(sender, text) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", sender === "user" ? "user-message" : "bot-message");

        if (sender === "bot") {
            const botImg = document.createElement("img");
            botImg.src = "bot-icon.png"; // Replace with actual bot icon
            messageDiv.appendChild(botImg);
        }

        messageDiv.innerHTML += text;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;

        currentConversation.push({ sender, text });
    }

    // Fetch Response from Backend
    function fetchBotResponse(message) {
        fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message }),
        })
        .then(response => response.json())
        .then(data => addMessage("bot", data.response))
        .catch(() => addMessage("bot", "Error fetching response."));
    }

    // Update Conversation List
    function updateConversationList() {
        conversationList.innerHTML = "";
        conversations.forEach((conv, index) => {
            const listItem = document.createElement("li");
            listItem.textContent = `Conversation ${index + 1}`;
            listItem.addEventListener("click", () => loadConversation(index));
            conversationList.appendChild(listItem);
        });
    }

    // Load Conversation
    function loadConversation(index) {
        chatBox.innerHTML = "";
        conversations[index].forEach(msg => addMessage(msg.sender, msg.text));
        currentConversation = conversations[index];
    }

    // Start New Conversation
    newConversationBtn.addEventListener("click", () => {
        if (currentConversation.length) {
            conversations.push(currentConversation);
            localStorage.setItem("conversations", JSON.stringify(conversations));
            updateConversationList();
        }
        chatBox.innerHTML = "";
        currentConversation = [];
    });
});
