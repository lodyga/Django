document.addEventListener('DOMContentLoaded', () => {
  const aiAssistantButton = document.getElementById('aiAssistantButton');
  const storedUser = document.getElementById('userContainer');
  const userName = storedUser.getAttribute('userName');
  const chatBox = document.getElementById("chatBox");
  const savedChat = sessionStorage.getItem('chatHistory');
  if (savedChat) {
    chatBox.value = savedChat;
  };
  const userInput = document.getElementById("userInput");
  const sendButton = document.getElementById("sendButton");

  // Function to add a message to the chat box
  function addMessage(role, message) {
    // const messageElement = document.createElement("div");
    // messageElement.innerHTML = `<strong>${role}:</strong> ${message}`;
    // chatBox.appendChild(messageElement);
    chatBox.value += `\n${role}: ${message}`;
    chatBox.scrollTop = chatBox.scrollHeight;  // Auto-scroll to the bottom
    sessionStorage.setItem('chatHistory', chatBox.value)
  }

  // Get the CSRF token from the cookie
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }


  // Function to send a message to the backend
  async function sendMessage() {
    // Include the CSRF token in the request headers
    const csrfToken = getCookie("csrftoken");
    const message = userInput.value.trim();
    if (!message) return;

    // Show spinner and disable button
    sendButton.disabled = true;
    sendButton.firstChild.textContent = "Wait ";
    document.getElementById('aiSendButtonSpinner').classList.remove("d-none");

    // Add the user's message to the chat box
    addMessage(userName, message);
    userInput.value = "";  // Clear the input field

    // Send the message to the backend
    const response = await fetch("", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": csrfToken,  // Add CSRF token for Django
      },
      body: `message=${encodeURIComponent(message)}`,
    });

    if (response.ok) {
      const data = await response.json();
      addMessage("AI", data.response);
    } else {
      addMessage("AI", "Error: Could not get a response.");
    }

    // Hide spinner and re-enable button
    sendButton.disabled = false;
    sendButton.firstChild.textContent = "Send";
    document.getElementById('aiSendButtonSpinner').classList.add('d-none');
  }

  // Event listener for the send button
  sendButton.addEventListener('click', sendMessage);
  userInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') sendMessage();
  });

  aiAssistantButton.addEventListener('click', () => {
    aiContainer.classList.toggle("d-none");
  });
});