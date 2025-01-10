// Handle sending user input and bot response
document.getElementById("send-btn").addEventListener("click", sendMessage);
document.getElementById("user-input").addEventListener("keypress", function(event) {
  if (event.key === 'Enter') {
    sendMessage();
  }
});

// Handle voice input
document.getElementById("voice-btn").addEventListener("click", startVoiceInput);

// Handle logout
document.getElementById("logout-btn").addEventListener("click", function() {
  window.location.href = "login.html"; // Redirect back to login page
});

// Send message and get a response
async function sendMessage() {
  const userInput = document.getElementById("user-input").value.trim();
  if (!userInput) return;

  // Display the user's message
  displayMessage(userInput, "user");

  // Fetch the bot's response from the server
  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ input: userInput })
    });

    if (!response.ok) {
      throw new Error("Failed to fetch the response from the server.");
    }

    const data = await response.json();
    displayMessage(data.response, "bot"); // Display the bot's response
  } catch (error) {
    console.error("Error:", error);
    displayMessage("Oops! Something went wrong. Please try again.", "bot");
  }

  // Clear the input field
  document.getElementById("user-input").value = "";
}

// Display a message in the chat content
function displayMessage(message, sender) {
  const chatContent = document.getElementById("chat-content");

  const messageDiv = document.createElement("div");
  messageDiv.classList.add("chat-message", sender);

  const messageText = document.createElement("p");
  messageText.textContent = message;

  messageDiv.appendChild(messageText);
  chatContent.appendChild(messageDiv);

  // Scroll to the latest message
  chatContent.scrollTop = chatContent.scrollHeight;
}

// Handle voice input using Web Speech API (Speech Recognition)
function startVoiceInput() {
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  recognition.lang = "en-US";
  recognition.start();

  recognition.onresult = function(event) {
    const transcript = event.results[0][0].transcript;
    document.getElementById("user-input").value = transcript;
    sendMessage(); // Send the recognized text as a message
  };

  recognition.onerror = function(event) {
    console.error("Speech recognition error:", event.error);
  };
}
