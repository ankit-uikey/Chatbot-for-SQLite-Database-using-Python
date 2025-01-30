async function sendMessage() {
    let userInput = document.getElementById("user-input").value;
    let chatBox = document.getElementById("chat-box");

    chatBox.innerHTML += `<div><b>You:</b> ${userInput}</div>`;

    let response = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userInput }),
    });

    let result = await response.json();
    chatBox.innerHTML += `<div><b>Bot:</b> ${result.response}</div>`;

    document.getElementById("user-input").value = "";
}
